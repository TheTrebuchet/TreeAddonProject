import bpy
import math 
def tree_update(self, context):
    tps = bpy.data.window_managers['WinMan'].treegen_props
    if tps.ops_complete: 
        bpy.ops.object.tree_update()
def leaf_update(self,context):
    tps = bpy.data.window_managers['WinMan'].treegen_props
    bpy.context.object.modifiers["TreeGen"].show_viewport = tps.leafbool
    bpy.context.object.modifiers["TreeGen"].show_in_editmode = tps.leafbool
    if tps.leafbool:
        if tps.leafname =='':tps.leafname='basic_leaf'
        bpy.ops.object.tree_leaf()
        bpy.context.object.modifiers["TreeGen"]["Input_3"] = bpy.data.objects[tps.leafname]
        bpy.context.object.modifiers["TreeGen"].show_viewport = True



class TREEGEN_PG_props(bpy.types.PropertyGroup):
    ops_complete: bpy.props.BoolProperty(
        default=True,
    )
    facebool: bpy.props.BoolProperty(
        name='Faces',
        description='Switches between bark and spine',
        default=True,
        update=tree_update,
    )
    leafbool: bpy.props.BoolProperty(
        name='Leaves',
        description='Turns leaves on and off',
        default=False,
        update=leaf_update,
    )
    leafname: bpy.props.StringProperty(
        name='Leaf Object',
        description='object used to create leaves, x is width, y is length',
        default='',
        update=leaf_update
    )
    treename: bpy.props.StringProperty(
        name='Tree name',
        description='Used for updating panel',
        default='',
    )
    Msides: bpy.props.IntProperty(
        name='Trunk segments',
        description='Number of segments in the circle of the main trunk',
        default=10,
        min=4,
        soft_max=32,
        update=tree_update
    )
    Mlength: bpy.props.FloatProperty(
        name='Height',
        description='Length of the main trunk, scaled down with each branch',
        default=10.0,
        min=0.1,
        soft_max=200.0,
        update=tree_update
    )
    Mradius: bpy.props.FloatProperty(
        name='Max Radius',
        description='The radius TreeGen starts with',
        default=0.44,
        min=0.01,
        soft_max=10,
        update=tree_update
    )
    Mtipradius: bpy.props.FloatProperty(
        name='Tip Radius',
        description='The minimum radius a branch can have',
        default=0.015,
        min=0,
        max=1,
        update=tree_update
    )
    Mscale: bpy.props.FloatProperty(
        name='Object Scale',
        description='Scale applied after Tree generation',
        default=1,
        min=0.01,
        soft_max=10,
        update=tree_update
    )

    Mvres: bpy.props.IntProperty(
        name='Simulation Resolution',
        description='The number of segments along the main trunk',
        default=30,
        min=5,
        update=tree_update
    )

    Rperlin_amount: bpy.props.FloatProperty(
        name='Jiggle Amount',
        description='Simple noise used for small random jiggles of the tree curve',
        default=0.1,
        min=0.0,
        soft_max=1,
        update=tree_update
    )

    Rperlin_scale: bpy.props.FloatProperty(
        name='Jiggle Scale',
        description='Scale of the noise',
        default=1,
        min=0.0001,
        soft_max=32,
        update=tree_update
    )

    Rperlin_seed: bpy.props.IntProperty(
        name='Jiggle Seed',
        default=1,
        min=1,
        update=tree_update
    )

    bends_amount: bpy.props.FloatProperty(
        name='Bending Amount',
        description='Raise this value if you want to bend the Tree curve',
        default=0.4,
        min=0.0,
        soft_max=10,
        update=tree_update
    )

    bends_up: bpy.props.FloatProperty(
        name='Tip Bending',
        description='Tendency of the branch to grow upwards',
        default=0.3,
        min=-1.0,
        max=1.0,
        update=tree_update
    )

    bends_correction: bpy.props.FloatProperty(
        name='Correction Amount',
        description='Controls how much the tree can bend towards ground',
        default=0.5,
        min=0.0,
        soft_max=1,
        update=tree_update
    )

    bends_weight: bpy.props.FloatProperty(
        name='Weight Factor',
        description='Raise this value to weigh down heavy branches, same as it would happen naturally. If your tree falls down, it means it is too heavy, either lower weight or raise the correction amount',
        default=0.1,
        min=0.0,
        soft_max=1,
        update=tree_update
    )

    bends_scale: bpy.props.FloatProperty(
        name='Bending Scale',
        description='Scale of bending noise',
        default=0.9,
        min=0.01,
        soft_max=10,
        update=tree_update
    )

    bends_seed: bpy.props.IntProperty(
        name='Bends Seed',
        default=1,
        min = 1,
        update=tree_update
    )

    branch_levels: bpy.props.IntProperty(
        name='Levels of branches',
        description='The number of levels of branches to generate, goes up to 3',
        default=2,
        min=0,
        max=3,
        update=tree_update
    )

    branch_number1: bpy.props.IntProperty(
        name='Branch Quantity 1',
        description='Number of branches in the first level',
        default=30,
        min=1,
        soft_max=100,
        update=tree_update
    )

    branch_number2: bpy.props.IntProperty(
        name='Branch Quantity 2',
        description='Number of branches in the second level',
        default=5,
        min=1,
        soft_max=20,
        update=tree_update
    )

    branch_number3: bpy.props.IntProperty(
        name='Branch Quantity 3',
        description='Number of branches in the third level',
        default=2,
        min=1,
        soft_max=10,
        update=tree_update
    )

    branch_maxangle: bpy.props.FloatProperty(
        name='Bottom Angle',
        description='Angle at which the bottom branch grows',
        default=6/18*math.pi,
        min=0.0,
        soft_max=2*math.pi,
        unit = 'ROTATION',
        update=tree_update
    )

    branch_minangle: bpy.props.FloatProperty(
        name='Top angle',
        description='Angle at which the top branch grows',
        default=3/18*math.pi,
        min=0.0,
        soft_max=2*math.pi,
        unit = 'ROTATION',
        update=tree_update
    )

    branch_height: bpy.props.FloatProperty(
        name='Branching Height',
        description='Relative height at which branches start growing',
        default=0.3,
        min=0.0,
        soft_max=0.9,
        update=tree_update
    )

    branch_variety: bpy.props.FloatProperty(
        name='Branching Variety',
        description='Amount of variation from Main Parameters',
        default=0.1,
        min=0.0,
        soft_max=1,
        update=tree_update
    )

    branch_scaling: bpy.props.FloatProperty(
        name='Next Branch Scaling',
        description='The length of each next branch level is multiplied by this value',
        default=0.3,
        min=0.1,
        soft_max=0.9,
        update=tree_update
    )

    branch_seed: bpy.props.IntProperty(
        name='Branching seed',
        default=1,
        min=1,
        update=tree_update
    )
    branch_shift: bpy.props.FloatProperty(
        name='General Shape',
        description='Relation between the branch height and length. It can make the tree look more round or cone-shaped',
        default=0.7,
        min=0.01,
        max=1,
        update=tree_update
    )
    flare_amount: bpy.props.FloatProperty(
        name='Trunk Flare',
        description='Defines each branch\s profile. It can widen up the base or make it a perfect cone',
        default=1.0,
        min=0.01,
        max=1,
        update=tree_update
    )