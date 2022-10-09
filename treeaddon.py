import bpy
import bmesh
import math
import random
import mathutils
import bl_math
import inspect

bl_info = {
    "name": "TreeGen",
    "author": "TheTrebuchet",
    "version": (0, 0, 1),
    "blender": (3, 3, 1),
    "location": "View3D > Sidebar > Tree Generator (Create Tab)",
    "description": "Adds a generated tree at cursor",
    "warning": "",
    "doc_url": "",
    "category": "Add Object",
}
# SPINE
# number of vertices, length
def spine_init(n, length, l, p_a, p_s, p_seed, guide):
    # quat rotates the spine, f1 and f2 jiggle the spine
    quat = mathutils.Vector((0,0,1)).rotation_difference(guide)
    f1 = lambda z : p_a*(mathutils.noise.noise(mathutils.Vector([0, p_seed, p_s*z]))-0.5)
    f2 = lambda z : p_a*(mathutils.noise.noise(mathutils.Vector([0, p_seed, p_s*(z+length)]))-0.5)
    spine = [quat@mathutils.Vector((f1(l*i), f2(l*i), l*i)) for i in range(n)]
    return spine

# bends the spine in a more meaningful way
def spine_bend(spine, b_a, b_ang, b_c, b_s, b_seed, l, guide):
    for i in range(1, len(spine)):
        noise = lambda b_a, b_seed, i, l, b_s: b_a*mathutils.noise.noise((0, b_seed, i*l*b_s))
        bend_vec = mathutils.Vector((noise(b_a, b_seed, i, l, b_s), noise(b_a, b_seed+10, i, l, b_s), 1)).normalized()
        
        # correction for absurd angles
        vec = spine[i] - spine[i-1]
        x = bl_math.clamp(vec.angle(guide.normalized(),0.0)/math.radians(b_ang))**b_c**b_c
        vec = (guide.rotation_difference((0,0,1)))@vec
        bend_vec = bend_vec*(1-x) + mathutils.Vector((-vec[0],-vec[1], vec[2])).normalized()*x
        
        # transformation itself
        trans1 = mathutils.Matrix.Translation(-1*spine[i])
        trans2 = mathutils.Matrix.Translation(spine[i])
        quat = mathutils.Vector(((0,0,1))).rotation_difference(bend_vec)
        spine[i:] = [trans2@(quat@(trans1@vec)) for vec in spine[i:]]

        # correction for tree being completely sideways
    ''' 
    vec_c = spine[-1] - spine[0]
    quat = vec_c.rotation_difference(mathutils.Vector((0.0,0.0,1.0)))
    spine = [quat@i for i in spine]
    '''
    return spine

def spine_gen(m_p, r_p, guide):
    # parameters
    length = m_p[1]
    l = m_p[4]
    n = round(length/l)
    p_a, p_s, p_seed, b_a, b_ang, b_c, b_s, b_seed = r_p

    # spine gen
    spine = spine_init(n, length, l, p_a, p_s, p_seed, guide)
    spine = spine_bend(spine, b_a, b_ang, bl_math.clamp(b_c)*3.3, b_s, b_seed, l, guide)
    
    return spine, l, n


# BARK
# number of sides, radius
def bark_circle(n,r):
    circle = []
    if n<3 or r==0:
        return []
    else:
        for i in range(n):
            circle.append(mathutils.Vector((r*math.cos(2*math.pi*i/n), r*math.sin(2*math.pi*i/n), 0)))
    return circle

def bark_gen(spine, l, n, m_p, t_p, guide):
    # generating quat to adjust first and last circle, matters for the branch only
    quat = mathutils.Vector((0,0,1)).rotation_difference(guide)
    # parameters
    sides, length, radius = m_p[:3]
    s_fun, f_a = t_p[:2]
    # s_fun function, should be accessible from interface, scales the circles
    scale_list = [s_fun(h*l, length, radius, f_a) for h in range(n)]

    # generating bark with scaling and rotation based on parameters and spine
    bark = [quat@i for i in bark_circle(sides,scale_list[0])]
    
    for x in range(1, n-1):
        vec = spine[x+1] - spine[x-1]
        quat = mathutils.Vector((0,0,1)).rotation_difference(vec)
        new_circle = [quat @ i for i in bark_circle(sides,scale_list[x])]
        for y in new_circle:
            bark.append((mathutils.Vector(spine[x]) + mathutils.Vector(y)))
    
    bark += [(quat@i + mathutils.Vector(spine[-1])) for i in bark_circle(sides,scale_list[-1])]
    return bark

