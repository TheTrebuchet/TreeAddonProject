import bpy

def CalmTree_nodegroup_exec():
    CalmTree_nodegroup= bpy.data.node_groups.new(type = "GeometryNodeTree", name = "CalmTree_nodegroup")

    #initialize CalmTree_nodegroup nodes
    #node Instance on Points
    instance_on_points = CalmTree_nodegroup.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.location = (540.0, 200.0)
    instance_on_points.width, instance_on_points.height = 140.0, 100.0
    #Selection
    instance_on_points.inputs[1].default_value = True
    #Pick Instance
    instance_on_points.inputs[3].default_value = False
    #Instance Index
    instance_on_points.inputs[4].default_value = 0
    #Rotation
    instance_on_points.inputs[5].default_value = (0.0, 0.0, 0.0)
    #Scale
    instance_on_points.inputs[6].default_value = (0.12999999523162842, 0.12999999523162842, 0.12999999523162842)

    #CalmTree_nodegroup outputs
    CalmTree_nodegroup.outputs.new("NodeSocketGeometry", "Geometry")

    #node Group Output
    group_output = CalmTree_nodegroup.nodes.new("NodeGroupOutput")
    group_output.location = (960.0, 0.0)
    group_output.width, group_output.height = 140.0, 100.0

    #node Join Geometry
    join_geometry = CalmTree_nodegroup.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.location = (760.0, 300.0)
    join_geometry.width, join_geometry.height = 140.0, 100.0

    #node Math.004
    math_multsize = CalmTree_nodegroup.nodes.new("ShaderNodeMath")
    math_multsize.location = (-160.0, -400.0)
    math_multsize.width, math_multsize.height = 140.0, 100.0
    math_multsize.operation = 'MULTIPLY'
    math_multsize.use_clamp = False
    #Value
    math_multsize.inputs[0].default_value = 0.5
    #Value_001
    math_multsize.inputs[1].default_value = -1.0
    #Value_002
    math_multsize.inputs[2].default_value = 0.5

    #node Math
    math_multrotx = CalmTree_nodegroup.nodes.new("ShaderNodeMath")
    math_multrotx.location = (-140.0, 60.0)
    math_multrotx.width, math_multrotx.height = 140.0, 100.0
    math_multrotx.operation = 'MULTIPLY'
    math_multrotx.use_clamp = False
    #Value
    math_multrotx.inputs[0].default_value = 0.5
    #Value_001
    math_multrotx.inputs[1].default_value = 0.5
    #Value_002
    math_multrotx.inputs[2].default_value = 0.5

    #node Math.001
    math_multroty = CalmTree_nodegroup.nodes.new("ShaderNodeMath")
    math_multroty.location = (-140.0, 0.0)
    math_multroty.width, math_multroty.height = 140.0, 100.0
    math_multroty.operation = 'MULTIPLY'
    math_multroty.use_clamp = False
    #Value
    math_multroty.inputs[0].default_value = 0.5
    #Value_001
    math_multroty.inputs[1].default_value = 0.5
    #Value_002
    math_multroty.inputs[2].default_value = 0.5

    #node Random Value.001
    random_size = CalmTree_nodegroup.nodes.new("FunctionNodeRandomValue")
    random_size.location = (60.0, -440.0)
    random_size.width, random_size.height = 140.0, 100.0
    random_size.data_type = 'FLOAT'
    #Min
    random_size.inputs[0].default_value = (0.0, 0.0, 0.0)
    #Max
    random_size.inputs[1].default_value = (1.0, 1.0, 1.0)
    #Min_001
    random_size.inputs[2].default_value = 0.019999999552965164
    #Max_001
    random_size.inputs[3].default_value = 0.10000002384185791
    #Min_002
    random_size.inputs[4].default_value = 0
    #Max_002
    random_size.inputs[5].default_value = 100
    #Probability
    random_size.inputs[6].default_value = 0.5
    #ID
    random_size.inputs[7].default_value = 0
    #Seed
    random_size.inputs[8].default_value = 0

    #node Math.005
    math_addsize = CalmTree_nodegroup.nodes.new("ShaderNodeMath")
    math_addsize.location = (320.0, -440.0)
    math_addsize.width, math_addsize.height = 140.0, 100.0
    math_addsize.operation = 'ADD'
    math_addsize.use_clamp = False
    #Value
    math_addsize.inputs[0].default_value = 0.5
    #Value_001
    math_addsize.inputs[1].default_value = -1.0
    #Value_002
    math_addsize.inputs[2].default_value = 0.5

    #node Distribute Points on Faces
    distribute_points_on_faces = CalmTree_nodegroup.nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.location = (-720.0, 180.0)
    distribute_points_on_faces.width, distribute_points_on_faces.height = 170.0, 100.0
    distribute_points_on_faces.distribute_method = 'POISSON'
    #Selection
    distribute_points_on_faces.inputs[1].default_value = True
    #Distance Min
    distribute_points_on_faces.inputs[2].default_value = 0.14999999105930328
    #Density Max
    distribute_points_on_faces.inputs[3].default_value = 532.0
    #Density
    distribute_points_on_faces.inputs[4].default_value = 364.0
    #Density Factor
    distribute_points_on_faces.inputs[5].default_value = 1.0
    #Seed
    distribute_points_on_faces.inputs[6].default_value = 2

    #node Combine XYZ
    combine_xyz = CalmTree_nodegroup.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.location = (180.0, 20.0)
    combine_xyz.width, combine_xyz.height = 140.0, 100.0
    #X
    combine_xyz.inputs[0].default_value = 0.0
    #Y
    combine_xyz.inputs[1].default_value = 0.0
    #Z
    combine_xyz.inputs[2].default_value = 0.0

    #node Separate XYZ
    separate_xyz = CalmTree_nodegroup.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.location = (-500.0, 20.0)
    separate_xyz.width, separate_xyz.height = 140.0, 100.0
    #Vector
    separate_xyz.inputs[0].default_value = (0.0, 0.0, 0.0)

    #node Object Info
    object_info = CalmTree_nodegroup.nodes.new("GeometryNodeObjectInfo")
    object_info.location = (220.0, -120.0)
    object_info.width, object_info.height = 140.0, 100.0
    object_info.transform_space = 'ORIGINAL'
    #As Instance
    object_info.inputs[1].default_value = False

    #CalmTree_nodegroup inputs
    #input Mesh
    CalmTree_nodegroup.inputs.new("NodeSocketGeometry", "Mesh")

    #input Selection
    CalmTree_nodegroup.inputs.new("NodeSocketBool", "Selection")
    CalmTree_nodegroup.inputs["Selection"].default_value = True

    #input Object
    CalmTree_nodegroup.inputs.new("NodeSocketObject", "Object")

    #input Density Max
    CalmTree_nodegroup.inputs.new("NodeSocketFloat", "Density Max")
    CalmTree_nodegroup.inputs["Density Max"].default_value = 532.0
    CalmTree_nodegroup.inputs["Density Max"].min_value = 0.0
    CalmTree_nodegroup.inputs["Density Max"].max_value = 3.4028234663852886e+38

    #input Distance Min
    CalmTree_nodegroup.inputs.new("NodeSocketFloatDistance", "Distance Min")

    #input Rotation Variety
    CalmTree_nodegroup.inputs.new("NodeSocketFloat", "Rotation Variety")
    CalmTree_nodegroup.inputs["Rotation Variety"].default_value = 0.2
    CalmTree_nodegroup.inputs["Rotation Variety"].min_value = -1.0
    CalmTree_nodegroup.inputs["Rotation Variety"].max_value = 1.0

    #input Size
    CalmTree_nodegroup.inputs.new("NodeSocketFloat", "Size")
    CalmTree_nodegroup.inputs["Size"].default_value = 0.10000002384185791
    CalmTree_nodegroup.inputs["Size"].min_value = -3.4028234663852886e+38
    CalmTree_nodegroup.inputs["Size"].max_value = 3.4028234663852886e+38

    #input Size Variety
    CalmTree_nodegroup.inputs.new("NodeSocketFloat", "Size Variety")
    CalmTree_nodegroup.inputs["Size Variety"].default_value = 0.1
    CalmTree_nodegroup.inputs["Size Variety"].min_value = -3.4028234663852886e+38
    CalmTree_nodegroup.inputs["Size Variety"].max_value = 3.4028234663852886e+38

    #input Seed
    CalmTree_nodegroup.inputs.new("NodeSocketInt", "Seed")
    CalmTree_nodegroup.inputs["Seed"].default_value = 0
    CalmTree_nodegroup.inputs["Seed"].min_value = -2147483648
    CalmTree_nodegroup.inputs["Seed"].max_value = 2147483647


    #node Group Input
    group_input = CalmTree_nodegroup.nodes.new("NodeGroupInput")
    group_input.location = (-1440.0, 20.0)
    group_input.width, group_input.height = 140.0, 100.0

    #node Random Value.002
    random_roty = CalmTree_nodegroup.nodes.new("FunctionNodeRandomValue")
    random_roty.location = (-480.0, -440.0)
    random_roty.width, random_roty.height = 140.0, 100.0
    random_roty.data_type = 'FLOAT'
    #Min
    random_roty.inputs[0].default_value = (0.0, 0.0, 0.0)
    #Max
    random_roty.inputs[1].default_value = (1.0, 1.0, 1.0)
    #Min_001
    random_roty.inputs[2].default_value = -0.7199999690055847
    #Max_001
    random_roty.inputs[3].default_value = 0.699999988079071
    #Min_002
    random_roty.inputs[4].default_value = 0
    #Max_002
    random_roty.inputs[5].default_value = 100
    #Probability
    random_roty.inputs[6].default_value = 0.5
    #ID
    random_roty.inputs[7].default_value = 0
    #Seed
    random_roty.inputs[8].default_value = 1

    #node Random Value
    random_rotx = CalmTree_nodegroup.nodes.new("FunctionNodeRandomValue")
    random_rotx.location = (-500.0, -120.0)
    random_rotx.width, random_rotx.height = 140.0, 100.0
    random_rotx.data_type = 'FLOAT'
    #Min
    random_rotx.inputs[0].default_value = (0.0, 0.0, 0.0)
    #Max
    random_rotx.inputs[1].default_value = (1.0, 1.0, 1.0)
    #Min_001
    random_rotx.inputs[2].default_value = -0.7199999690055847
    #Max_001
    random_rotx.inputs[3].default_value = 0.699999988079071
    #Min_002
    random_rotx.inputs[4].default_value = 0
    #Max_002
    random_rotx.inputs[5].default_value = 100
    #Probability
    random_rotx.inputs[6].default_value = 0.5
    #ID
    random_rotx.inputs[7].default_value = 0
    #Seed
    random_rotx.inputs[8].default_value = 0

    #node Math.003
    math_multrot = CalmTree_nodegroup.nodes.new("ShaderNodeMath")
    math_multrot.location = (-740.0, -360.0)
    math_multrot.width, math_multrot.height = 140.0, 100.0
    math_multrot.operation = 'MULTIPLY'
    math_multrot.use_clamp = False
    #Value
    math_multrot.inputs[0].default_value = 0.5
    #Value_001
    math_multrot.inputs[1].default_value = -1.0
    #Value_002
    math_multrot.inputs[2].default_value = 0.5

    #node Math.002
    math_addseed = CalmTree_nodegroup.nodes.new("ShaderNodeMath")
    math_addseed.location = (-700.0, -600.0)
    math_addseed.width, math_addseed.height = 140.0, 100.0
    math_addseed.operation = 'ADD'
    math_addseed.use_clamp = False
    #Value
    math_addseed.inputs[0].default_value = 0.5
    #Value_001
    math_addseed.inputs[1].default_value = 1.0
    #Value_002
    math_addseed.inputs[2].default_value = 0.5

    #initialize CalmTree_nodegroup links
    CalmTree_nodegroup.links.new(join_geometry.outputs["Geometry"], group_output.inputs["Geometry"])
    CalmTree_nodegroup.links.new(group_input.outputs["Mesh"], distribute_points_on_faces.inputs["Mesh"])
    CalmTree_nodegroup.links.new(group_input.outputs["Mesh"], join_geometry.inputs["Geometry"])
    CalmTree_nodegroup.links.new(distribute_points_on_faces.outputs["Points"], instance_on_points.inputs["Points"])
    CalmTree_nodegroup.links.new(object_info.outputs["Geometry"], instance_on_points.inputs["Instance"])
    CalmTree_nodegroup.links.new(instance_on_points.outputs["Instances"], join_geometry.inputs["Geometry"])
    CalmTree_nodegroup.links.new(combine_xyz.outputs["Vector"], instance_on_points.inputs["Rotation"])
    CalmTree_nodegroup.links.new(distribute_points_on_faces.outputs["Rotation"], separate_xyz.inputs["Vector"])
    CalmTree_nodegroup.links.new(random_rotx.outputs[1], math_multroty.inputs[1])
    CalmTree_nodegroup.links.new(math_addsize.outputs["Value"], instance_on_points.inputs["Scale"])
    CalmTree_nodegroup.links.new(random_roty.outputs[1], math_multrotx.inputs[1])
    CalmTree_nodegroup.links.new(math_addseed.outputs["Value"], random_roty.inputs["Seed"])
    CalmTree_nodegroup.links.new(group_input.outputs["Seed"], random_rotx.inputs["Seed"])
    CalmTree_nodegroup.links.new(math_multrot.outputs["Value"], random_rotx.inputs[2])
    CalmTree_nodegroup.links.new(math_multrot.outputs["Value"], random_roty.inputs[2])
    CalmTree_nodegroup.links.new(group_input.outputs["Rotation Variety"], random_roty.inputs[3])
    CalmTree_nodegroup.links.new(group_input.outputs["Rotation Variety"], random_rotx.inputs[3])
    CalmTree_nodegroup.links.new(group_input.outputs["Rotation Variety"], math_multrot.inputs[0])
    CalmTree_nodegroup.links.new(math_multsize.outputs["Value"], random_size.inputs[2])
    CalmTree_nodegroup.links.new(group_input.outputs["Size Variety"], random_size.inputs[3])
    CalmTree_nodegroup.links.new(group_input.outputs["Size Variety"], math_multsize.inputs["Value"])
    CalmTree_nodegroup.links.new(random_size.outputs[1], math_addsize.inputs[0])
    CalmTree_nodegroup.links.new(group_input.outputs["Size"], math_addsize.inputs[1])
    CalmTree_nodegroup.links.new(separate_xyz.outputs["Y"], math_multroty.inputs[0])
    CalmTree_nodegroup.links.new(separate_xyz.outputs["X"], math_multrotx.inputs[0])
    CalmTree_nodegroup.links.new(math_multrotx.outputs["Value"], combine_xyz.inputs["X"])
    CalmTree_nodegroup.links.new(math_multroty.outputs["Value"], combine_xyz.inputs["Y"])
    CalmTree_nodegroup.links.new(separate_xyz.outputs["Z"], combine_xyz.inputs["Z"])
    CalmTree_nodegroup.links.new(group_input.outputs["Seed"], random_size.inputs["Seed"])
    CalmTree_nodegroup.links.new(group_input.outputs["Seed"], distribute_points_on_faces.inputs["Seed"])
    CalmTree_nodegroup.links.new(group_input.outputs["Object"], object_info.inputs["Object"])
    CalmTree_nodegroup.links.new(group_input.outputs["Density Max"], distribute_points_on_faces.inputs["Density Max"])
    CalmTree_nodegroup.links.new(group_input.outputs["Selection"], distribute_points_on_faces.inputs["Selection"])
    CalmTree_nodegroup.links.new(group_input.outputs["Distance Min"], distribute_points_on_faces.inputs["Distance Min"])
    CalmTree_nodegroup.links.new(group_input.outputs["Seed"], math_addseed.inputs[0])