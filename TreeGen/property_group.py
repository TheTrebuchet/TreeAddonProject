import bpy
def update_p(self, context):
    bpy.ops.object.update_tree()

class TreeGen_PG(bpy.types.PropertyGroup):
    treename: bpy.props.StringProperty(
        default='tree',
    )
    facebool: bpy.props.BoolProperty(
        name='Faces switch',
        default=True,
        update=update_p,
    )
    Msides: bpy.props.IntProperty(
        name="Number of trunk sides",
        default=11,
        min=4,
        soft_max=32,
        update=update_p
    )
    Mlength: bpy.props.FloatProperty(
        name="Trunk length",
        default=100.0,
        min=0.1,
        soft_max=200.0,
        update=update_p
    )
    Mradius: bpy.props.FloatProperty(
        name="Tree radius",
        default=4,
        min=0.1,
        soft_max=32,
        update=update_p
    )
    Mscale: bpy.props.FloatProperty(
        name="Tree scale",
        default=0.1,
        min=0.01,
        soft_max=10,
        update=update_p
    )

    Mratio: bpy.props.FloatProperty(
        name="Ratio of faces",
        default=2,
        min=0.2,
        soft_max=5,
        update=update_p
    )

    Rperlin: bpy.props.BoolProperty(
        name="turns on the jiggles",
        default=False,
    )

    Rperlin_amount: bpy.props.FloatProperty(
        name="jiggle amount",
        default=0.01,
        min=0.0,
        soft_max=1,
        update=update_p
    )

    Rperlin_scale: bpy.props.FloatProperty(
        name="jiggle scale",
        default=0.05,
        min=0.0001,
        soft_max=32,
        update=update_p
    )

    Rperlin_seed: bpy.props.IntProperty(
        name="jiggle seed",
        default=1,
        min=1,
        update=update_p
    )

    bends_type: bpy.props.IntProperty(
        name="bending type",
        default=1,
        min=1,
        max=3,
        update=update_p
    )

    bends_amount: bpy.props.FloatProperty(
        name="bending amount",
        default=0.5,
        min=0.0,
        soft_max=10,
        update=update_p
    )

    bends_angle: bpy.props.FloatProperty(
        name="Bends max angle",
        default=90,
        min=15,
        soft_max=180,
        update=update_p
    )

    bends_correction: bpy.props.FloatProperty(
        name="bending correction",
        default=0.2,
        min=0.0,
        soft_max=1,
        update=update_p
    )

    bends_weight: bpy.props.FloatProperty(
        name="branch weight",
        default=0.5,
        min=0.0,
        soft_max=1,
        update=update_p
    )

    bends_scale: bpy.props.FloatProperty(
        name="Bending scale",
        default=0.1,
        min=0.01,
        soft_max=10,
        update=update_p
    )

    bends_seed: bpy.props.IntProperty(
        name="bends seed",
        default=1,
        min = 1,
        update=update_p
    )

    branch_levels: bpy.props.IntProperty(
        name="branching levels",
        default=2,
        min=0,
        soft_max=4,
        update=update_p
    )

    branch_number1: bpy.props.IntProperty(
        name="branches number1",
        default=30,
        min=1,
        soft_max=100,
        update=update_p
    )

    branch_number2: bpy.props.IntProperty(
        name="branches number2",
        default=5,
        min=1,
        soft_max=20,
        update=update_p
    )

    branch_number3: bpy.props.IntProperty(
        name="branches number3",
        default=2,
        min=1,
        soft_max=10,
        update=update_p
    )

    branch_angle: bpy.props.FloatProperty(
        name="branching angle",
        default=70,
        min=15,
        soft_max=90,
        update=update_p
    )

    branch_height: bpy.props.FloatProperty(
        name="branching height",
        default=0.3,
        min=0.0,
        soft_max=0.9,
        update=update_p
    )

    branch_variety: bpy.props.FloatProperty(
        name="branching variety",
        default=0.1,
        min=0.0,
        soft_max=1,
        update=update_p
    )

    branch_seed: bpy.props.IntProperty(
        name="branching seed",
        default=1,
        min=1,
        update=update_p
    )
    flare_amount: bpy.props.FloatProperty(
        name="amount of tree flare",
        default=0.8,
        min=0.01,
        max=1,
        update=update_p
    )
    