#number of sides, number of vertices, generates faces
def face_gen(s, n):
    faces = []
    for i in range(n-1):
        for j in range(s):
            if j != s-1:
                faces.append(tuple([j+s*i, j+1+s*i, j+1+(i+1)*s, j+(i+1)*s]))
            else:
                faces.append(tuple([j+s*i, s*i, s*(i+1), j+s*(i+1)]))
    return faces


# BRANCHES AND TREE GENERATION
# outputs [place of the branch, vector that gives branch angle and size, radius of the branch]
def branch_guides(spine, verts, number, m_p, b_p, t_p):
    # parameters
    n = len(spine)
    sides = m_p[0]
    a_br, h_br, var_br, s_br = b_p[1:]
    scale_f, br_w, br_f = t_p[2:]
    guides = []
    
    # guide instructions
    for i in range(number):
        s_br+=number
        random.seed(s_br)
        s_pick = random.randint(round(h_br*n), n-1)
        random.seed(s_br+1)
        v_pick = s_pick*sides+random.randint(0, sides-1)
        trans_vec = spine[s_pick]
        quat = mathutils.Quaternion(((mathutils.Vector((0,0,1))).cross(verts[v_pick]-spine[s_pick])).normalized(), math.radians(a_br))
        guide_vec = (quat @ mathutils.Vector((0,0,1)))*scale_f(s_pick/n, br_f, br_w)
        radius = (verts[v_pick]-spine[s_pick]).length*1.6
        guides.append([trans_vec, guide_vec, radius])
    return guides

#generates a single trunk, whether it will be branch or the main trunk
def trunk_gen(m_p, t_p, r_p, guide):
    spine, l, n = spine_gen(m_p, r_p, guide)
    verts = bark_gen(spine, l, n, m_p, t_p, guide)
    faces = face_gen(m_p[0], n)
    
    return verts, faces, spine

#this function updates facelist of all trunks and branches
#returns newspinelist and newfacelist of the new branches
def branch_gen(vertslist, faceslist, spinelist, m_p, b_p, number, t_p, r_p):
    newspinelist = []
    newvertslist = []
    
    sides = m_p[0]
    t_sides = m_p[0]//2 #updating sides
    if t_sides<4:
        t_sides=4

    for i in range(len(spinelist)):
        guides = branch_guides(spinelist[i], vertslist[i], number, m_p, b_p, t_p)
        m_p[0] = t_sides
        for pack in guides:
            m_p[1] = pack[1].length #updating length
            m_p[2] = pack[-1]*0.6 #updating radius
            r_p[2]+=1 #updating seeds
            r_p[-1]+=1
            
            newverts, newfaces, newspine = trunk_gen(m_p, t_p, r_p, pack[1])
            newverts = [vec+pack[0] for vec in newverts]
            newspine = [vec+pack[0] for vec in newspine]
            newspinelist.append(newspine)
            newvertslist.append(newverts)
            faceslist.append(newfaces)
        m_p[0] = sides
    m_p[0] = t_sides
    return newvertslist, newspinelist


