import bpy

class CALMTREE_PT_createparent:
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "CalmTree"
    bl_context = "objectmode"

class CALMTREE_PT_createmain(CALMTREE_PT_createparent, bpy.types.Panel):
    """Creates a Panel for tree creation"""
    bl_label = "CalmTree Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CalmTree"
    
    '''    @staticmethod
    def poll(self,context):
        tps = bpy.data.window_managers["WinMan"].calmtree_props
        if tps.treename != context.object.name:
            bpy.ops.object.tree_sync()
            tps.treename = context.object.name
        return True'''

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        col = layout.column(align=True)
        tps = bpy.data.window_managers["WinMan"].calmtree_props

        col.operator('object.tree_create', text = 'Create',icon='SCRIPT')
        col.operator('object.tree_sync', text = 'Sync', icon='FILE_REFRESH')
        col.operator('object.tree_default', text = 'Reset to default', icon='LOOP_BACK')
        col.separator()
        col.operator('object.tree_draw', text='draw trunk', icon = 'GREASEPENCIL')
        
        
        col.label(text="Main Settings")
        col.prop(wm.calmtree_props, "leafbool")
        col.prop(wm.calmtree_props, "facebool")
        col.prop(wm.calmtree_props, "engine")
        
        col.label(text="Main Parameters")
        col.prop(wm.calmtree_props, "Msides")
        col.prop(wm.calmtree_props, "Mvres")
        col.prop(wm.calmtree_props, "Mlength")
        col.prop(wm.calmtree_props, "Mradius")
        col.prop(wm.calmtree_props, "Mtipradius")

        col.label(text="Growth Parameters")
        col.prop(wm.calmtree_props, "bends_amount")
        col.prop(wm.calmtree_props, "bends_scale")
        col.prop(wm.calmtree_props, "bends_up")
        if tps.engine=='classic':
            col.prop(wm.calmtree_props, "bends_weight")
        col.prop(wm.calmtree_props, "bends_correction")

        
        col.label(text="Branch Parameters")
        if tps.engine=='classic':
            col.prop(wm.calmtree_props, "branch_levels")
            for i in range(tps.branch_levels):
                col.prop(wm.calmtree_props, "branch_number"+str(i+1))
            col.prop(wm.calmtree_props, "branch_scaling")
            col.prop(wm.calmtree_props, "branch_minangle")
            col.prop(wm.calmtree_props, "branch_maxangle")
            col.prop(wm.calmtree_props, "branch_height")
            col.label(text="Simple Jiggle")
            col.prop(wm.calmtree_props, "Rperlin_amount")
            col.prop(wm.calmtree_props, "Rperlin_scale")
        if tps.engine=='dynamic':
            col.prop(wm.calmtree_props, 'branch_number1')
            col.prop(wm.calmtree_props, 'branch_number2')
            col.prop(wm.calmtree_props, "branch_minangle")
            col.prop(wm.calmtree_props, "branch_maxangle")
            col.prop(wm.calmtree_props, "branch_height")
            col.prop(wm.calmtree_props, "Ythreshold")
            col.prop(wm.calmtree_props, "Tthreshold")
            col.prop(wm.calmtree_props, "leaffactor")
        col.label(text="Seeds and Variety")
        col.prop(wm.calmtree_props, "Rperlin_seed")
        col.prop(wm.calmtree_props, "bends_seed")
        col.prop(wm.calmtree_props, "branch_seed")
        col.prop(wm.calmtree_props, "branch_variety")
        col.label(text="Scale and Shape")
        col.prop(wm.calmtree_props, "Mscale")
        col.prop(wm.calmtree_props, 'flare_amount')
        col.prop(wm.calmtree_props, 'branch_shift')

class CALMTREE_PT_createedit(bpy.types.Panel):
    """Creates a Panel for tree creation"""
    bl_label = "TreeEdit"
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "CalmTree"
    bl_context = "curve_edit"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Now edit the bezier curve.")
        col.label(text="After you finish hit regrow")
        col.label(text="I strongly recommend draw tool")
        col.operator('object.tree_regrow', text = 'Regrow',icon='SCRIPT')
    

class CALMTREE_PT_createexperimental(CALMTREE_PT_createparent, bpy.types.Panel):
    """Creates a Panel for tree creation"""
    bl_label = "Experimental"
    bl_parent_id = "CALMTREE_PT_createmain"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self,context):
        layout = self.layout
        wm = context.window_manager
        col = layout.column(align=True)
        

class CALMTREE_PT_createadvanced(CALMTREE_PT_createparent, bpy.types.Panel):
    """Creates a Panel for tree creation"""
    bl_label = "Advanced"
    bl_parent_id = "CALMTREE_PT_createmain"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self,context):
        layout = self.layout
        wm = context.window_manager
        tps = bpy.data.window_managers["WinMan"].calmtree_props

        col = layout.column(align=True)
        col.prop(wm.calmtree_props, "interp")
        col.prop(wm.calmtree_props, "branch_horizontal")
        col.label(text="Branch generation")
        col.prop(wm.calmtree_props, "poisson_type")
        if tps.poisson_type=='fancy':
            col.prop(wm.calmtree_props, "poisson_qual")

class CALMTREE_PT_materialsparent:
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "CalmTree"
    bl_context = "objectmode"

class CALMTREE_PT_materialsmain(CALMTREE_PT_materialsparent, bpy.types.Panel):
    """Creates a Panel for tree creation"""
    bl_label = "CalmTree Materials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CalmTree"
    
    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        tps = bpy.data.window_managers["WinMan"].calmtree_props
        col = layout.column(align=True)
        col.label(text="UV Tools")
        col.operator('object.tree_uv', text='UV from Camera', icon = 'UV')
        layout.prop(wm.calmtree_props, 'leafchoice')
        if tps.leafchoice == 'custom':            
            col.label(text="head over to geogroup tab!")
        col.prop(wm.calmtree_props, "matbool")