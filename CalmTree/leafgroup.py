import bpy

mat = bpy.data.materials.new(name = "basic")
mat.use_nodes = True
#initialize basic node group
def basic_node_group():
    basic = mat.node_tree
    #start with a clean node tree
    for node in basic.nodes:
        basic.nodes.remove(node)
    #initialize basic nodes
    #node Material Output
    material_output = basic.nodes.new("ShaderNodeOutputMaterial")
    material_output.target = 'ALL'
    #Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Thickness
    material_output.inputs[3].default_value = 0.0

    #initialize leafnode node group
    def leafnode_node_group():
        leafnode= bpy.data.node_groups.new(type = "ShaderNodeTree", name = "leafnode")

        #initialize leafnode nodes
        #node Reroute.001
        reroute_001 = leafnode.nodes.new("NodeReroute")
        #node Bright/Contrast
        bright_contrast = leafnode.nodes.new("ShaderNodeBrightContrast")
        #Bright
        bright_contrast.inputs[1].default_value = 0.25
        #Contrast
        bright_contrast.inputs[2].default_value = 0.0

        #node Mapping
        mapping = leafnode.nodes.new("ShaderNodeMapping")
        mapping.vector_type = 'POINT'
        #Location
        mapping.inputs[1].default_value = (0.0, 0.0, 0.0)
        #Scale
        mapping.inputs[3].default_value = (1.0, 1.0, 1.0)

        #node Math.004
        math_004 = leafnode.nodes.new("ShaderNodeMath")
        math_004.operation = 'GREATER_THAN'
        #Value_002
        math_004.inputs[2].default_value = 0.5

        #node Separate XYZ.001
        separate_xyz_001 = leafnode.nodes.new("ShaderNodeSeparateXYZ")

        #node Group Input
        group_input = leafnode.nodes.new("NodeGroupInput")

        #node Separate XYZ
        separate_xyz = leafnode.nodes.new("ShaderNodeSeparateXYZ")

        #node Math.001
        math_001 = leafnode.nodes.new("ShaderNodeMath")
        math_001.operation = 'SIGN'
        #Value_001
        math_001.inputs[1].default_value = 0.5
        #Value_002
        math_001.inputs[2].default_value = 0.5

        #node Combine XYZ
        combine_xyz = leafnode.nodes.new("ShaderNodeCombineXYZ")
        #X
        combine_xyz.inputs[0].default_value = 0.0
        #Y
        combine_xyz.inputs[1].default_value = 0.0

        #node Math.002
        math_002 = leafnode.nodes.new("ShaderNodeMath")
        math_002.operation = 'MULTIPLY'
        #Value_002
        math_002.inputs[2].default_value = 0.5

        #node Group Output
        group_output = leafnode.nodes.new("NodeGroupOutput")

        #node Translucent BSDF
        translucent_bsdf = leafnode.nodes.new("ShaderNodeBsdfTranslucent")
        #Normal
        translucent_bsdf.inputs[1].default_value = (0.0, 0.0, 0.0)
        #Weight
        translucent_bsdf.inputs[2].default_value = 0.0

        #node Mix Shader
        mix_shader = leafnode.nodes.new("ShaderNodeMixShader")
        #Fac
        mix_shader.inputs[0].default_value = 0.699999988079071

        #node Mix
        mix = leafnode.nodes.new("ShaderNodeMix")
        mix.data_type = 'RGBA'
        mix.clamp_factor = True
        mix.factor_mode = 'UNIFORM'
        mix.blend_type = 'MIX'
        #Factor_Vector
        mix.inputs[1].default_value = (0.5, 0.5, 0.5)
        #A_Float
        mix.inputs[2].default_value = 0.0
        #B_Float
        mix.inputs[3].default_value = 0.0
        #A_Vector
        mix.inputs[4].default_value = (0.0, 0.0, 0.0)
        #B_Vector
        mix.inputs[5].default_value = (0.0, 0.0, 0.0)

        #node Math.003
        math_003 = leafnode.nodes.new("ShaderNodeMath")
        math_003.operation = 'MULTIPLY'
        #Value_002
        math_003.inputs[2].default_value = 0.5

        #node Math
        math = leafnode.nodes.new("ShaderNodeMath")
        math.operation = 'MULTIPLY'
        #Value_001
        math.inputs[1].default_value = 0.14000001549720764
        #Value_002
        math.inputs[2].default_value = 0.5

        #node Math.005
        math_005 = leafnode.nodes.new("ShaderNodeMath")
        math_005.operation = 'GREATER_THAN'
        #Value_002
        math_005.inputs[2].default_value = 0.5

        #node Math.006
        math_006 = leafnode.nodes.new("ShaderNodeMath")
        math_006.operation = 'MULTIPLY'
        #Value_002
        math_006.inputs[2].default_value = 0.5

        #node Diffuse BSDF
        diffuse_bsdf = leafnode.nodes.new("ShaderNodeBsdfDiffuse")
        #Roughness
        diffuse_bsdf.inputs[1].default_value = 0.0
        #Normal
        diffuse_bsdf.inputs[2].default_value = (0.0, 0.0, 0.0)
        #Weight
        diffuse_bsdf.inputs[3].default_value = 0.0

        #node Reroute
        reroute = leafnode.nodes.new("NodeReroute")
        #node Reroute.003
        reroute_003 = leafnode.nodes.new("NodeReroute")
        #node Reroute.002
        reroute_002 = leafnode.nodes.new("NodeReroute")
        #node Wave Texture.001
        wave_texture_001 = leafnode.nodes.new("ShaderNodeTexWave")
        wave_texture_001.wave_type = 'BANDS'
        wave_texture_001.rings_direction = 'X'
        wave_texture_001.wave_profile = 'SIN'
        #Scale
        wave_texture_001.inputs[1].default_value = 31.1299991607666
        #Distortion
        wave_texture_001.inputs[2].default_value = 0.0
        #Detail
        wave_texture_001.inputs[3].default_value = 2.0
        #Detail Scale
        wave_texture_001.inputs[4].default_value = 1.0
        #Detail Roughness
        wave_texture_001.inputs[5].default_value = 0.5
        #Phase Offset
        wave_texture_001.inputs[6].default_value = 0.0

        #node Voronoi Texture
        voronoi_texture = leafnode.nodes.new("ShaderNodeTexVoronoi")
        voronoi_texture.voronoi_dimensions = '3D'
        voronoi_texture.feature = 'DISTANCE_TO_EDGE'
        voronoi_texture.distance = 'EUCLIDEAN'
        #W
        voronoi_texture.inputs[1].default_value = 0.0
        #Scale
        voronoi_texture.inputs[2].default_value = 540.89990234375
        #Smoothness
        voronoi_texture.inputs[3].default_value = 1.0
        #Exponent
        voronoi_texture.inputs[4].default_value = 0.5
        #Randomness
        voronoi_texture.inputs[5].default_value = 0.8475000858306885

        #node Math.007
        math_007 = leafnode.nodes.new("ShaderNodeMath")
        math_007.operation = 'GREATER_THAN'
        #Value_001
        math_007.inputs[1].default_value = 0.030000030994415283
        #Value_002
        math_007.inputs[2].default_value = 0.5

        #node Vector Math
        vector_math = leafnode.nodes.new("ShaderNodeVectorMath")
        vector_math.operation = 'DISTANCE'
        #Vector_001
        vector_math.inputs[1].default_value = (0.0, 0.0, 0.0)
        #Vector_002
        vector_math.inputs[2].default_value = (0.0, 0.0, 0.0)
        #Scale
        vector_math.inputs[3].default_value = 1.0

        #node Reroute.004
        reroute_004 = leafnode.nodes.new("NodeReroute")
        #node Reroute.005
        reroute_005 = leafnode.nodes.new("NodeReroute")
        #node Texture Coordinate.001
        texture_coordinate_001 = leafnode.nodes.new("ShaderNodeTexCoord")

        #Set parents

        #Set locations
        reroute_001.location = (-340.0, 780.0)
        bright_contrast.location = (260.0, 560.0)
        mapping.location = (-140.0, 1120.0)
        math_004.location = (240.0, 1060.0)
        separate_xyz_001.location = (-220.0, 560.0)
        group_input.location = (-1340.0, 600.0)
        separate_xyz.location = (-895.0, 866.75)
        math_001.location = (-705.0, 873.25)
        combine_xyz.location = (-325.0, 866.75)
        math_002.location = (-515.0, 884.25)
        group_output.location = (1760.0, 820.0)
        translucent_bsdf.location = (1380.0, 820.0)
        mix_shader.location = (1560.0, 820.0)
        mix.location = (1180.0, 880.0)
        math_003.location = (1000.0, 840.0)
        math.location = (-100.0, 840.0)
        math_005.location = (560.0, 840.0)
        math_006.location = (800.0, 840.0)
        diffuse_bsdf.location = (1380.0, 960.0)
        reroute.location = (-280.0, 1140.0)
        reroute_003.location = (-40.0, 280.0)
        reroute_002.location = (-960.0, 280.0)
        wave_texture_001.location = (40.0, 1140.0)
        voronoi_texture.location = (-140.0, 1340.0)
        math_007.location = (60.0, 1340.0)
        vector_math.location = (-40.0, 600.0)
        reroute_004.location = (-1020.0, 1080.0)
        reroute_005.location = (-940.0, 460.0)
        texture_coordinate_001.location = (-1400.0, 1100.0)

        #sSet dimensions
        reroute_001.width, reroute_001.height = 16.0, 100.0
        bright_contrast.width, bright_contrast.height = 140.0, 100.0
        mapping.width, mapping.height = 140.0, 100.0
        math_004.width, math_004.height = 140.0, 100.0
        separate_xyz_001.width, separate_xyz_001.height = 140.0, 100.0
        group_input.width, group_input.height = 140.0, 100.0
        separate_xyz.width, separate_xyz.height = 140.0, 100.0
        math_001.width, math_001.height = 140.0, 100.0
        combine_xyz.width, combine_xyz.height = 140.0, 100.0
        math_002.width, math_002.height = 140.0, 100.0
        group_output.width, group_output.height = 140.0, 100.0
        translucent_bsdf.width, translucent_bsdf.height = 140.0, 100.0
        mix_shader.width, mix_shader.height = 140.0, 100.0
        mix.width, mix.height = 140.0, 100.0
        math_003.width, math_003.height = 140.0, 100.0
        math.width, math.height = 140.0, 100.0
        math_005.width, math_005.height = 140.0, 100.0
        math_006.width, math_006.height = 140.0, 100.0
        diffuse_bsdf.width, diffuse_bsdf.height = 150.0, 100.0
        reroute.width, reroute.height = 16.0, 100.0
        reroute_003.width, reroute_003.height = 16.0, 100.0
        reroute_002.width, reroute_002.height = 16.0, 100.0
        wave_texture_001.width, wave_texture_001.height = 150.0, 100.0
        voronoi_texture.width, voronoi_texture.height = 140.0, 100.0
        math_007.width, math_007.height = 140.0, 100.0
        vector_math.width, vector_math.height = 140.0, 100.0
        reroute_004.width, reroute_004.height = 16.0, 100.0
        reroute_005.width, reroute_005.height = 16.0, 100.0
        texture_coordinate_001.width, texture_coordinate_001.height = 140.0, 100.0

        #initialize leafnode links
        #mix_shader.Shader -> group_output.Shader
        leafnode.links.new(mix_shader.outputs[0], group_output.inputs[0])
        #translucent_bsdf.BSDF -> mix_shader.Shader
        leafnode.links.new(translucent_bsdf.outputs[0], mix_shader.inputs[2])
        #diffuse_bsdf.BSDF -> mix_shader.Shader
        leafnode.links.new(diffuse_bsdf.outputs[0], mix_shader.inputs[1])
        #reroute.Output -> mapping.Vector
        leafnode.links.new(reroute.outputs[0], mapping.inputs[0])
        #reroute_004.Output -> separate_xyz.Vector
        leafnode.links.new(reroute_004.outputs[0], separate_xyz.inputs[0])
        #separate_xyz.X -> math_001.Value
        leafnode.links.new(separate_xyz.outputs[0], math_001.inputs[0])
        #mapping.Vector -> wave_texture_001.Vector
        leafnode.links.new(mapping.outputs[0], wave_texture_001.inputs[0])
        #math_001.Value -> math_002.Value
        leafnode.links.new(math_001.outputs[0], math_002.inputs[0])
        #combine_xyz.Vector -> mapping.Rotation
        leafnode.links.new(combine_xyz.outputs[0], mapping.inputs[2])
        #math_002.Value -> combine_xyz.Z
        leafnode.links.new(math_002.outputs[0], combine_xyz.inputs[2])
        #wave_texture_001.Fac -> math_004.Value
        leafnode.links.new(wave_texture_001.outputs[1], math_004.inputs[0])
        #math_004.Value -> math_006.Value
        leafnode.links.new(math_004.outputs[0], math_006.inputs[0])
        #math_005.Value -> math_006.Value
        leafnode.links.new(math_005.outputs[0], math_006.inputs[1])
        #group_input.Value -> math_002.Value
        leafnode.links.new(group_input.outputs[1], math_002.inputs[1])
        #reroute_001.Output -> math_004.Value
        leafnode.links.new(reroute_001.outputs[0], math_004.inputs[1])
        #group_input.Threshold -> reroute_001.Input
        leafnode.links.new(group_input.outputs[2], reroute_001.inputs[0])
        #math.Value -> math_005.Value
        leafnode.links.new(math.outputs[0], math_005.inputs[1])
        #math_003.Value -> mix.Factor
        leafnode.links.new(math_003.outputs[0], mix.inputs[0])
        #bright_contrast.Color -> mix.A
        leafnode.links.new(bright_contrast.outputs[0], mix.inputs[6])
        #reroute_002.Output -> reroute_003.Input
        leafnode.links.new(reroute_002.outputs[0], reroute_003.inputs[0])
        #reroute_003.Output -> mix.B
        leafnode.links.new(reroute_003.outputs[0], mix.inputs[7])
        #mix.Result -> diffuse_bsdf.Color
        leafnode.links.new(mix.outputs[2], diffuse_bsdf.inputs[0])
        #mix.Result -> translucent_bsdf.Color
        leafnode.links.new(mix.outputs[2], translucent_bsdf.inputs[0])
        #group_input.Color -> reroute_002.Input
        leafnode.links.new(group_input.outputs[0], reroute_002.inputs[0])
        #reroute_003.Output -> bright_contrast.Color
        leafnode.links.new(reroute_003.outputs[0], bright_contrast.inputs[0])
        #separate_xyz_001.X -> vector_math.Vector
        leafnode.links.new(separate_xyz_001.outputs[0], vector_math.inputs[0])
        #vector_math.Value -> math_005.Value
        leafnode.links.new(vector_math.outputs[1], math_005.inputs[0])
        #reroute_005.Output -> separate_xyz_001.Vector
        leafnode.links.new(reroute_005.outputs[0], separate_xyz_001.inputs[0])
        #reroute_001.Output -> math.Value
        leafnode.links.new(reroute_001.outputs[0], math.inputs[0])
        #reroute.Output -> voronoi_texture.Vector
        leafnode.links.new(reroute.outputs[0], voronoi_texture.inputs[0])
        #math_006.Value -> math_003.Value
        leafnode.links.new(math_006.outputs[0], math_003.inputs[1])
        #voronoi_texture.Distance -> math_007.Value
        leafnode.links.new(voronoi_texture.outputs[0], math_007.inputs[0])
        #math_007.Value -> math_003.Value
        leafnode.links.new(math_007.outputs[0], math_003.inputs[0])
        #reroute_004.Output -> reroute.Input
        leafnode.links.new(reroute_004.outputs[0], reroute.inputs[0])
        #texture_coordinate_001.Object -> reroute_004.Input
        leafnode.links.new(texture_coordinate_001.outputs[3], reroute_004.inputs[0])
        #reroute_004.Output -> reroute_005.Input
        leafnode.links.new(reroute_004.outputs[0], reroute_005.inputs[0])

    leafnode_node_group()

    #node Group
    group = basic.nodes.new("ShaderNodeGroup")
    group.node_tree = bpy.data.node_groups["leafnode"]
    #Input_1
    group.inputs[0].default_value = (0.1369853913784027, 0.1911628544330597, 0.009205194190144539, 1.0)
    #Input_13
    group.inputs[1].default_value = 19.46000099182129
    #Input_14
    group.inputs[2].default_value = 0.010000020265579224

    #Set parents

    #Set locations
    material_output.location = (300.0, 300.0)
    group.location = (-142.69786071777344, 160.0)

    #sSet dimensions
    material_output.width, material_output.height = 140.0, 100.0
    group.width, group.height = 162.69786071777344, 100.0

    #initialize basic links
    #group.Shader -> material_output.Surface
    basic.links.new(group.outputs[0], material_output.inputs[0])

basic_node_group()