# THE MIGHTY TREE GENERATION
def tree_gen(m_p, b_p, bn_p, t_p, r_p):
    #initial trunk
    verts, faces, spine = trunk_gen(m_p, t_p, r_p, mathutils.Vector((0,0,1)))
    newvertslist = [verts]
    vertslist = [verts]
    faceslist = [faces]
    newspinelist = [spine]
    #generates branches on that trunk stored in new_lists temporarily
    if b_p[0] != 0:
        for i in range(b_p[0]):
            newvertslist, newspinelist = branch_gen(newvertslist, faceslist, newspinelist, m_p, b_p, bn_p[i], t_p, r_p)
            vertslist += newvertslist #newlists are added to old lists

    #faces are created from the list of lists, I am adding corrections to make it into a whole new list
    adds = 0
    for i in range(1, len(vertslist)):
        adds += len(vertslist[i-1])
        faces += [tuple([i+adds for i in j]) for j in faceslist[i]]

    #verts are created from the list of lists, so I am just joining them together
    verts = []
    for i in vertslist:
        verts += i
    
    verts = [vec*m_p[3] for vec in verts] #scales the tree
    return verts, faces

class TreeGen(bpy.types.Operator):
    """creates a tree in cursor location"""
    bl_idname = 'object.create_tree'
    bl_label = 'Lob that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tps = context.window_manager.treegen_props

        # temporary parameters
        flare_amount = 0.1
        scale_lf1 = lambda x, h, r, a : (-r*x**0.5/h**0.5+r)*(1-a)+(-r*x/h+r)*a #this one is for trunk flare
        branch_width = 30
        branch_flare = 1.2
        scale_lf2 = lambda x, a, b :  (a**(-2*(2*x-1))-(2*x-1)**2*a**(-2*(2*x-1)))**0.5*b #this one is for branches scale

        #parameter lists
        l=tps.Mlength/(tps.Mlength//(tps.Mratio*math.tan(2*math.pi/(2*tps.Msides))*tps.Mradius))
        m_p = [tps.Msides, tps.Mlength, tps.Mradius, tps.Mscale, l]
        b_p = [tps.branch_levels, tps.branch_angle, tps.branch_height, tps.branch_variety, tps.branch_seed]
        bn_p = [tps.branch_number1, tps.branch_number2, tps.branch_number3]
        t_p = [scale_lf1, flare_amount, scale_lf2, branch_width, branch_flare]
        r_p = [tps.Rperlin_amount, tps.Rperlin_scale, tps.Rperlin_seed, tps.Rbends_amount, tps.Rbends_angle, tps.Rbends_correction, tps.Rbends_scale, tps.Rbends_seed]


        #generates the trunk and lists of lists of stuff
        verts, faces = tree_gen(m_p, b_p, bn_p, t_p, r_p)

        mesh = bpy.data.meshes.new("tree")
        object = bpy.data.objects.new("tree", mesh)

        bpy.context.collection.objects.link(object)

        mesh.from_pydata(verts ,[], faces)
        verts = []
        faces = []
        return {'FINISHED'}

class TreeGen_PG(bpy.types.PropertyGroup):
    Msides: bpy.props.IntProperty(
        name="Number of trunk sides",
        default=10,
        min=4,
        soft_max=32
    )
    Mlength: bpy.props.FloatProperty(
        name="Trunk length",
        default=100.0,
        min=0.1,
        soft_max=200.0
    )
    Mradius: bpy.props.FloatProperty(
        name="Tree radius",
        default=4,
        min=0.1,
        soft_max=32
    )
    Mscale: bpy.props.FloatProperty(
        name="Tree scale",
        default=0.1,
        min=0.01,
        soft_max=10
    )

    Mratio: bpy.props.FloatProperty(
        name="Ratio of faces",
        default=2,
        min=0.2,
        soft_max=5
    )

    Rperlin: bpy.props.BoolProperty(
        name="turns on the jiggles",
        default=False,
    )

    Rperlin_amount: bpy.props.FloatProperty(
        name="jiggle amount",
        default=0.01,
        min=0.0,
        soft_max=1
    )

    Rperlin_scale: bpy.props.FloatProperty(
        name="jiggle scale",
        default=0.05,
        min=4,
        soft_max=32
    )

    Rperlin_seed: bpy.props.IntProperty(
        name="jiggle seed",
        default=1,
        min=1,
    )

    Rbends_amount: bpy.props.FloatProperty(
        name="bending amount",
        default=0.5,
        min=0.0,
        soft_max=10
    )

    Rbends_angle: bpy.props.FloatProperty(
        name="Bends max angle",
        default=90,
        min=15,
        soft_max=120
    )

    Rbends_correction: bpy.props.FloatProperty(
        name="bending correction",
        default=0.2,
        min=0.0,
        soft_max=1
    )

    Rbends_scale: bpy.props.FloatProperty(
        name="Bending scale",
        default=0.1,
        min=0.01,
        soft_max=10
    )

    Rbends_seed: bpy.props.IntProperty(
        name="bends seed",
        default=1,
        min = 1
    )

    branch_levels: bpy.props.IntProperty(
        name="branching levels",
        default=2,
        min=1,
        soft_max=4
    )

    branch_number1: bpy.props.IntProperty(
        name="branches number1",
        default=30,
        min=1,
        soft_max=100
    )

    branch_number2: bpy.props.IntProperty(
        name="branches number2",
        default=5,
        min=1,
        soft_max=20
    )

    branch_number3: bpy.props.IntProperty(
        name="branches number3",
        default=2,
        min=1,
        soft_max=10
    )

    branch_angle: bpy.props.FloatProperty(
        name="branching angle",
        default=70,
        min=15,
        soft_max=90
    )

    branch_height: bpy.props.FloatProperty(
        name="branching height",
        default=0.3,
        min=0.0,
        soft_max=0.9
    )

    branch_weight: bpy.props.FloatProperty(
        name="branch weight",
        default=0.5,
        min=0.0,
        soft_max=1
    )

    branch_variety: bpy.props.FloatProperty(
        name="branching variety",
        default=0.1,
        min=0.0,
        soft_max=1
    )

    branch_seed: bpy.props.IntProperty(
        name="branching seed",
        default=1,
        min=1,
    )

class Object_PT_TreeGenerator(bpy.types.Panel):
    """Creates a Panel in the Object properties window for tree creation, use with caution"""
    bl_label = "Tree_Gen"
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "Create"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        col = layout.column(align=True)
        
        layout.label(text="Aight lad, lob that tree over there would ya?")

        col.operator('object.create_tree',
        text = 'Create a Tree')
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Main Parameters:")
        col.prop(wm.treegen_props, "Msides")
        col.prop(wm.treegen_props, "Mlength")
        col.prop(wm.treegen_props, "Mradius")
        col.prop(wm.treegen_props, "Mscale")
        col.prop(wm.treegen_props, "Mratio")

        col = layout.column(align=True)
        col.label(text="Random Parameters:")
        col.prop(wm.treegen_props, "Rperlin")
        col.prop(wm.treegen_props, "Rperlin_amount")
        col.prop(wm.treegen_props, "Rperlin_scale")
        col.prop(wm.treegen_props, "Rperlin_seed")
        col.prop(wm.treegen_props, "Rbends_amount")
        col.prop(wm.treegen_props, "Rbends_angle")
        col.prop(wm.treegen_props, "Rbends_correction")
        col.prop(wm.treegen_props, "Rbends_scale")
        col.prop(wm.treegen_props, "Rbends_seed")

        col = layout.column(align=True)
        col.label(text="Branch Parameters:")
        col.prop(wm.treegen_props, "branch_levels")
        col.prop(wm.treegen_props, "branch_number1")
        col.prop(wm.treegen_props, "branch_number2")
        col.prop(wm.treegen_props, "branch_number3")
        col.prop(wm.treegen_props, "branch_angle")
        col.prop(wm.treegen_props, "branch_height")
        col.prop(wm.treegen_props, "branch_weight")
        col.prop(wm.treegen_props, "branch_variety")
        col.prop(wm.treegen_props, "branch_seed")

classes = [TreeGen, TreeGen_PG, Object_PT_TreeGenerator]

def register():
    for i in classes:
        bpy.utils.register_class(i)

    bpy.types.WindowManager.treegen_props = bpy.props.PointerProperty(
        type=TreeGen_PG)


def unregister():
    del bpy.types.WindowManager.treegen_props

    for i in classes:
        bpy.utils.unregister_class(i)

if __name__ == '__main__':
    register()
