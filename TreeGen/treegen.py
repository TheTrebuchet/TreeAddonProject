import bpy
import bmesh
from .geogroup import *
from .algorithm import *

def parameters():
    tps = bpy.data.window_managers["WinMan"].treegen_props
    
    # temporary parameters
    scale_lf1 = lambda x, a : 1/((x+1)**a)-(x/2)**a #this one is for trunk flare
    scale_lf2 = lambda x, a : ((1-(x-1)**2)/(a*(x-1)+1))**0.5  #this one is for branches scale
    
    l=tps.Mlength/tps.Mvres
    m_p = [tps.Msides, tps.Mlength, tps.Mradius, tps.Mtipradius, tps.Mscale, l]
    br_p = [tps.branch_levels, tps.branch_minangle, tps.branch_maxangle, tps.branch_height, tps.branch_variety, tps.branch_scaling, tps.branch_seed]
    bn_p = [tps.branch_number1, tps.branch_number2, tps.branch_number3]
    bd_p = [tps.bends_amount, tps.bends_up, tps.bends_correction, tps.bends_scale, tps.bends_weight/(tps.Mlength), tps.bends_seed]
    t_p = [scale_lf1, tps.flare_amount, scale_lf2, tps.branch_shift]
    r_p = [tps.Rperlin_amount, tps.Rperlin_scale, tps.Rperlin_seed]
    return m_p, br_p, bn_p, bd_p, r_p, t_p

def saveconfig():
    tps = bpy.data.window_managers["WinMan"].treegen_props
    config = ''
    excluded = ['__','rna','sync']
    for new in dir(tps):
            if not any(x in new for x in excluded):
                config += new + '=' +str(getattr(tps, new)) + ','
    return config


class TREEGEN_OT_new(bpy.types.Operator):
    """creates a tree at (0,0,0) according to user panel input"""
    bl_idname = 'object.tree_create'
    bl_label = 'Lob that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tps = context.window_manager.treegen_props

        m_p, br_p, bn_p, bd_p, r_p, t_p = parameters()
        seeds = [br_p[-1], bd_p[-1], r_p[-1]]

        #generates the trunk and lists of lists of stuff
        verts, edges, faces, selection = tree_gen(m_p, br_p, bn_p, bd_p, r_p, t_p, tps.facebool)

        #creating the tree
        mesh = bpy.data.meshes.new("tree")
        object = bpy.data.objects.new("tree", mesh)
        bpy.context.collection.objects.link(object)
        mesh.from_pydata(verts ,edges, faces)
        
        #name of the created object and selecting it
        bpy.ops.object.select_all(action='DESELECT')
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.shade_smooth()
        object.matrix_world.translation = context.scene.cursor.location

        #writing properties
        br_p[-1], bd_p[-1], r_p[-1] = seeds
        context.object["TreeGenConfig"] = saveconfig()

        #adding vertex group for furthest branches
        if selection:
            v_group = object.vertex_groups.new(name="leaves")
            v_group.add(selection, 1.0, 'ADD')

        #adding geometry nodes for leaves
        if 'TreeGen_nodegroup' not in bpy.data.node_groups:
            TreeGen_nodegroup_exec()
        ng = bpy.data.node_groups['TreeGen_nodegroup']
        if 'TreeGen' not in bpy.context.object.modifiers:
            bpy.context.object.modifiers.new(name = 'TreeGen',type = 'NODES')
        geo_mod = bpy.context.object.modifiers['TreeGen']
        if not geo_mod.node_group:
            geo_mod.node_group = ng
        bpy.ops.object.geometry_nodes_input_attribute_toggle(prop_path="[\"Input_2_use_attribute\"]", modifier_name="TreeGen")
        bpy.context.object.modifiers["TreeGen"]["Input_2_attribute_name"] = "leaves"
        tps.treename = context.object.name
        verts = []
        faces = []
        return {'FINISHED'}
        
class TREEGEN_OT_update(bpy.types.Operator):
    """updates the tree according to user panel input"""
    bl_idname = 'object.tree_update'
    bl_label = 'update that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try: 
            bpy.context.object["TreeGenConfig"]
        except: 
            self.report({"INFO"}, "I can't update an object that isn't a tree")
            return {'FINISHED'}
        
        tps = context.window_manager.treegen_props
        selected_obj = bpy.context.object.data

        m_p, br_p, bn_p, bd_p, r_p, t_p = parameters()
        seeds = [br_p[-1], bd_p[-1], r_p[-1]]

        #generates the trunk and lists of lists of stuff
        verts, edges, faces, selection = tree_gen(m_p, br_p, bn_p, bd_p, r_p, t_p, tps.facebool)
        
        
        #updating mesh, tree update is a temporary object
        t_mesh = bpy.data.meshes.new('tree update')
        t_mesh.from_pydata(verts,edges,faces)

        bm = bmesh.new()
        bm.from_mesh(t_mesh)

        bm.to_mesh(selected_obj)
        bm.free()
        bpy.data.meshes.remove(t_mesh)
        for f in selected_obj.polygons:
            f.use_smooth = True
        
        v_group = bpy.context.object.vertex_groups['leaves']
        v_group.remove([i for i in range(len(verts))])
        v_group.add(selection, 1.0, 'REPLACE')
        
        br_p[-1], bd_p[-1], r_p[-1] = seeds
        context.object["TreeGenConfig"] = saveconfig()

        return {'FINISHED'}

