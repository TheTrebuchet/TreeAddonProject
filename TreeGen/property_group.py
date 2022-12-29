import bpy
def update_p(self, context):
    tps = bpy.data.window_managers["WinMan"].treegen_props
    if tps.sync_complete:
        bpy.ops.object.tree_update()

class TreeGen_PG(bpy.types.PropertyGroup):
    sync_complete: bpy.props.BoolProperty(
        default=True,
    )
    facebool: bpy.props.BoolProperty(
        name='Faces Switch',
        default=True,
        update=update_p,
    )
    Msides: bpy.props.IntProperty(
        name="Number of Trunk Sides",
        default=11,
        min=4,
        soft_max=32,
        update=update_p
    )
    Mlength: bpy.props.FloatProperty(
        name="Height",
        default=100.0,
        min=0.1,
        soft_max=200.0,
        update=update_p
    )
    Mradius: bpy.props.FloatProperty(
        name="Base Radius",
        default=4,
        min=0.1,
        soft_max=32,
        update=update_p
    )
    Mtipradius: bpy.props.FloatProperty(
        name="Tip Radius",
        default=0.01,
        min=0,
        max=1,
        update=update_p
    )
    Mscale: bpy.props.FloatProperty(
        name="Object Scale",
        default=0.1,
        min=0.01,
        soft_max=10,
        update=update_p
    )

    Mratio: bpy.props.FloatProperty(
        name="Ratio of Faces",
        default=2,
        min=0.2,
        soft_max=5,
        update=update_p
    )

    Rperlin_amount: bpy.props.FloatProperty(
        name="Jiggle Amount",
        default=0.01,
        min=0.0,
        soft_max=1,
        update=update_p
    )

    Rperlin_scale: bpy.props.FloatProperty(
        name="Jiggle Scale",
        default=0.2,
        min=0.0001,
        soft_max=32,
        update=update_p
    )

    Rperlin_seed: bpy.props.IntProperty(
        name="Jiggle Seed",
        default=1,
        min=1,
        update=update_p
    )

    bends_type: bpy.props.IntProperty(
        name="Bending Type",
        default=1,
        min=1,
        max=3,
        update=update_p
    )

    bends_amount: bpy.props.FloatProperty(
        name="Bending Amount",
        default=0.5,
        min=0.0,
        soft_max=10,
        update=update_p
    )

    bends_up: bpy.props.FloatProperty(
        name="Angle Influence",
        default=0.0,
        min=-1.0,
        max=1.0,
        update=update_p
    )

    bends_correction: bpy.props.FloatProperty(
        name="Correction Amount",
        default=0.2,
        min=0.0,
        soft_max=1,
        update=update_p
    )

    bends_weight: bpy.props.FloatProperty(
        name="Weight Factor",
        default=0.5,
        min=0.0,
        soft_max=1,
        update=update_p
    )

    bends_scale: bpy.props.FloatProperty(
        name="Bending Scale",
        default=0.1,
        min=0.01,
        soft_max=10,
        update=update_p
    )

    bends_seed: bpy.props.IntProperty(
        name="Bends Seed",
        default=1,
        min = 1,
        update=update_p
    )

    branch_levels: bpy.props.IntProperty(
        name="Branching Levels",
        default=2,
        min=0,
        soft_max=4,
        update=update_p
    )

    branch_number1: bpy.props.IntProperty(
        name="Branch Quantity 1",
        default=30,
        min=1,
        soft_max=100,
        update=update_p
    )

    branch_number2: bpy.props.IntProperty(
        name="Branch Quantity 2",
        default=5,
        min=1,
        soft_max=20,
        update=update_p
    )

    branch_number3: bpy.props.IntProperty(
        name="Branch Quantity 3",
        default=2,
        min=1,
        soft_max=10,
        update=update_p
    )

    branch_maxangle: bpy.props.FloatProperty(
        name="Tip's Angle",
        default=70.0,
        min=0.0,
        soft_max=180.0,
        update=update_p
    )

    branch_minangle: bpy.props.FloatProperty(
        name="Bottom angle",
        default=0.0,
        min=0.0,
        soft_max=180.0,
        update=update_p
    )

    branch_height: bpy.props.FloatProperty(
        name="Branching Height",
        default=0.3,
        min=0.0,
        soft_max=0.9,
        update=update_p
    )

    branch_variety: bpy.props.FloatProperty(
        name="Branching Variety",
        default=0.1,
        min=0.0,
        soft_max=1,
        update=update_p
    )

    branch_scaling: bpy.props.FloatProperty(
        name="Subsequent Branch Scale",
        default=0.4,
        min=0.1,
        soft_max=0.9,
        update=update_p
    )

    branch_seed: bpy.props.IntProperty(
        name="Branching seed",
        default=1,
        min=1,
        update=update_p
    )
    branch_shift: bpy.props.FloatProperty(
        name="General Shape",
        default=0.6,
        min=0.01,
        max=1,
        update=update_p
    )
    flare_amount: bpy.props.FloatProperty(
        name="Trunk Flare",
        default=0.8,
        min=0.01,
        max=1,
        update=update_p
    )