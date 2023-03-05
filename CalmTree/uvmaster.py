import bpy
import bmesh
import mathutils
from math import acos

class CALMTREE_OT_uv(bpy.types.Operator):
    """creates convienient uvmap for the tree"""
    bl_idname = 'object.tree_uv'
    bl_label = 'Create UV map'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        bpy.ops.object.editmode_toggle(True)
        info = [list(l) for l in bpy.context.object["CalmTreeLog"]]
        cam = context.scene.camera
        if not cam: 
            self.report({"INFO"}, "This won't work without camera in the scene")
            return{'FINISHED'}
        loc = bpy.context.scene.camera.location

        obj = bpy.context.object
        me = obj.data
        
        for bran in info:
            start = bran[0]
            sides = bran[2]
            

            base = [(v.co-loc).length for v in me.vertices[start:start+sides-1]]
            stidx = base.index(max(base))+start

            bran.append(stidx)
            index = [stidx,stidx+sides] # here the index you want select please change 

            bm = bmesh.from_edit_mesh(me)

            bm.verts.ensure_lookup_table()
            for i in index: bm.verts[i].select = True

            for edge in bm.edges:
                if edge.verts[0].select and edge.verts[1].select:
                    e = edge
                    e.seam = True

            loop = [l for l in e.link_loops if len(l.vert.link_edges)==4][0]

            while len(loop.vert.link_edges) == 4:
                loop = loop.link_loop_prev.link_loop_radial_prev.link_loop_prev

                e_next = loop.edge
                e_next.seam = True
            bmesh.update_edit_mesh(me)
            
            for vert in bm.verts:vert.select=False

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
        bpy.ops.mesh.select_all(action='DESELECT')

        for bran in info:
            Mstart = bran[0]
            Mend = bran[1]
            sides = bran[2]
            stidx = bran[3]

            for vert in bm.verts[Mstart:Mend+1]:vert.select = True
            uv_layer = bm.loops.layers.uv.verify()
            uv_verts = {}

            for face in bm.faces:
                if all([v.select for v in face.verts]):
                    for loop in face.loops:
                        if loop.vert not in uv_verts:
                            uv_verts[loop.vert] = [loop[uv_layer]]
                        else:
                            uv_verts[loop.vert].append(loop[uv_layer])
                            
            def newco(pt,start,end):
                dang = lambda pt1,pt2: acos((pt2[1]-pt1[1])/(pt2-pt1).length)
                alpha = dang(start, end)
                mat_rot = mathutils.Matrix.Rotation(alpha, 2)
                return mat_rot@pt
            coords = lambda idx : (uv_verts[bm.verts[idx]][0].uv+uv_verts[bm.verts[idx]][1].uv)/2
            print(bran)
            start = coords(stidx)
            end = coords(Mend-sides+stidx-Mstart)
            print(start,end)
            for vert in uv_verts:
                    for uv_loop in uv_verts[vert]:
                        pt = newco(uv_loop.uv,start,end)
                        uv_loop.uv = pt
            sstart = coords(stidx)
            eend = coords(Mend-sides+stidx-Mstart)
            print(sstart,eend)
            for vert in bm.verts:vert.select = False
            bmesh.update_edit_mesh(me)

        for face in bm.faces:face.select = True
        bpy.ops.uv.pack_islands(rotate=False, margin=0.001)
        bmesh.update_edit_mesh(me)    
        return {'FINISHED'}