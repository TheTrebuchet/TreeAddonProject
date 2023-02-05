import bpy
import bmesh
from .geogroup import *
from .algorithm import *
import time
def checkedit(context):
    config = context.object["TreeGenConfig"]
    for i in config.split(','):
        if 'edit' in i:
            if 'True' in i: return True 
            if 'False' in i: return False
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
    bl_label = 'Place a tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tps = context.window_manager.treegen_props

        m_p, br_p, bn_p, bd_p, r_p, t_p = parameters()
        seeds = [br_p[-1], bd_p[-1], r_p[-1]]
        
        #generates the trunk and lists of lists of branches
        m_p[3]*=m_p[2]
        st_pack = (Vector((0,0,0)),Vector((0,0,1))*m_p[1], m_p[2])
        branchlist = [[branch(st_pack, m_p, bd_p, br_p, r_p, True).generate()]]
        branchlist = outgrow(branchlist, br_p, bn_p, bd_p, r_p, t_p)
        verts, edges, faces, selection = toverts(branchlist, tps.facebool, m_p, br_p, t_p)
        
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
        
        #writing properties
        tps.treename = context.object.name
        br_p[-1], bd_p[-1], r_p[-1] = seeds
        context.object["TreeGenConfig"] = saveconfig()
        return {'FINISHED'}
        
class TREEGEN_OT_update(bpy.types.Operator):
    """updates the tree according to user panel input"""
    bl_idname = 'object.tree_update'
    bl_label = 'update the tree object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tps = context.window_manager.treegen_props   
        try: 
            bpy.context.object["TreeGenConfig"]
        except: 
            self.report({"INFO"}, "I can't update an object that isn't a tree")
            return {'FINISHED'}
        
        tree_obj = bpy.context.object
        custom_child = [o for o in tree_obj.children if 'custom trunk' in o.name]
        
        if len(custom_child)>1:
            self.report({"INFO"}, "I detected multiple viable trunks in the trees children, leave only one")
            return {'FINISHED'}
        
        branchlist = []
        m_p, br_p, bn_p, bd_p, r_p, t_p = parameters()
        seeds = [br_p[-1], bd_p[-1], r_p[-1]]
        
        if len(custom_child)==1:
            curve = [v.co for v in custom_child[0].data.vertices]
            if curve[-1].length<curve[0].length:
                curve.reverse()
            m_p[3]*=m_p[2]
            branchlist = branchinit(curve, m_p, bd_p, br_p, r_p)
        else:
            m_p[3]*=m_p[2]
            st_pack = (Vector((0,0,0)),Vector((0,0,1))*m_p[1], m_p[2])
            branchlist = [[branch(st_pack, m_p, bd_p, br_p, r_p, True).generate()]]
        
        '''
        # now this is just a temporary trick until blender fixes something
        if tps.treename != context.object.name:
            bpy.ops.object.tree_sync()
            tps.treename = context.object.name
        '''

        #generates the trunk and lists of lists of branches
        branchlist = outgrow(branchlist, br_p, bn_p, bd_p, r_p, t_p)
        verts, edges, faces, selection = toverts(branchlist, tps.facebool, m_p, br_p, t_p)
        
        #updating mesh, tree update is a temporary object
        t_mesh = bpy.data.meshes.new('tree update')
        t_mesh.from_pydata(verts,edges,faces)

        bm = bmesh.new()
        bm.from_mesh(t_mesh)

        bm.to_mesh(tree_obj.data)
        bm.free()
        bpy.data.meshes.remove(t_mesh)
        for f in tree_obj.data.polygons:
            f.use_smooth = True
        
        v_group = bpy.context.object.vertex_groups['leaves']
        v_group.remove([i for i in range(len(verts))])
        v_group.add(selection, 1.0, 'REPLACE')
        
        br_p[-1], bd_p[-1], r_p[-1] = seeds
        context.object["TreeGenConfig"] = saveconfig()

        return {'FINISHED'}
    
class TREEGEN_OT_draw(bpy.types.Operator):
    """let's the user edit the trunk"""
    bl_idname = 'object.tree_draw'
    bl_label = 'draw a new trunk'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), rotation=(0,math.pi/2,0))
        bpy.ops.transform.translate(value=(0,0,5))
        bpy.ops.transform.resize(value=(3.0, 3.0, 5.0))
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        context.object["TreeGenConfig"]='to be generated'
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