class TREEGEN_OT_sync(bpy.types.Operator):
    """syncs tps property group with custom properties"""
    bl_idname = 'object.tree_sync'
    bl_label = 'sync that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try: 
            bpy.context.object["TreeGenConfig"]
        except: 
            self.report({"INFO"}, "I can't sync an object that isn't a tree")
            return {'FINISHED'}
        
        tps = bpy.data.window_managers["WinMan"].treegen_props
        config = [i.split('=') for i in config.split(',')]
        excluded = ['__','rna','sync']
        tps.sync_complete = False
        for old in dir(tps):
                if not any(x in old for x in excluded):
                    new = [i for i in config if old in i][0][1]
                    print(old, new)
                    try:int(new)
                    except: pass
                    else: 
                        setattr(tps, old, int(new))
                        continue
                    try:float(new)
                    except: pass
                    else: 
                        setattr(tps, old, float(new))
                        continue
                    if new =='True':
                        setattr(tps,old,True)
                    elif new =='False':
                        setattr(tps,old,False)
                    else:
                        setattr(tps,old,new)
        tps.sync_complete = True

        return {'FINISHED'}

class TREEGEN_OT_default(bpy.types.Operator):
    """returns all values to default"""
    bl_idname = 'object.tree_default'
    bl_label = 'sync that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tps = bpy.data.window_managers["WinMan"].treegen_props
        tps.sync_complete = False
        for i in dir(tps):
            if '__' not in i and 'rna' not in i and 'sync' not in i:
                tps.property_unset(i)
        tps.sync_complete=True
        bpy.ops.object.tree_update()
        return {'FINISHED'}

class TREEGEN_OT_leaf(bpy.types.Operator):
    """handles leaves"""
    bl_idname = 'object.tree_leaf'
    bl_label = 'leaf that tree'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        tps = context.window_manager.treegen_props
        
        colname = "TreeGenLeaves"
        name = tps.leafname

        if colname not in [i.name for i in bpy.data.collections]:
            collection = bpy.data.collections.new(colname)
            bpy.context.scene.collection.children.link(collection)

        for col in bpy.data.collections:
            if col.name == colname and name not in [o.name for o in col.objects]:
                if name in [o.name for o in bpy.data.objects]:
                    object = bpy.data.objects[name]
                    bpy.context.scene.collection.objects.unlink(object)
                    col.objects.link(object)
                    break
                mesh = bpy.data.meshes.new(name)
                object = bpy.data.objects.new(name, mesh)
                col.objects.link(object)
                verts = [Vector((1,0,0)),Vector((1,2,0)),Vector((-1,2,0)),Vector((-1,0,0))]
                mesh.from_pydata(verts,[], [[0,1,2,3]])
        return {'FINISHED'}

class TREEGEN_PT_createparent:
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "Create"
    bl_context = "objectmode"

class TREEGEN_PT_createmain(TREEGEN_PT_createparent, bpy.types.Panel):
    """Creates a Panel in the Object properties window for tree creation, use with caution"""
    bl_label = "TreeGen"
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "Create"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        col = layout.column(align=True)
        tps = bpy.data.window_managers["WinMan"].treegen_props

        col.operator('object.tree_create', text = 'Create',icon='SCRIPT')
        col.operator('object.tree_sync', text = 'Sync', icon='FILE_REFRESH')
        col.operator('object.tree_default', text = 'Reset to default', icon='LOOP_BACK')
        col = layout.column(align=True)
        col.label(text="Main Settings:")
        col.prop(wm.treegen_props, "leafbool")
        col.prop(wm.treegen_props, "facebool")
        col = layout.column(align=True)
        col.label(text="Main Parameters")
        col.prop(wm.treegen_props, "Msides")
        col.prop(wm.treegen_props, "Mvres")
        col.prop(wm.treegen_props, "Mlength")
        col.prop(wm.treegen_props, "Mradius")
        col.prop(wm.treegen_props, "Mtipradius")
        

        col = layout.column(align=True)
        col.label(text="Growth Parameters")
        col.prop(wm.treegen_props, "bends_amount")
        col.prop(wm.treegen_props, "bends_scale")
        col.prop(wm.treegen_props, "bends_up")
        col.prop(wm.treegen_props, "bends_weight")
        col.prop(wm.treegen_props, "bends_correction")

        col = layout.column(align=True)
        col.label(text="Branch Parameters")
        col.prop(wm.treegen_props, "branch_levels")
        for i in range(tps.branch_levels):
            col.prop(wm.treegen_props, "branch_number"+str(i+1))
        col.prop(wm.treegen_props, "branch_scaling")
        col.prop(wm.treegen_props, "branch_minangle")
        col.prop(wm.treegen_props, "branch_maxangle")
        col.prop(wm.treegen_props, "branch_height")
        col.label(text="Simple Jiggle")
        col.prop(wm.treegen_props, "Rperlin_amount")
        col.prop(wm.treegen_props, "Rperlin_scale")
        col.label(text="Seeds and Variety")
        col.prop(wm.treegen_props, "Rperlin_seed")
        col.prop(wm.treegen_props, "bends_seed")
        col.prop(wm.treegen_props, "branch_seed")
        col.prop(wm.treegen_props, "branch_variety")
        col.label(text="Scale and Shape")
        col.prop(wm.treegen_props, "Mscale")
        col.prop(wm.treegen_props, 'flare_amount')
        col.prop(wm.treegen_props, 'branch_shift')
        

class TREEGEN_PT_createsubpanel(TREEGEN_PT_createparent, bpy.types.Panel):
    """Creates a Panel in the Object properties window for tree creation, use with caution"""
    bl_label = "Advanced"
    bl_parent_id = "TREEGEN_PT_createmain"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self,context):
        layout = self.layout
        wm = context.window_manager
        col = layout.prop_search(wm.treegen_props, 'leafname', context.scene, "objects")