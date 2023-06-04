import bpy


def barkgroup_node_group():
    barkgroup = bpy.data.node_groups.new(
        type="ShaderNodeTree", name="BarkGroup")
    barkgroup.inputs.new("NodeSocketFloat", "Scale")
    barkgroup.inputs.new("NodeSocketFloat", "Hue")
    barkgroup.inputs.new("NodeSocketFloat", "Saturation")
    barkgroup.inputs.new("NodeSocketFloat", "Brightness")
    barkgroup.inputs.new("NodeSocketVector", "UV Map")
    barkgroup.inputs.new("NodeSocketFloat", "Large Displacement")
    barkgroup.inputs.new("NodeSocketFloat", "Small Displacement")
    barkgroup.outputs.new("NodeSocketColor", "Color")
    barkgroup.outputs.new("NodeSocketFloat", "Roughness")
    barkgroup.outputs.new("NodeSocketFloat", "Displacement")

    # initialize barkgroup nodes
    # node Vector Math.004
    vector_math_004 = barkgroup.nodes.new("ShaderNodeVectorMath")
    vector_math_004.operation = 'ADD'
    # Vector_002
    vector_math_004.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    vector_math_004.inputs[3].default_value = 1.0

    # node Math.001
    math_001 = barkgroup.nodes.new("ShaderNodeMath")
    math_001.operation = 'ADD'
    # Value_002
    math_001.inputs[2].default_value = 0.5

    # node Math
    math = barkgroup.nodes.new("ShaderNodeMath")
    math.operation = 'MULTIPLY'
    # Value_001
    math.inputs[1].default_value = 0.0
    # Value_002
    math.inputs[2].default_value = 0.5

    # node Math.002
    math_002 = barkgroup.nodes.new("ShaderNodeMath")
    math_002.operation = 'MULTIPLY'
    # Value_002
    math_002.inputs[2].default_value = 0.5

    # node Mapping
    mapping = barkgroup.nodes.new("ShaderNodeMapping")
    mapping.vector_type = 'POINT'
    # Location
    mapping.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    mapping.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    mapping.inputs[3].default_value = (1.0, 0.3199999928474426, 1.0)

    # node Noise Texture.001
    noise_texture_001 = barkgroup.nodes.new("ShaderNodeTexNoise")
    noise_texture_001.noise_dimensions = '3D'
    # W
    noise_texture_001.inputs[1].default_value = 0.0
    # Scale
    noise_texture_001.inputs[2].default_value = 17.48000144958496
    # Detail
    noise_texture_001.inputs[3].default_value = 6.139999866485596
    # Roughness
    noise_texture_001.inputs[4].default_value = 0.5
    # Distortion
    noise_texture_001.inputs[5].default_value = 0.0

    # node Math.007
    math_007 = barkgroup.nodes.new("ShaderNodeMath")
    math_007.operation = 'MULTIPLY'
    math_007.use_clamp = True
    # Value_001
    math_007.inputs[1].default_value = 0.06000005453824997
    # Value_002
    math_007.inputs[2].default_value = 0.5

    # node Vector Math
    vector_math = barkgroup.nodes.new("ShaderNodeVectorMath")
    vector_math.operation = 'ADD'
    # Vector_002
    vector_math.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    vector_math.inputs[3].default_value = 1.0

    # node Noise Texture.002
    noise_texture_002 = barkgroup.nodes.new("ShaderNodeTexNoise")
    noise_texture_002.noise_dimensions = '3D'
    # W
    noise_texture_002.inputs[1].default_value = 0.0
    # Scale
    noise_texture_002.inputs[2].default_value = 22.580001831054688
    # Detail
    noise_texture_002.inputs[3].default_value = 5.0
    # Roughness
    noise_texture_002.inputs[4].default_value = 0.5
    # Distortion
    noise_texture_002.inputs[5].default_value = 0.0

    # node Mapping.001
    mapping_001 = barkgroup.nodes.new("ShaderNodeMapping")
    mapping_001.vector_type = 'POINT'
    # Location
    mapping_001.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    mapping_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    mapping_001.inputs[3].default_value = (1.0, 2.1500000953674316, 1.0)

    # node Mapping.002
    mapping_002 = barkgroup.nodes.new("ShaderNodeMapping")
    mapping_002.vector_type = 'POINT'
    # Location
    mapping_002.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    mapping_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    mapping_002.inputs[3].default_value = (1.0, 1.3799999952316284, 1.0)

    # node Math.011
    math_011 = barkgroup.nodes.new("ShaderNodeMath")
    math_011.operation = 'MULTIPLY'
    math_011.use_clamp = True
    # Value_001
    math_011.inputs[1].default_value = 0.3600000739097595
    # Value_002
    math_011.inputs[2].default_value = 0.5

    # node RGB Curves
    rgb_curves = barkgroup.nodes.new("ShaderNodeRGBCurve")
    # mapping settings
    rgb_curves.mapping.extend = 'EXTRAPOLATED'
    rgb_curves.mapping.tone = 'STANDARD'
    rgb_curves.mapping.black_level = (0.0, 0.0, 0.0)
    rgb_curves.mapping.white_level = (1.0, 1.0, 1.0)
    rgb_curves.mapping.clip_min_x = 0.0
    rgb_curves.mapping.clip_min_y = 0.0
    rgb_curves.mapping.clip_max_x = 1.0
    rgb_curves.mapping.clip_max_y = 1.0
    rgb_curves.mapping.use_clip = True
    # curve 0
    rgb_curves_curve_0 = rgb_curves.mapping.curves[0]
    rgb_curves_curve_0_point_0 = rgb_curves_curve_0.points[0]
    rgb_curves_curve_0_point_0.location = (0.0, 0.0)
    rgb_curves_curve_0_point_0.handle_type = 'AUTO'
    rgb_curves_curve_0_point_1 = rgb_curves_curve_0.points[1]
    rgb_curves_curve_0_point_1.location = (1.0, 1.0)
    rgb_curves_curve_0_point_1.handle_type = 'AUTO'
    # curve 1
    rgb_curves_curve_1 = rgb_curves.mapping.curves[1]
    rgb_curves_curve_1_point_0 = rgb_curves_curve_1.points[0]
    rgb_curves_curve_1_point_0.location = (0.0, 0.0)
    rgb_curves_curve_1_point_0.handle_type = 'AUTO'
    rgb_curves_curve_1_point_1 = rgb_curves_curve_1.points[1]
    rgb_curves_curve_1_point_1.location = (1.0, 1.0)
    rgb_curves_curve_1_point_1.handle_type = 'AUTO'
    # curve 2
    rgb_curves_curve_2 = rgb_curves.mapping.curves[2]
    rgb_curves_curve_2_point_0 = rgb_curves_curve_2.points[0]
    rgb_curves_curve_2_point_0.location = (0.0, 0.0)
    rgb_curves_curve_2_point_0.handle_type = 'AUTO'
    rgb_curves_curve_2_point_1 = rgb_curves_curve_2.points[1]
    rgb_curves_curve_2_point_1.location = (1.0, 1.0)
    rgb_curves_curve_2_point_1.handle_type = 'AUTO'
    # curve 3
    rgb_curves_curve_3 = rgb_curves.mapping.curves[3]
    rgb_curves_curve_3_point_0 = rgb_curves_curve_3.points[0]
    rgb_curves_curve_3_point_0.location = (0.0, 0.0)
    rgb_curves_curve_3_point_0.handle_type = 'AUTO'
    rgb_curves_curve_3_point_1 = rgb_curves_curve_3.points[1]
    rgb_curves_curve_3_point_1.location = (
        0.08181818574666977, 0.1499999761581421)
    rgb_curves_curve_3_point_1.handle_type = 'AUTO'
    rgb_curves_curve_3_point_2 = rgb_curves_curve_3.points.new(
        0.21363691985607147, 0.8312504291534424)
    rgb_curves_curve_3_point_2.handle_type = 'VECTOR'
    rgb_curves_curve_3_point_3 = rgb_curves_curve_3.points.new(1.0, 1.0)
    rgb_curves_curve_3_point_3.handle_type = 'AUTO'
    # update curve after changes
    rgb_curves.mapping.update()
    # Fac
    rgb_curves.inputs[0].default_value = 1.0

    # node Noise Texture
    noise_texture = barkgroup.nodes.new("ShaderNodeTexNoise")
    noise_texture.noise_dimensions = '3D'
    # W
    noise_texture.inputs[1].default_value = 0.0
    # Scale
    noise_texture.inputs[2].default_value = 2.1399998664855957
    # Detail
    noise_texture.inputs[3].default_value = 2.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Distortion
    noise_texture.inputs[5].default_value = 0.0

    # node Voronoi Texture
    voronoi_texture = barkgroup.nodes.new("ShaderNodeTexVoronoi")
    voronoi_texture.voronoi_dimensions = '2D'
    voronoi_texture.feature = 'F1'
    voronoi_texture.distance = 'EUCLIDEAN'
    # W
    voronoi_texture.inputs[1].default_value = 0.0
    # Scale
    voronoi_texture.inputs[2].default_value = 27.009998321533203
    # Smoothness
    voronoi_texture.inputs[3].default_value = 0.0
    # Exponent
    voronoi_texture.inputs[4].default_value = 0.5
    # Randomness
    voronoi_texture.inputs[5].default_value = 1.0

    # node Wave Texture
    wave_texture = barkgroup.nodes.new("ShaderNodeTexWave")
    wave_texture.wave_type = 'BANDS'
    wave_texture.rings_direction = 'X'
    wave_texture.wave_profile = 'SIN'
    # Scale
    wave_texture.inputs[1].default_value = 4.5
    # Distortion
    wave_texture.inputs[2].default_value = 0.0
    # Detail
    wave_texture.inputs[3].default_value = 2.0
    # Detail Scale
    wave_texture.inputs[4].default_value = 1.0
    # Detail Roughness
    wave_texture.inputs[5].default_value = 0.5
    # Phase Offset
    wave_texture.inputs[6].default_value = 0.0

    # node Mix.001
    mix_001 = barkgroup.nodes.new("ShaderNodeMix")
    mix_001.data_type = 'RGBA'
    mix_001.clamp_factor = True
    mix_001.factor_mode = 'UNIFORM'
    mix_001.blend_type = 'MIX'
    # Factor_Float
    mix_001.inputs[0].default_value = 0.625
    # Factor_Vector
    mix_001.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_001.inputs[2].default_value = 0.0
    # B_Float
    mix_001.inputs[3].default_value = 0.0
    # A_Vector
    mix_001.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_001.inputs[5].default_value = (0.0, 0.0, 0.0)

    # node Combine XYZ
    combine_xyz = barkgroup.nodes.new("ShaderNodeCombineXYZ")
    # X
    combine_xyz.inputs[0].default_value = 0.0
    # Y
    combine_xyz.inputs[1].default_value = 0.0

    # node Mapping.003
    mapping_003 = barkgroup.nodes.new("ShaderNodeMapping")
    mapping_003.vector_type = 'POINT'
    # Location
    mapping_003.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Scale
    mapping_003.inputs[3].default_value = (1.0, 1.0, 1.0)

    # node Noise Texture.003
    noise_texture_003 = barkgroup.nodes.new("ShaderNodeTexNoise")
    noise_texture_003.noise_dimensions = '3D'
    # W
    noise_texture_003.inputs[1].default_value = 0.0
    # Scale
    noise_texture_003.inputs[2].default_value = 2.4300003051757812
    # Detail
    noise_texture_003.inputs[3].default_value = 0.0
    # Roughness
    noise_texture_003.inputs[4].default_value = 0.5
    # Distortion
    noise_texture_003.inputs[5].default_value = 0.0

    # node Vector Math.005
    vector_math_005 = barkgroup.nodes.new("ShaderNodeVectorMath")
    vector_math_005.operation = 'ADD'
    # Vector_002
    vector_math_005.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    vector_math_005.inputs[3].default_value = 1.0

    # node ColorRamp
    colorramp = barkgroup.nodes.new("ShaderNodeValToRGB")
    colorramp.color_ramp.color_mode = 'RGB'
    colorramp.color_ramp.hue_interpolation = 'NEAR'
    colorramp.color_ramp.interpolation = 'LINEAR'

    colorramp.color_ramp.elements.remove(colorramp.color_ramp.elements[0])
    colorramp_cre_0 = colorramp.color_ramp.elements[0]
    colorramp_cre_0.position = 0.0
    colorramp_cre_0.alpha = 1.0
    colorramp_cre_0.color = (0.012983039021492004,
                             0.008568127639591694, 0.002124689519405365, 1.0)

    colorramp_cre_1 = colorramp.color_ramp.elements.new(0.054545484483242035)
    colorramp_cre_1.alpha = 1.0
    colorramp_cre_1.color = (
        0.21785758435726166, 0.18782173097133636, 0.1369573324918747, 1.0)

    colorramp_cre_2 = colorramp.color_ramp.elements.new(1.0)
    colorramp_cre_2.alpha = 1.0
    colorramp_cre_2.color = (
        0.6724432706832886, 0.5209956765174866, 0.29177066683769226, 1.0)

    # node Map Range.003
    map_range_003 = barkgroup.nodes.new("ShaderNodeMapRange")
    map_range_003.data_type = 'FLOAT'
    map_range_003.interpolation_type = 'LINEAR'
    map_range_003.clamp = True
    # From Min
    map_range_003.inputs[1].default_value = 0.14000000059604645
    # From Max
    map_range_003.inputs[2].default_value = 0.33000004291534424
    # To Min
    map_range_003.inputs[3].default_value = 1.0
    # To Max
    map_range_003.inputs[4].default_value = 0.7799999713897705
    # Steps
    map_range_003.inputs[5].default_value = 4.0
    # Vector
    map_range_003.inputs[6].default_value = (0.0, 0.0, 0.0)
    # From_Min_FLOAT3
    map_range_003.inputs[7].default_value = (0.0, 0.0, 0.0)
    # From_Max_FLOAT3
    map_range_003.inputs[8].default_value = (1.0, 1.0, 1.0)
    # To_Min_FLOAT3
    map_range_003.inputs[9].default_value = (0.0, 0.0, 0.0)
    # To_Max_FLOAT3
    map_range_003.inputs[10].default_value = (1.0, 1.0, 1.0)
    # Steps_FLOAT3
    map_range_003.inputs[11].default_value = (4.0, 4.0, 4.0)

    # node Group Output
    group_output = barkgroup.nodes.new("NodeGroupOutput")

    # node Hue Saturation Value
    hue_saturation_value = barkgroup.nodes.new("ShaderNodeHueSaturation")
    # Fac
    hue_saturation_value.inputs[3].default_value = 1.0

    # node Noise Texture.004
    noise_texture_004 = barkgroup.nodes.new("ShaderNodeTexNoise")
    noise_texture_004.noise_dimensions = '3D'
    # W
    noise_texture_004.inputs[1].default_value = 0.0
    # Scale
    noise_texture_004.inputs[2].default_value = 8.630000114440918
    # Detail
    noise_texture_004.inputs[3].default_value = 0.38999998569488525
    # Roughness
    noise_texture_004.inputs[4].default_value = 0.5
    # Distortion
    noise_texture_004.inputs[5].default_value = 0.0

    # node Map Range.001
    map_range_001 = barkgroup.nodes.new("ShaderNodeMapRange")
    map_range_001.data_type = 'FLOAT'
    map_range_001.interpolation_type = 'LINEAR'
    map_range_001.clamp = True
    # From Min
    map_range_001.inputs[1].default_value = 0.6500000953674316
    # From Max
    map_range_001.inputs[2].default_value = 1.0
    # To Min
    map_range_001.inputs[3].default_value = 0.0
    # To Max
    map_range_001.inputs[4].default_value = 0.06999999284744263
    # Steps
    map_range_001.inputs[5].default_value = 4.0
    # Vector
    map_range_001.inputs[6].default_value = (0.0, 0.0, 0.0)
    # From_Min_FLOAT3
    map_range_001.inputs[7].default_value = (0.0, 0.0, 0.0)
    # From_Max_FLOAT3
    map_range_001.inputs[8].default_value = (1.0, 1.0, 1.0)
    # To_Min_FLOAT3
    map_range_001.inputs[9].default_value = (0.0, 0.0, 0.0)
    # To_Max_FLOAT3
    map_range_001.inputs[10].default_value = (1.0, 1.0, 1.0)
    # Steps_FLOAT3
    map_range_001.inputs[11].default_value = (4.0, 4.0, 4.0)

    # node Map Range.002
    map_range_002 = barkgroup.nodes.new("ShaderNodeMapRange")
    map_range_002.data_type = 'FLOAT'
    map_range_002.interpolation_type = 'LINEAR'
    map_range_002.clamp = True
    # From Min
    map_range_002.inputs[1].default_value = 0.3699999749660492
    # From Max
    map_range_002.inputs[2].default_value = 3.130000114440918
    # To Min
    map_range_002.inputs[3].default_value = 0.0
    # To Max
    map_range_002.inputs[4].default_value = 1.0
    # Steps
    map_range_002.inputs[5].default_value = 4.0
    # Vector
    map_range_002.inputs[6].default_value = (0.0, 0.0, 0.0)
    # From_Min_FLOAT3
    map_range_002.inputs[7].default_value = (0.0, 0.0, 0.0)
    # From_Max_FLOAT3
    map_range_002.inputs[8].default_value = (1.0, 1.0, 1.0)
    # To_Min_FLOAT3
    map_range_002.inputs[9].default_value = (0.0, 0.0, 0.0)
    # To_Max_FLOAT3
    map_range_002.inputs[10].default_value = (1.0, 1.0, 1.0)
    # Steps_FLOAT3
    map_range_002.inputs[11].default_value = (4.0, 4.0, 4.0)

    # node Mix.002
    mix_002 = barkgroup.nodes.new("ShaderNodeMix")
    mix_002.data_type = 'RGBA'
    mix_002.clamp_factor = True
    mix_002.factor_mode = 'UNIFORM'
    mix_002.blend_type = 'LINEAR_LIGHT'
    # Factor_Vector
    mix_002.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix_002.inputs[2].default_value = 0.0
    # B_Float
    mix_002.inputs[3].default_value = 0.0
    # A_Vector
    mix_002.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix_002.inputs[5].default_value = (0.0, 0.0, 0.0)
    # B_Color
    mix_002.inputs[7].default_value = (
        0.041687678545713425, 0.041687678545713425, 0.041687678545713425, 1.0)

    # node Noise Texture.005
    noise_texture_005 = barkgroup.nodes.new("ShaderNodeTexNoise")
    noise_texture_005.noise_dimensions = '3D'
    # W
    noise_texture_005.inputs[1].default_value = 0.0
    # Scale
    noise_texture_005.inputs[2].default_value = 5.989999771118164
    # Detail
    noise_texture_005.inputs[3].default_value = 0.75
    # Roughness
    noise_texture_005.inputs[4].default_value = 0.5
    # Distortion
    noise_texture_005.inputs[5].default_value = 0.0

    # node Principled BSDF
    principled_bsdf_1 = barkgroup.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_1.distribution = 'GGX'
    principled_bsdf_1.subsurface_method = 'RANDOM_WALK'
    # Subsurface
    principled_bsdf_1.inputs[1].default_value = 0.0
    # Subsurface Radius
    principled_bsdf_1.inputs[2].default_value = (
        1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Color
    principled_bsdf_1.inputs[3].default_value = (
        0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    # Subsurface IOR
    principled_bsdf_1.inputs[4].default_value = 1.399999976158142
    # Subsurface Anisotropy
    principled_bsdf_1.inputs[5].default_value = 0.0
    # Metallic
    principled_bsdf_1.inputs[6].default_value = 0.0
    # Specular
    principled_bsdf_1.inputs[7].default_value = 0.5
    # Specular Tint
    principled_bsdf_1.inputs[8].default_value = 0.0
    # Anisotropic
    principled_bsdf_1.inputs[10].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf_1.inputs[11].default_value = 0.0
    # Sheen
    principled_bsdf_1.inputs[12].default_value = 0.0
    # Sheen Tint
    principled_bsdf_1.inputs[13].default_value = 0.5
    # Clearcoat
    principled_bsdf_1.inputs[14].default_value = 0.0
    # Clearcoat Roughness
    principled_bsdf_1.inputs[15].default_value = 0.029999999329447746
    # IOR
    principled_bsdf_1.inputs[16].default_value = 1.4500000476837158
    # Transmission
    principled_bsdf_1.inputs[17].default_value = 0.0
    # Transmission Roughness
    principled_bsdf_1.inputs[18].default_value = 0.0
    # Emission
    principled_bsdf_1.inputs[19].default_value = (0.0, 0.0, 0.0, 1.0)
    # Emission Strength
    principled_bsdf_1.inputs[20].default_value = 1.0
    # Alpha
    principled_bsdf_1.inputs[21].default_value = 1.0
    # Normal
    principled_bsdf_1.inputs[22].default_value = (0.0, 0.0, 0.0)
    # Clearcoat Normal
    principled_bsdf_1.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Tangent
    principled_bsdf_1.inputs[24].default_value = (0.0, 0.0, 0.0)
    # Weight
    principled_bsdf_1.inputs[25].default_value = 0.0

    # node Vector Math.003
    vector_math_003 = barkgroup.nodes.new("ShaderNodeVectorMath")
    vector_math_003.operation = 'MULTIPLY'
    # Vector_002
    vector_math_003.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    vector_math_003.inputs[3].default_value = 1.0

    # node Map Range
    map_range = barkgroup.nodes.new("ShaderNodeMapRange")
    map_range.data_type = 'FLOAT'
    map_range.interpolation_type = 'LINEAR'
    map_range.clamp = True
    # From Min
    map_range.inputs[1].default_value = 0.0
    # From Max
    map_range.inputs[2].default_value = 1.0
    # To Min
    map_range.inputs[3].default_value = -3.5199997425079346
    # To Max
    map_range.inputs[4].default_value = 1.0
    # Steps
    map_range.inputs[5].default_value = 4.0
    # Vector
    map_range.inputs[6].default_value = (0.0, 0.0, 0.0)
    # From_Min_FLOAT3
    map_range.inputs[7].default_value = (0.0, 0.0, 0.0)
    # From_Max_FLOAT3
    map_range.inputs[8].default_value = (1.0, 1.0, 1.0)
    # To_Min_FLOAT3
    map_range.inputs[9].default_value = (0.0, 0.0, 0.0)
    # To_Max_FLOAT3
    map_range.inputs[10].default_value = (1.0, 1.0, 1.0)
    # Steps_FLOAT3
    map_range.inputs[11].default_value = (4.0, 4.0, 4.0)

    # node Math.005
    math_005 = barkgroup.nodes.new("ShaderNodeMath")
    math_005.label = "Small Displacement"
    math_005.operation = 'MULTIPLY'
    # Value_002
    math_005.inputs[2].default_value = 0.5

    # node Group Input
    group_input = barkgroup.nodes.new("NodeGroupInput")

    # node Musgrave Texture
    musgrave_texture = barkgroup.nodes.new("ShaderNodeTexMusgrave")
    musgrave_texture.musgrave_dimensions = '3D'
    musgrave_texture.musgrave_type = 'FBM'
    # W
    musgrave_texture.inputs[1].default_value = 0.0
    # Scale
    musgrave_texture.inputs[2].default_value = 251.69998168945312
    # Detail
    musgrave_texture.inputs[3].default_value = 2.0
    # Dimension
    musgrave_texture.inputs[4].default_value = 2.0
    # Lacunarity
    musgrave_texture.inputs[5].default_value = 2.0
    # Offset
    musgrave_texture.inputs[6].default_value = 0.0
    # Gain
    musgrave_texture.inputs[7].default_value = 1.0

    # node Math.009
    math_009 = barkgroup.nodes.new("ShaderNodeMath")
    math_009.operation = 'ADD'
    # Value_002
    math_009.inputs[2].default_value = 0.5

    # node Math.010
    math_010 = barkgroup.nodes.new("ShaderNodeMath")
    math_010.operation = 'MULTIPLY'
    math_010.use_clamp = True
    # Value_001
    math_010.inputs[1].default_value = 0.22000008821487427
    # Value_002
    math_010.inputs[2].default_value = 0.5

    # node Voronoi Texture.001
    voronoi_texture_001 = barkgroup.nodes.new("ShaderNodeTexVoronoi")
    voronoi_texture_001.label = "Voronoi"
    voronoi_texture_001.voronoi_dimensions = '3D'
    voronoi_texture_001.feature = 'SMOOTH_F1'
    voronoi_texture_001.distance = 'EUCLIDEAN'
    # W
    voronoi_texture_001.inputs[1].default_value = 0.0
    # Scale
    voronoi_texture_001.inputs[2].default_value = 83.53999328613281
    # Smoothness
    voronoi_texture_001.inputs[3].default_value = 1.0
    # Exponent
    voronoi_texture_001.inputs[4].default_value = 0.5
    # Randomness
    voronoi_texture_001.inputs[5].default_value = 1.0

    # node ColorRamp.001
    colorramp_001 = barkgroup.nodes.new("ShaderNodeValToRGB")
    colorramp_001.color_ramp.color_mode = 'RGB'
    colorramp_001.color_ramp.hue_interpolation = 'NEAR'
    colorramp_001.color_ramp.interpolation = 'LINEAR'

    colorramp_001.color_ramp.elements.remove(
        colorramp_001.color_ramp.elements[0])
    colorramp_001_cre_0 = colorramp_001.color_ramp.elements[0]
    colorramp_001_cre_0.position = 0.0
    colorramp_001_cre_0.alpha = 1.0
    colorramp_001_cre_0.color = (
        0.16537627577781677, 0.12001702189445496, 0.05650651082396507, 1.0)

    colorramp_001_cre_1 = colorramp_001.color_ramp.elements.new(1.0)
    colorramp_001_cre_1.alpha = 1.0
    colorramp_001_cre_1.color = (
        0.41593509912490845, 0.3226011395454407, 0.15277840197086334, 1.0)

    # node Math.003
    math_003 = barkgroup.nodes.new("ShaderNodeMath")
    math_003.operation = 'SUBTRACT'
    math_003.use_clamp = True
    # Value_002
    math_003.inputs[2].default_value = 0.5

    # node Math.004
    math_004 = barkgroup.nodes.new("ShaderNodeMath")
    math_004.operation = 'MULTIPLY'
    math_004.use_clamp = True
    # Value_001
    math_004.inputs[1].default_value = 1.0
    # Value_002
    math_004.inputs[2].default_value = 0.5

    # node Math.008
    math_008 = barkgroup.nodes.new("ShaderNodeMath")
    math_008.operation = 'MULTIPLY'
    math_008.use_clamp = True
    # Value_001
    math_008.inputs[1].default_value = 0.6000000238418579
    # Value_002
    math_008.inputs[2].default_value = 0.5

    # node Mix
    mix = barkgroup.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.clamp_factor = True
    mix.factor_mode = 'UNIFORM'
    mix.blend_type = 'SOFT_LIGHT'
    mix.clamp_result = True
    # Factor_Float
    mix.inputs[0].default_value = 0.9912496209144592
    # Factor_Vector
    mix.inputs[1].default_value = (0.5, 0.5, 0.5)
    # A_Float
    mix.inputs[2].default_value = 0.0
    # B_Float
    mix.inputs[3].default_value = 0.0
    # A_Vector
    mix.inputs[4].default_value = (0.0, 0.0, 0.0)
    # B_Vector
    mix.inputs[5].default_value = (0.0, 0.0, 0.0)

    # Set parents

    # Set locations
    vector_math_004.location = (23.0, 441.0)
    math_001.location = (-137.0, 441.0)
    math.location = (-297.0, 441.0)
    math_002.location = (-297.0, 267.0)
    mapping.location = (-617.0, 441.0)
    noise_texture_001.location = (-457.0, 206.0)
    math_007.location = (23.0, 25.0)
    vector_math.location = (183.0, -155.0)
    noise_texture_002.location = (-137.0, -104.0)
    mapping_001.location = (-137.0, 267.0)
    mapping_002.location = (353.0, -70.0)
    math_011.location = (1033.0, -244.0)
    rgb_curves.location = (353.0, 441.0)
    noise_texture.location = (-457.0, 441.0)
    voronoi_texture.location = (23.0, 290.0)
    wave_texture.location = (183.0, 441.0)
    mix_001.location = (1033.0, 174.0)
    combine_xyz.location = (-1097.0, 441.0)
    mapping_003.location = (-937.0, 441.0)
    noise_texture_003.location = (-1417.0, 441.0)
    vector_math_005.location = (-777.0, 441.0)
    colorramp.location = (773.0, 206.0)
    map_range_003.location = (1362.6102294921875, 175.7975311279297)
    group_output.location = (1973.0, -0.0)
    hue_saturation_value.location = (1353.0, 441.0)
    noise_texture_004.location = (-1097.0, 302.0)
    map_range_001.location = (-937.0, 130.0)
    map_range_002.location = (1033.0, 441.0)
    mix_002.location = (1193.0, 441.0)
    noise_texture_005.location = (780.0, 680.0)
    principled_bsdf_1.location = (1523.0, 441.0)
    vector_math_003.location = (-1700.0, 440.0)
    map_range.location = (183.0, 112.0)
    math_005.location = (-1257.0, 441.0)
    group_input.location = (-2020.0, 80.0)
    musgrave_texture.location = (353.0, -441.0)
    math_009.location = (760.0, -260.0)
    math_010.location = (560.0, -160.0)
    voronoi_texture_001.location = (560.0, 120.0)
    colorramp_001.location = (773.0, -26.0)
    math_003.location = (613.0, 441.0)
    math_004.location = (353.0, 104.0)
    math_008.location = (1033.0, -70.0)
    mix.location = (1193.0, 197.0)

    # sSet dimensions
    vector_math_004.width, vector_math_004.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    math_002.width, math_002.height = 140.0, 100.0
    mapping.width, mapping.height = 140.0, 100.0
    noise_texture_001.width, noise_texture_001.height = 140.0, 100.0
    math_007.width, math_007.height = 140.0, 100.0
    vector_math.width, vector_math.height = 140.0, 100.0
    noise_texture_002.width, noise_texture_002.height = 140.0, 100.0
    mapping_001.width, mapping_001.height = 140.0, 100.0
    mapping_002.width, mapping_002.height = 140.0, 100.0
    math_011.width, math_011.height = 140.0, 100.0
    rgb_curves.width, rgb_curves.height = 240.0, 100.0
    noise_texture.width, noise_texture.height = 140.0, 100.0
    voronoi_texture.width, voronoi_texture.height = 140.0, 100.0
    wave_texture.width, wave_texture.height = 150.0, 100.0
    mix_001.width, mix_001.height = 140.0, 100.0
    combine_xyz.width, combine_xyz.height = 140.0, 100.0
    mapping_003.width, mapping_003.height = 140.0, 100.0
    noise_texture_003.width, noise_texture_003.height = 140.0, 100.0
    vector_math_005.width, vector_math_005.height = 140.0, 100.0
    colorramp.width, colorramp.height = 240.0, 100.0
    map_range_003.width, map_range_003.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    hue_saturation_value.width, hue_saturation_value.height = 150.0, 100.0
    noise_texture_004.width, noise_texture_004.height = 140.0, 100.0
    map_range_001.width, map_range_001.height = 140.0, 100.0
    map_range_002.width, map_range_002.height = 140.0, 100.0
    mix_002.width, mix_002.height = 140.0, 100.0
    noise_texture_005.width, noise_texture_005.height = 140.0, 100.0
    principled_bsdf_1.width, principled_bsdf_1.height = 240.0, 100.0
    vector_math_003.width, vector_math_003.height = 140.0, 100.0
    map_range.width, map_range.height = 140.0, 100.0
    math_005.width, math_005.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    musgrave_texture.width, musgrave_texture.height = 150.0, 100.0
    math_009.width, math_009.height = 140.0, 100.0
    math_010.width, math_010.height = 140.0, 100.0
    voronoi_texture_001.width, voronoi_texture_001.height = 140.0, 100.0
    colorramp_001.width, colorramp_001.height = 240.0, 100.0
    math_003.width, math_003.height = 140.0, 100.0
    math_004.width, math_004.height = 140.0, 100.0
    math_008.width, math_008.height = 140.0, 100.0
    mix.width, mix.height = 140.0, 100.0

    # initialize barkgroup links
    # vector_math_004.Vector -> wave_texture.Vector
    barkgroup.links.new(vector_math_004.outputs[0], wave_texture.inputs[0])
    # vector_math_005.Vector -> vector_math_004.Vector
    barkgroup.links.new(vector_math_005.outputs[0], vector_math_004.inputs[0])
    # wave_texture.Color -> rgb_curves.Color
    barkgroup.links.new(wave_texture.outputs[0], rgb_curves.inputs[1])
    # math_001.Value -> vector_math_004.Vector
    barkgroup.links.new(math_001.outputs[0], vector_math_004.inputs[1])
    # noise_texture.Fac -> math.Value
    barkgroup.links.new(noise_texture.outputs[0], math.inputs[0])
    # math.Value -> math_001.Value
    barkgroup.links.new(math.outputs[0], math_001.inputs[0])
    # noise_texture_001.Fac -> math_002.Value
    barkgroup.links.new(noise_texture_001.outputs[0], math_002.inputs[0])
    # math_002.Value -> math_001.Value
    barkgroup.links.new(math_002.outputs[0], math_001.inputs[1])
    # vector_math_005.Vector -> noise_texture.Vector
    barkgroup.links.new(vector_math_005.outputs[0], noise_texture.inputs[0])
    # mapping.Vector -> noise_texture_001.Vector
    barkgroup.links.new(mapping.outputs[0], noise_texture_001.inputs[0])
    # vector_math_005.Vector -> mapping.Vector
    barkgroup.links.new(vector_math_005.outputs[0], mapping.inputs[0])
    # vector_math_005.Vector -> mapping_001.Vector
    barkgroup.links.new(vector_math_005.outputs[0], mapping_001.inputs[0])
    # mapping_001.Vector -> voronoi_texture.Vector
    barkgroup.links.new(mapping_001.outputs[0], voronoi_texture.inputs[0])
    # rgb_curves.Color -> math_003.Value
    barkgroup.links.new(rgb_curves.outputs[0], math_003.inputs[0])
    # voronoi_texture.Distance -> map_range.Value
    barkgroup.links.new(voronoi_texture.outputs[0], map_range.inputs[0])
    # map_range.Result -> math_004.Value
    barkgroup.links.new(map_range.outputs[0], math_004.inputs[0])
    # mapping_002.Vector -> voronoi_texture_001.Vector
    barkgroup.links.new(mapping_002.outputs[0], voronoi_texture_001.inputs[0])
    # vector_math_005.Vector -> vector_math.Vector
    barkgroup.links.new(vector_math_005.outputs[0], vector_math.inputs[0])
    # vector_math_005.Vector -> noise_texture_002.Vector
    barkgroup.links.new(
        vector_math_005.outputs[0], noise_texture_002.inputs[0])
    # math_007.Value -> vector_math.Vector
    barkgroup.links.new(math_007.outputs[0], vector_math.inputs[1])
    # noise_texture_002.Fac -> math_007.Value
    barkgroup.links.new(noise_texture_002.outputs[0], math_007.inputs[0])
    # math_008.Value -> mix.A
    barkgroup.links.new(math_008.outputs[0], mix.inputs[6])
    # math_011.Value -> mix.B
    barkgroup.links.new(math_011.outputs[0], mix.inputs[7])
    # math_003.Value -> math_008.Value
    barkgroup.links.new(math_003.outputs[0], math_008.inputs[0])
    # math_003.Value -> colorramp.Fac
    barkgroup.links.new(math_003.outputs[0], colorramp.inputs[0])
    # colorramp.Color -> mix_001.A
    barkgroup.links.new(colorramp.outputs[0], mix_001.inputs[6])
    # colorramp_001.Color -> mix_001.B
    barkgroup.links.new(colorramp_001.outputs[0], mix_001.inputs[7])
    # voronoi_texture_001.Color -> colorramp_001.Fac
    barkgroup.links.new(
        voronoi_texture_001.outputs[1], colorramp_001.inputs[0])
    # vector_math.Vector -> mapping_002.Vector
    barkgroup.links.new(vector_math.outputs[0], mapping_002.inputs[0])
    # voronoi_texture_001.Color -> math_009.Value
    barkgroup.links.new(voronoi_texture_001.outputs[1], math_009.inputs[0])
    # musgrave_texture.Fac -> math_010.Value
    barkgroup.links.new(musgrave_texture.outputs[0], math_010.inputs[0])
    # math_010.Value -> math_009.Value
    barkgroup.links.new(math_010.outputs[0], math_009.inputs[1])
    # math_009.Value -> math_011.Value
    barkgroup.links.new(math_009.outputs[0], math_011.inputs[0])
    # math_004.Value -> math_003.Value
    barkgroup.links.new(math_004.outputs[0], math_003.inputs[1])
    # vector_math_003.Vector -> mapping_003.Vector
    barkgroup.links.new(vector_math_003.outputs[0], mapping_003.inputs[0])
    # combine_xyz.Vector -> mapping_003.Rotation
    barkgroup.links.new(combine_xyz.outputs[0], mapping_003.inputs[2])
    # noise_texture_003.Fac -> math_005.Value
    barkgroup.links.new(noise_texture_003.outputs[0], math_005.inputs[0])
    # math_005.Value -> combine_xyz.Z
    barkgroup.links.new(math_005.outputs[0], combine_xyz.inputs[2])
    # vector_math_003.Vector -> noise_texture_003.Vector
    barkgroup.links.new(
        vector_math_003.outputs[0], noise_texture_003.inputs[0])
    # noise_texture_005.Fac -> map_range_002.Value
    barkgroup.links.new(noise_texture_005.outputs[0], map_range_002.inputs[0])
    # mix_001.Result -> mix_002.A
    barkgroup.links.new(mix_001.outputs[2], mix_002.inputs[6])
    # map_range_002.Result -> mix_002.Factor
    barkgroup.links.new(map_range_002.outputs[0], mix_002.inputs[0])
    # mapping_003.Vector -> vector_math_005.Vector
    barkgroup.links.new(mapping_003.outputs[0], vector_math_005.inputs[0])
    # vector_math_003.Vector -> noise_texture_004.Vector
    barkgroup.links.new(
        vector_math_003.outputs[0], noise_texture_004.inputs[0])
    # noise_texture_004.Fac -> map_range_001.Value
    barkgroup.links.new(noise_texture_004.outputs[0], map_range_001.inputs[0])
    # map_range_001.Result -> vector_math_005.Vector
    barkgroup.links.new(map_range_001.outputs[0], vector_math_005.inputs[1])
    # hue_saturation_value.Color -> principled_bsdf_1.Base Color
    barkgroup.links.new(
        hue_saturation_value.outputs[0], principled_bsdf_1.inputs[0])
    # mix_002.Result -> hue_saturation_value.Color
    barkgroup.links.new(mix_002.outputs[2], hue_saturation_value.inputs[4])
    # mix.Result -> map_range_003.Value
    barkgroup.links.new(mix.outputs[2], map_range_003.inputs[0])
    # map_range_003.Result -> principled_bsdf_1.Roughness
    barkgroup.links.new(map_range_003.outputs[0], principled_bsdf_1.inputs[9])
    # group_input.Scale -> vector_math_003.Vector
    barkgroup.links.new(group_input.outputs[0], vector_math_003.inputs[1])
    # hue_saturation_value.Color -> group_output.Color
    barkgroup.links.new(
        hue_saturation_value.outputs[0], group_output.inputs[0])
    # map_range_003.Result -> group_output.Roughness
    barkgroup.links.new(map_range_003.outputs[0], group_output.inputs[1])
    # mix.Result -> group_output.Displacement
    barkgroup.links.new(mix.outputs[2], group_output.inputs[2])
    # group_input.Hue -> hue_saturation_value.Hue
    barkgroup.links.new(group_input.outputs[1], hue_saturation_value.inputs[0])
    # group_input.Saturation -> hue_saturation_value.Saturation
    barkgroup.links.new(group_input.outputs[2], hue_saturation_value.inputs[1])
    # group_input.Brightness -> hue_saturation_value.Value
    barkgroup.links.new(group_input.outputs[3], hue_saturation_value.inputs[2])
    # vector_math_003.Vector -> noise_texture_005.Vector
    barkgroup.links.new(
        vector_math_003.outputs[0], noise_texture_005.inputs[0])
    # vector_math_003.Vector -> musgrave_texture.Vector
    barkgroup.links.new(vector_math_003.outputs[0], musgrave_texture.inputs[0])
    # group_input.map -> vector_math_003.Vector
    barkgroup.links.new(group_input.outputs[4], vector_math_003.inputs[0])
    # group_input.Small Disp -> math_002.Value
    barkgroup.links.new(group_input.outputs[5], math_002.inputs[1])
    # group_input.Large Disp -> math_005.Value
    barkgroup.links.new(group_input.outputs[6], math_005.inputs[1])


def calmtree_bark_node_group(mat):
    calmtree_bark = mat.node_tree
    # start with a clean node tree
    for node in calmtree_bark.nodes:
        calmtree_bark.nodes.remove(node)
    # initialize calmtree_bark nodes
    # node Material Output
    material_output = calmtree_bark.nodes.new("ShaderNodeOutputMaterial")
    material_output.target = 'ALL'
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # node Principled BSDF
    principled_bsdf = calmtree_bark.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.distribution = 'GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Subsurface
    principled_bsdf.inputs[1].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[2].default_value = (
        1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Color
    principled_bsdf.inputs[3].default_value = (
        0.05012740194797516, 0.08010157942771912, 0.3986773192882538, 1.0)
    # Subsurface IOR
    principled_bsdf.inputs[4].default_value = 1.399999976158142
    # Subsurface Anisotropy
    principled_bsdf.inputs[5].default_value = 0.0
    # Metallic
    principled_bsdf.inputs[6].default_value = 0.0
    # Specular
    principled_bsdf.inputs[7].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[8].default_value = 0.0
    # Anisotropic
    principled_bsdf.inputs[10].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[11].default_value = 0.0
    # Sheen
    principled_bsdf.inputs[12].default_value = 0.0
    # Sheen Tint
    principled_bsdf.inputs[13].default_value = 0.5
    # Clearcoat
    principled_bsdf.inputs[14].default_value = 0.0
    # Clearcoat Roughness
    principled_bsdf.inputs[15].default_value = 0.029999999329447746
    # IOR
    principled_bsdf.inputs[16].default_value = 1.4500000476837158
    # Transmission
    principled_bsdf.inputs[17].default_value = 0.0
    # Transmission Roughness
    principled_bsdf.inputs[18].default_value = 0.0
    # Emission
    principled_bsdf.inputs[19].default_value = (0.0, 0.0, 0.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[20].default_value = 1.0
    # Alpha
    principled_bsdf.inputs[21].default_value = 1.0
    # Normal
    principled_bsdf.inputs[22].default_value = (0.0, 0.0, 0.0)
    # Clearcoat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Tangent
    principled_bsdf.inputs[24].default_value = (0.0, 0.0, 0.0)
    # Weight
    principled_bsdf.inputs[25].default_value = 0.0

    # node Group
    group = calmtree_bark.nodes.new("ShaderNodeGroup")
    group.node_tree = bpy.data.node_groups["BarkGroup"]
    # Input_0
    group.inputs[0].default_value = 10.0
    # Input_7
    group.inputs[1].default_value = 0.44999998807907104
    # Input_8
    group.inputs[2].default_value = 0.4000000059604645
    # Input_9
    group.inputs[3].default_value = 0.10000000149011612
    # Input_22
    group.inputs[5].default_value = 0.20000000298023224
    # Input_23
    group.inputs[6].default_value = 0.019999999552965164

    # node Displacement
    displacement = calmtree_bark.nodes.new("ShaderNodeDisplacement")
    displacement.space = 'OBJECT'
    # Midlevel
    displacement.inputs[1].default_value = 0.0
    # Scale
    displacement.inputs[2].default_value = 0.14000001549720764
    # Normal
    displacement.inputs[3].default_value = (0.0, 0.0, 0.0)

    # node Texture Coordinate
    texture_coordinate = calmtree_bark.nodes.new("ShaderNodeTexCoord")

    # Set parents

    # Set locations
    material_output.location = (723.7403564453125, 110.46446228027344)
    principled_bsdf.location = (33.0, 140.0)
    group.location = (-679.8018798828125, -120.0)
    displacement.location = (40.0, -540.0)
    texture_coordinate.location = (-880.0, -120.0)

    # sSet dimensions
    material_output.width, material_output.height = 140.0, 100.0
    principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
    group.width, group.height = 212.8018798828125, 100.0
    displacement.width, displacement.height = 140.0, 100.0
    texture_coordinate.width, texture_coordinate.height = 140.0, 100.0

    # initialize calmtree_bark links
    # group.Color -> principled_bsdf.Base Color
    calmtree_bark.links.new(group.outputs[0], principled_bsdf.inputs[0])
    # group.Roughness -> principled_bsdf.Roughness
    calmtree_bark.links.new(group.outputs[1], principled_bsdf.inputs[9])
    # displacement.Displacement -> material_output.Displacement
    calmtree_bark.links.new(displacement.outputs[0], material_output.inputs[2])
    # group.Displacement -> displacement.Height
    calmtree_bark.links.new(group.outputs[2], displacement.inputs[0])
    # principled_bsdf.BSDF -> material_output.Surface
    calmtree_bark.links.new(
        principled_bsdf.outputs[0], material_output.inputs[0])
    # texture_coordinate.UV -> group.map
    calmtree_bark.links.new(texture_coordinate.outputs[2], group.inputs[4])
