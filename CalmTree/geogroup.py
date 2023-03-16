import bpy

def CalmTree_nodegroup_exec():
    calmtree_nodegroup= bpy.data.node_groups.new(type = "GeometryNodeTree", name = "CalmTree_nodegroup")

    #initialize calmtree_nodegroup nodes
    #calmtree_nodegroup inputs
    #input Mesh
    calmtree_nodegroup.inputs.new("NodeSocketGeometry", "Mesh")

    #input Selection
    calmtree_nodegroup.inputs.new("NodeSocketBool", "Selection")
    calmtree_nodegroup.inputs[1].default_value = True

    #input Object
    calmtree_nodegroup.inputs.new("NodeSocketObject", "Object")

    #input Density Max
    calmtree_nodegroup.inputs.new("NodeSocketFloat", "Density Max")
    calmtree_nodegroup.inputs[3].default_value = 532.0
    calmtree_nodegroup.inputs[3].min_value = 0.0
    calmtree_nodegroup.inputs[3].max_value = 3.4028234663852886e+38

    #input Distance Min
    calmtree_nodegroup.inputs.new("NodeSocketFloatDistance", "Distance Min")
    calmtree_nodegroup.inputs[4].default_value = 0.1
    calmtree_nodegroup.inputs[4].min_value = 0.0
    calmtree_nodegroup.inputs[4].max_value = 100

    #input Rotation Variety
    calmtree_nodegroup.inputs.new("NodeSocketFloat", "Rotation Variety")
    calmtree_nodegroup.inputs[5].default_value = 0.20000000298023224
    calmtree_nodegroup.inputs[5].min_value = 0.0
    calmtree_nodegroup.inputs[5].max_value = 3.14

    #input Size
    calmtree_nodegroup.inputs.new("NodeSocketFloat", "Size")
    calmtree_nodegroup.inputs[6].default_value = 1.0
    calmtree_nodegroup.inputs[6].min_value = 0.0
    calmtree_nodegroup.inputs[6].max_value = 3.4028234663852886e+38

    #input Size Variety
    calmtree_nodegroup.inputs.new("NodeSocketFloat", "Size Variety")
    calmtree_nodegroup.inputs[7].default_value = 0.10000000149011612
    calmtree_nodegroup.inputs[7].min_value = 0.0
    calmtree_nodegroup.inputs[7].max_value = 3.4028234663852886e+38

    #input Seed
    calmtree_nodegroup.inputs.new("NodeSocketInt", "Seed")
    calmtree_nodegroup.inputs[8].default_value = 0
    calmtree_nodegroup.inputs[8].min_value = -2147483648
    calmtree_nodegroup.inputs[8].max_value = 2147483647


    #node Group Input
    group_input = calmtree_nodegroup.nodes.new("NodeGroupInput")

    #node Random Value.002
    random_value_002 = calmtree_nodegroup.nodes.new("FunctionNodeRandomValue")
    random_value_002.data_type = 'FLOAT'
    #Min
    random_value_002.inputs[0].default_value = (0.0, 0.0, 0.0)
    #Max
    random_value_002.inputs[1].default_value = (1.0, 1.0, 1.0)
    #Min_001
    random_value_002.inputs[2].default_value = -1.0
    #Max_001
    random_value_002.inputs[3].default_value = 1.0
    #Min_002
    random_value_002.inputs[4].default_value = 0
    #Max_002
    random_value_002.inputs[5].default_value = 100
    #Probability
    random_value_002.inputs[6].default_value = 0.5
    #ID
    random_value_002.inputs[7].default_value = 0
    #Seed
    random_value_002.inputs[8].default_value = 2

    #node Random Value.001
    random_value_001 = calmtree_nodegroup.nodes.new("FunctionNodeRandomValue")
    random_value_001.data_type = 'FLOAT'
    #Min
    random_value_001.inputs[0].default_value = (0.0, 0.0, 0.0)
    #Max
    random_value_001.inputs[1].default_value = (1.0, 1.0, 1.0)
    #Min_001
    random_value_001.inputs[2].default_value = -1.0
    #Max_001
    random_value_001.inputs[3].default_value = 1.0
    #Min_002
    random_value_001.inputs[4].default_value = 0
    #Max_002
    random_value_001.inputs[5].default_value = 100
    #Probability
    random_value_001.inputs[6].default_value = 0.5
    #ID
    random_value_001.inputs[7].default_value = 0
    #Seed
    random_value_001.inputs[8].default_value = 1

    #node Random Value
    random_value = calmtree_nodegroup.nodes.new("FunctionNodeRandomValue")
    random_value.data_type = 'FLOAT'
    #Min
    random_value.inputs[0].default_value = (0.0, 0.0, 0.0)
    #Max
    random_value.inputs[1].default_value = (1.0, 1.0, 1.0)
    #Min_001
    random_value.inputs[2].default_value = -1.0
    #Max_001
    random_value.inputs[3].default_value = 1.0
    #Min_002
    random_value.inputs[4].default_value = 0
    #Max_002
    random_value.inputs[5].default_value = 100
    #Probability
    random_value.inputs[6].default_value = 0.5
    #ID
    random_value.inputs[7].default_value = 0
    #Seed
    random_value.inputs[8].default_value = 0

    #node Math.002
    math_002 = calmtree_nodegroup.nodes.new("ShaderNodeMath")
    math_002.operation = 'MULTIPLY'
    #Value_002
    math_002.inputs[2].default_value = 0.5

    #node Math.001
    math_001 = calmtree_nodegroup.nodes.new("ShaderNodeMath")
    math_001.operation = 'MULTIPLY'
    #Value_002
    math_001.inputs[2].default_value = 0.5

    #node Math
    math = calmtree_nodegroup.nodes.new("ShaderNodeMath")
    math.operation = 'MULTIPLY'
    #Value_002
    math.inputs[2].default_value = 0.5

    #node Math.004
    math_004 = calmtree_nodegroup.nodes.new("ShaderNodeMath")
    math_004.operation = 'ADD'
    #Value_001
    math_004.inputs[1].default_value = 1.0
    #Value_002
    math_004.inputs[2].default_value = 0.5

    #node Math.003
    math_003 = calmtree_nodegroup.nodes.new("ShaderNodeMath")
    math_003.operation = 'MULTIPLY'
    #Value_002
    math_003.inputs[2].default_value = 0.5

    #node Combine XYZ.001
    combine_xyz_001 = calmtree_nodegroup.nodes.new("ShaderNodeCombineXYZ")
    #Z
    combine_xyz_001.inputs[2].default_value = 0.0

    #node Distribute Points on Faces
    distribute_points_on_faces = calmtree_nodegroup.nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.distribute_method = 'POISSON'
    #Density
    distribute_points_on_faces.inputs[4].default_value = 364.0
    #Density Factor
    distribute_points_on_faces.inputs[5].default_value = 1.0

    #node Vector Math.001
    vector_math_001 = calmtree_nodegroup.nodes.new("ShaderNodeVectorMath")
    vector_math_001.operation = 'MULTIPLY_ADD'
    #Vector_001
    vector_math_001.inputs[1].default_value = (0.0, 1.0, 1.0)
    #Scale
    vector_math_001.inputs[3].default_value = 1.0

    #node Join Geometry
    join_geometry = calmtree_nodegroup.nodes.new("GeometryNodeJoinGeometry")

    #node Object Info
    object_info = calmtree_nodegroup.nodes.new("GeometryNodeObjectInfo")
    object_info.transform_space = 'ORIGINAL'
    #As Instance
    object_info.inputs[1].default_value = False

    #node Instance on Points
    instance_on_points = calmtree_nodegroup.nodes.new("GeometryNodeInstanceOnPoints")
    #Selection
    instance_on_points.inputs[1].default_value = True
    #Pick Instance
    instance_on_points.inputs[3].default_value = False
    #Instance Index
    instance_on_points.inputs[4].default_value = 0

    #calmtree_nodegroup outputs
    calmtree_nodegroup.outputs.new("NodeSocketGeometry", "Geometry")
    calmtree_nodegroup.outputs[0].attribute_domain = 'POINT'

    #node Group Output
    group_output = calmtree_nodegroup.nodes.new("NodeGroupOutput")

    #node Reroute.005
    reroute_005 = calmtree_nodegroup.nodes.new("NodeReroute")
    #node Reroute.012
    reroute_012 = calmtree_nodegroup.nodes.new("NodeReroute")
    #node Reroute.013
    reroute_013 = calmtree_nodegroup.nodes.new("NodeReroute")
    #node Reroute
    reroute = calmtree_nodegroup.nodes.new("NodeReroute")
    #Set parents

    #Set locations
    group_input.location = (-817.0, 416.5)
    random_value_002.location = (-817.0, -243.5)
    random_value_001.location = (-817.0, -48.5)
    random_value.location = (-817.0, 146.5)
    math_002.location = (-573.0, -11.5)
    math_001.location = (-573.0, 164.5)
    math.location = (-573.0, 340.5)
    math_004.location = (-329.0, -43.5)
    math_003.location = (-55.0, -33.5)
    combine_xyz_001.location = (-329.0, 97.5)
    distribute_points_on_faces.location = (-329.0, 378.5)
    vector_math_001.location = (-55.0, 201.5)
    join_geometry.location = (433.0, 416.5)
    object_info.location = (-55.0, 416.5)
    instance_on_points.location = (189.0, 378.5)
    group_output.location = (677.0, 416.5)
    reroute_005.location = (-573.0, 416.5)
    reroute_012.location = (189.0, 416.5)
    reroute_013.location = (-329.0, 416.5)
    reroute.location = (-573.0, 378.5)

    #sSet dimensions
    group_input.width, group_input.height = 140.0, 100.0
    random_value_002.width, random_value_002.height = 140.0, 100.0
    random_value_001.width, random_value_001.height = 140.0, 100.0
    random_value.width, random_value.height = 140.0, 100.0
    math_002.width, math_002.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    math_004.width, math_004.height = 140.0, 100.0
    math_003.width, math_003.height = 140.0, 100.0
    combine_xyz_001.width, combine_xyz_001.height = 140.0, 100.0
    distribute_points_on_faces.width, distribute_points_on_faces.height = 170.0, 100.0
    vector_math_001.width, vector_math_001.height = 140.0, 100.0
    join_geometry.width, join_geometry.height = 140.0, 100.0
    object_info.width, object_info.height = 140.0, 100.0
    instance_on_points.width, instance_on_points.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    reroute_005.width, reroute_005.height = 16.0, 100.0
    reroute_012.width, reroute_012.height = 16.0, 100.0
    reroute_013.width, reroute_013.height = 16.0, 100.0
    reroute.width, reroute.height = 16.0, 100.0

    #initialize calmtree_nodegroup links
    #join_geometry.Geometry -> group_output.Geometry
    calmtree_nodegroup.links.new(join_geometry.outputs[0], group_output.inputs[0])
    #reroute.Output -> distribute_points_on_faces.Mesh
    calmtree_nodegroup.links.new(reroute.outputs[0], distribute_points_on_faces.inputs[0])
    #reroute_012.Output -> join_geometry.Geometry
    calmtree_nodegroup.links.new(reroute_012.outputs[0], join_geometry.inputs[0])
    #distribute_points_on_faces.Points -> instance_on_points.Points
    calmtree_nodegroup.links.new(distribute_points_on_faces.outputs[0], instance_on_points.inputs[0])
    #object_info.Geometry -> instance_on_points.Instance
    calmtree_nodegroup.links.new(object_info.outputs[3], instance_on_points.inputs[2])
    #instance_on_points.Instances -> join_geometry.Geometry
    calmtree_nodegroup.links.new(instance_on_points.outputs[0], join_geometry.inputs[0])
    #group_input.Density Max -> distribute_points_on_faces.Density Max
    calmtree_nodegroup.links.new(group_input.outputs[3], distribute_points_on_faces.inputs[3])
    #group_input.Selection -> distribute_points_on_faces.Selection
    calmtree_nodegroup.links.new(group_input.outputs[1], distribute_points_on_faces.inputs[1])
    #group_input.Distance Min -> distribute_points_on_faces.Distance Min
    calmtree_nodegroup.links.new(group_input.outputs[4], distribute_points_on_faces.inputs[2])
    #reroute_013.Output -> object_info.Object
    calmtree_nodegroup.links.new(reroute_013.outputs[0], object_info.inputs[0])
    #distribute_points_on_faces.Rotation -> vector_math_001.Vector
    calmtree_nodegroup.links.new(distribute_points_on_faces.outputs[2], vector_math_001.inputs[0])
    #vector_math_001.Vector -> instance_on_points.Rotation
    calmtree_nodegroup.links.new(vector_math_001.outputs[0], instance_on_points.inputs[5])
    #combine_xyz_001.Vector -> vector_math_001.Vector
    calmtree_nodegroup.links.new(combine_xyz_001.outputs[0], vector_math_001.inputs[2])
    #random_value.Value -> math.Value
    calmtree_nodegroup.links.new(random_value.outputs[1], math.inputs[0])
    #math.Value -> combine_xyz_001.X
    calmtree_nodegroup.links.new(math.outputs[0], combine_xyz_001.inputs[0])
    #math_001.Value -> combine_xyz_001.Y
    calmtree_nodegroup.links.new(math_001.outputs[0], combine_xyz_001.inputs[1])
    #group_input.Seed -> distribute_points_on_faces.Seed
    calmtree_nodegroup.links.new(group_input.outputs[8], distribute_points_on_faces.inputs[6])
    #group_input.Rotation Variety -> math.Value
    calmtree_nodegroup.links.new(group_input.outputs[5], math.inputs[1])
    #group_input.Rotation Variety -> math_001.Value
    calmtree_nodegroup.links.new(group_input.outputs[5], math_001.inputs[0])
    #random_value_001.Value -> math_001.Value
    calmtree_nodegroup.links.new(random_value_001.outputs[1], math_001.inputs[1])
    #random_value_002.Value -> math_002.Value
    calmtree_nodegroup.links.new(random_value_002.outputs[1], math_002.inputs[1])
    #math_003.Value -> instance_on_points.Scale
    calmtree_nodegroup.links.new(math_003.outputs[0], instance_on_points.inputs[6])
    #math_004.Value -> math_003.Value
    calmtree_nodegroup.links.new(math_004.outputs[0], math_003.inputs[1])
    #math_002.Value -> math_004.Value
    calmtree_nodegroup.links.new(math_002.outputs[0], math_004.inputs[0])
    #group_input.Size Variety -> math_002.Value
    calmtree_nodegroup.links.new(group_input.outputs[7], math_002.inputs[0])
    #group_input.Size -> math_003.Value
    calmtree_nodegroup.links.new(group_input.outputs[6], math_003.inputs[0])
    #group_input.Mesh -> reroute.Input
    calmtree_nodegroup.links.new(group_input.outputs[0], reroute.inputs[0])
    #group_input.Object -> reroute_005.Input
    calmtree_nodegroup.links.new(group_input.outputs[2], reroute_005.inputs[0])
    #reroute.Output -> reroute_012.Input
    calmtree_nodegroup.links.new(reroute.outputs[0], reroute_012.inputs[0])
    #reroute_005.Output -> reroute_013.Input
    calmtree_nodegroup.links.new(reroute_005.outputs[0], reroute_013.inputs[0])