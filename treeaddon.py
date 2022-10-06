import bpy
import bmesh
import math
import random
import mathutils
import bl_math

bl_info = {
    "name": "TreeGen",
    "author": "TheTrebuchet",
    "version": (0, 0, 1),
    "blender": (3, 3, 1),
    "location": "View3D > Sidebar > Tree Generator (Create Tab)",
    "description": "Adds generated tree at cursor"
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
def branch_guides(spine, verts, m_p, b_p, t_p):
    # parameters
    n = len(spine)
    sides = m_p[0]
    n_br, a_br, h_br, var_br, s_br = b_p
    scale_f, br_w, br_f = t_p[2:]
    guides = []
    
    # guide instructions
    for i in range(n_br):
        s_br+=n_br
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
def branch_gen(vertslist, faceslist, spinelist, m_p, b_p, t_p, r_p):
    newspinelist = []
    newvertslist = []
    
    sides = m_p[0]
    t_sides = m_p[0]//2 #updating sides
    if t_sides<4:
        t_sides=4

    for i in range(len(spinelist)):
        guides = branch_guides(spinelist[i], vertslist[i], m_p, b_p, t_p)
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
def tree_gen(m_p, b_p, t_p, r_p):
    #initial trunk
    verts, faces, spine = trunk_gen(m_p, t_p, r_p, mathutils.Vector((0,0,1)))
    newvertslist = [verts]
    vertslist = [verts]
    faceslist = [faces]
    newspinelist = [spine]
    #adjusting parameters for branch functions
    branch_seq = b_p[1:4]
    b_p = [b_p[1]]+b_p[4:]
    #generates branches on that trunk stored in new_ lists temporarily
    if b_p[0] != 0:
        for i in branch_seq:
            b_p[0] = i
            newvertslist, newspinelist = branch_gen(newvertslist, faceslist, newspinelist, m_p, b_p, t_p, r_p)
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

    # MAIN PARAMETERS
    sides = 10
    length = 100
    radius = 4
    scale = 0.1
    ratio = 2

    # RANDOM PARAMETERS
    perlin = True
    perlin_amount = 0.01
    perlin_scale = 0.05
    perlin_seed = 3

    bends_amount = 0.5
    bends_angle = 90
    bends_correction = 0.2
    bends_scale = 0.1
    bends_seed = 8

    # BRANCH PARAMETERS
    branch_levels = 2
    branch_number1 = 30
    branch_number2 = 5
    branch_number3 = 2
    branch_angle = 70
    branch_height = 0.3
    branch_weight = 0.5
    branch_variety = 0.1
    branch_seed = 1

    # temporary parameters
    flare_amount = 0.1
    scale_lf1 = lambda x, h, r, a: (-r*x**0.5/h**0.5+r)*(1-a)+(-r*x/h+r)*a #this one is for trunk flare
    branch_width = 30
    branch_flare = 1.2
    scale_lf2 = lambda x, a, b :  (a**(-2*(2*x-1))-(2*x-1)**2*a**(-2*(2*x-1)))**0.5*b #this one is for branches scale

    #parameter lists
    l=length/(length//(ratio*math.tan(2*math.pi/(2*sides))*radius))
    m_p = [sides, length, radius, scale, l]
    b_p = [branch_levels, branch_number1, branch_number2, branch_number3, branch_angle, branch_height, branch_variety, branch_seed]
    t_p = [scale_lf1, flare_amount, scale_lf2, branch_width, branch_flare]
    r_p = [perlin_amount, perlin_scale, perlin_seed, bends_amount, bends_angle, bends_correction, bends_scale, bends_seed]

    def execute(self, context):

        #generates the trunk and lists of lists of stuff

        verts, faces = tree_gen(self.m_p, self.b_p, self.t_p, self.r_p)

        print('-------------------------')
        mesh = bpy.data.meshes.new("tree")
        object = bpy.data.objects.new("tree", mesh)

        bpy.context.collection.objects.link(object)

        mesh.from_pydata(verts ,[], faces)
        return {'FINISHED'}

class TreeGenerator(bpy.types.Panel):
    """Creates a Panel in the Object properties window for tree creation, use with caution"""
    bl_label = "Tree_Gen"
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "Create"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Aight lad, lob that tree over there would ya?")

        row = layout.row()
        row.operator(TreeGen.bl_idname)
        layout.separator()    

def register():
    bpy.utils.register_class(TreeGen)
    bpy.utils.register_class(TreeGenerator)


def unregister():
    bpy.utils.unregister_class(TreeGen)
    bpy.utils.unregister_class(TreeGenerator)

if __name__ == '__main__':
    register()