class TREEGEN_OT_regrow(bpy.types.Operator):
        """regrows tree from line of points"""
        bl_idname = 'object.tree_regrow'
        bl_label = 'regrow from existing curve'
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            tps = context.window_manager.treegen_props
            tps.ops_complete=False
            try: 
                bpy.context.object["TreeGenConfig"]
            except: 
                self.report({"INFO"}, "I can't update an object that isn't a tree")
                return {'FINISHED'}
            curve = []
            bpy.ops.object.mode_set(mode='OBJECT')
            obj = bpy.context.active_object
            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type="VERT")
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.data.vertices[0].select = True
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_linked(delimit=set())
            bpy.ops.object.mode_set(mode='OBJECT')
            curve = [v.co for v in obj.data.vertices if v.select]
            
            if curve[-1].length<curve[0].length:
                curve.reverse()
            
            curve_obj = bpy.context.active_object
            
            tps.Mlength = sum([(curve[i+1]-curve[i]).length for i in range(len(curve)-1)])
            tps.Mscale=1
            tps.Mvres = len(curve)
            m_p, br_p, bn_p, bd_p, r_p, t_p = parameters()
            seeds = [br_p[-1], bd_p[-1], r_p[-1]]

            #generates the trunk and lists of lists of stuff
            m_p[3]*=m_p[2]
            branchlist = branchinit(curve, m_p, bd_p, br_p, r_p)
            branchlist = outgrow(branchlist, br_p, bn_p, bd_p, r_p, t_p)
            verts, edges, faces, selection = toverts(branchlist, tps.facebool, m_p, br_p, t_p)
            
            #creating the tree
            mesh = bpy.data.meshes.new("tree")
            object = bpy.data.objects.new("tree", mesh)
            bpy.context.collection.objects.link(object)
            mesh.from_pydata(verts ,edges, faces)
            bpy.ops.object.select_all(action='DESELECT')
            object.select_set(True)
            bpy.context.view_layer.objects.active = object
            bpy.ops.object.shade_smooth()

            #renaming and parenting
            tree = bpy.context.active_object
            curve_obj.parent = tree
            ext=''
            if len(tree.name.split('.'))>1:
                ext = '.'+tree.name.split('.')[1]
            curve_obj.name = 'custom trunk'+ext
            for m in bpy.data.meshes: 
                if m.users==0 and m.name == str('trunk curve'+ext):
                    bpy.data.meshes.remove(m)
            curve_obj.data.name = 'trunk curve'+ext
            
            #name of the created object and selecting it
            object.matrix_world.translation = context.scene.cursor.location

            #writing properties
            br_p[-1], bd_p[-1], r_p[-1] = seeds

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
            
            context.object["TreeGenConfig"] = saveconfig()
            tps.ops_complete=True

            return {'FINISHED'}

class TREEGEN_OT_sync(bpy.types.Operator):
    """syncs tps property group with custom properties"""
    bl_idname = 'object.tree_sync'
    bl_label = 'sync tree object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try: 
            bpy.context.object["TreeGenConfig"]
        except: 
            self.report({"INFO"}, "I can't sync an object that isn't a tree")
            return {'FINISHED'}
        
        config = context.object["TreeGenConfig"]

        tps = bpy.data.window_managers["WinMan"].treegen_props
        config = [i.split('=') for i in config.split(',')]
        excluded = ['__','rna','sync']
        tps.ops_complete = False
        for old in dir(tps):
                if not any(x in old for x in excluded):
                    new = [i for i in config if old in i][0][1]
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
        tps.ops_complete = True

        return {'FINISHED'}

class TREEGEN_OT_default(bpy.types.Operator):
    """returns all values to default"""
    bl_idname = 'object.tree_default'
    bl_label = 'return to defaults'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tps = bpy.data.window_managers["WinMan"].treegen_props
        tps.treename = context.object.name
        tps.ops_complete = False
        excluded = ['__', 'rna', 'sync']
        for i in dir(tps):
            if not any(x in i for x in excluded):
                tps.property_unset(i)
        tps.ops_complete=True
        bpy.ops.object.tree_update()
        return {'FINISHED'}

class TREEGEN_OT_leaf(bpy.types.Operator):
    """handles leaves"""
    bl_idname = 'object.tree_leaf'
    bl_label = 'attach leaves'
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
    
    '''    @staticmethod
    def poll(self,context):
        tps = bpy.data.window_managers["WinMan"].treegen_props
        if tps.treename != context.object.name:
            bpy.ops.object.tree_sync()
            tps.treename = context.object.name
        return True'''

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        col = layout.column(align=True)
        tps = bpy.data.window_managers["WinMan"].treegen_props

        col.operator('object.tree_create', text = 'Create',icon='SCRIPT')
        col.operator('object.tree_sync', text = 'Sync', icon='FILE_REFRESH')
        col.operator('object.tree_default', text = 'Reset to default', icon='LOOP_BACK')
        col.separator()
        col.operator('object.tree_draw', text='draw trunk', icon = 'GREASEPENCIL')
        
        col.label(text="Main Settings")
        col.prop(wm.treegen_props, "leafbool")
        col.prop(wm.treegen_props, "facebool")
        
        col.label(text="Main Parameters")
        col.prop(wm.treegen_props, "Msides")
        col.prop(wm.treegen_props, "Mvres")
        col.prop(wm.treegen_props, "Mlength")
        col.prop(wm.treegen_props, "Mradius")
        col.prop(wm.treegen_props, "Mtipradius")

        col.label(text="Growth Parameters")
        col.prop(wm.treegen_props, "bends_amount")
        col.prop(wm.treegen_props, "bends_scale")
        col.prop(wm.treegen_props, "bends_up")
        col.prop(wm.treegen_props, "bends_weight")
        col.prop(wm.treegen_props, "bends_correction")

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

class TREEGEN_PT_createedit(bpy.types.Panel):
    """Creates a Panel in the Object properties window for tree creation"""
    bl_label = "TreeEdit"
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "Create"
    bl_context = "curve_edit"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Now edit the bezier curve.")
        col.label(text="After you finish hit regrow")
        col.label(text="I strongly recommend draw tool")
        col.operator('object.tree_regrow', text = 'Regrow',icon='SCRIPT')
    

class TREEGEN_PT_createsubpanel(TREEGEN_PT_createparent, bpy.types.Panel):
    """Creates a Panel in the Object properties window for tree creation"""
    bl_label = "Advanced"
    bl_parent_id = "TREEGEN_PT_createmain"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self,context):
        layout = self.layout
        wm = context.window_manager
        layout.prop_search(wm.treegen_props, 'leafname', context.scene, "objects")