import bpy
class TreeGen_props(bpy.types.PropertyGroups):
    Msides: bpy.types.IntProperty(
        name="Number of trunk sides",
        default=10,
        min=4,
        soft_max=32
    )
    Mlength: bpy.types.FloatProperty(
        name="Trunk length",
        default=100.0,
        min=0.1,
        soft_max=200.0
    )
    Mradius: bpy.types.FloatProperty(
        name="Tree radius",
        default=4,
        min=0.1,
        soft_max=32
    )
    Mscale: bpy.types.FloatProperty(
        name="Tree scale",
        default=0.1,
        min=0.01,
        soft_max=10
    )

    Mratio: bpy.types.FloatProperty(
        name="Ratio of faces",
        default=2,
        min=0.2,
        soft_max=5
    )

    Rperlin: bpy.types.BoolProperty(
        name="turns on the jiggles",
        default=False,
    )

    Rperlin_amount: bpy.types.FloatProperty(
        name="jiggle amount",
        default=0.01,
        min=0.0,
        soft_max=1
    )

    Rperlin_scale: bpy.types.FloatProperty(
        name="jiggle scale",
        default=0.05,
        min=4,
        soft_max=32
    )

    Rperlin_seed: bpy.types.IntProperty(
        name="jiggle seed",
        default=1,
        min=1,
    )

    Rbends_amount: bpy.types.FloatProperty(
        name="bending amount",
        default=0.5,
        min=0.0,
        soft_max=10
    )

    Rbends_angle: bpy.types.FloatProperty(
        name="Bends max angle",
        default=90,
        min=15,
        soft_max=120
    )

    Rbends_correction: bpy.types.FloatProperty(
        name="bending correction",
        default=0.2,
        min=0.0,
        soft_max=1
    )

    Rbends_scale: bpy.types.FloatProperty(
        name="Bending scale",
        default=0.1,
        min=0.01,
        soft_max=10
    )

    Rbends_seed: bpy.types.IntProperty(
        name="bends seed",
        default=1,
        min = 1
    )

    branch_levels: bpy.types.IntProperty(
        name="branching levels",
        default=2,
        min=1,
        soft_max=4
    )

    branch_number1: bpy.types.IntProperty(
        name="branches number1",
        default=30,
        min=1,
        soft_max=100
    )

    branch_number2: bpy.types.IntProperty(
        name="branches number2",
        default=5,
        min=1,
        soft_max=20
    )

    branch_number3: bpy.types.IntProperty(
        name="branches number3",
        default=2,
        min=1,
        soft_max=10
    )

    branch_angle: bpy.types.FloatProperty(
        name="branching angle",
        default=70,
        min=15,
        soft_max=90
    )

    branch_height: bpy.types.FloatProperty(
        name="branching height",
        default=0.3,
        min=0.0,
        soft_max=0.9
    )

    branch_weight: bpy.types.FloatProperty(
        name="branch weight",
        default=0.5,
        min=0.0,
        soft_max=1
    )

    branch_variety: bpy.types.FloatProperty(
        name="branching variety",
        default=0.1,
        min=0.0,
        soft_max=1
    )

    branch_seed: bpy.types.IntProperty(
        name="branching seed",
        default=1,
        min=1,
    )