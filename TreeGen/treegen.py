import bpy
import math
import random
from mathutils import Vector, noise, Matrix
import bl_math
import bmesh

# SPINE
# number of vertices, length
def spine_init(n, length, l, p_a, p_s, p_seed, guide):
    # quat rotates the spine, f1 and f2 jiggle the spine
    quat = Vector((0,0,1)).rotation_difference(guide)
    f1 = lambda z : p_a*(noise.noise(Vector([0, p_seed, p_s*z]))-0.5)
    f2 = lambda z : p_a*(noise.noise(Vector([0, p_seed, p_s*(z+length)]))-0.5)
    spine = [quat@Vector((f1(l*i), f2(l*i), l*i)) for i in range(n)]
    return spine

# bends the spine in a more meaningful way
def spine_bend(spine, b_a, b_ang, b_c, b_s, b_w, b_seed, l, guide):
    f_noise = lambda b_a, b_seed, i, l, b_s: b_a*noise.noise((0, b_seed, i*l*b_s))
    for i in range(1, len(spine)):
        bend_vec = Vector((f_noise(b_a, b_seed, i, l, b_s), f_noise(b_a, b_seed+10, i, l, b_s), 1)).normalized()
        
        # correction bend_vec, but honestly it just decides how much this vector points upwards
        vec = spine[i] - spine[i-1]
        x = bl_math.clamp(vec.angle(guide.normalized(),0.0)/math.radians(b_ang))**(1-b_c)**(1-b_c)
        vec = (guide.rotation_difference((0,0,1)))@vec
        bend_vec = bend_vec*(1-x) + Vector((-vec[0],-vec[1], vec[2])).normalized()*x

        #based on a the bd
        

        # transformation itself
        trans1 = Matrix.Translation(-1*spine[i])
        trans2 = Matrix.Translation(spine[i])
        quat = Vector(((0,0,1))).rotation_difference(bend_vec)
        spine[i:] = [trans2@(quat@(trans1@vec)) for vec in spine[i:]]
    return spine

def spine_gen(m_p, bd_p, r_p, guide):
    # parameters
    length, l = m_p[1], m_p[4]
    n = round(length/l)+1
    p_a, p_s, p_seed = r_p
    b_a, b_ang, b_c, b_s, b_w, b_seed = bd_p

    # spine gen
    spine = spine_init(n, length, l, p_a, p_s, p_seed, guide)
    spine = spine_bend(spine, b_a, b_ang, b_c, b_s, b_w, b_seed, l, guide)
    return spine, n

# BARK
# number of sides, radius
def bark_circle(n,r):
    circle = []
    if n<3 or r==0:
        return []
    else:
        for i in range(n):
            circle.append(Vector((r*math.cos(2*math.pi*i/n), r*math.sin(2*math.pi*i/n), 0)))
    return circle

def bark_gen(spine, n, m_p, t_p):
    # parameters
    sides, radius = m_p[0], m_p[2]
    s_fun, f_a = t_p[:2]
    # s_fun function, should be accessible from interface, scales the circles
    scale_list = [s_fun(i/n, f_a)*radius for i in range(n)]

    # generating bark with scaling and rotation based on parameters and spine
    quat = Vector((0,0,1)).rotation_difference(spine[1]-spine[0])
    bark = [quat@i for i in bark_circle(sides,scale_list[0])]
    
    for x in range(1, n-1):
        vec = spine[x+1] - spine[x-1]
        quat = Vector((0,0,1)).rotation_difference(vec)
        new_circle = [quat @ i for i in bark_circle(sides,scale_list[x])]
        for y in new_circle:
            bark.append((Vector(spine[x]) + Vector(y)))
    
    bark += [(quat@i + Vector(spine[-1])) for i in bark_circle(sides,scale_list[-1])]
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
def branch_guides(spine, number, m_p, br_p, t_p):
    # parameters
    n = len(spine)
    length, radius = m_p[1:3]
    a_br, h_br, var_br, s_br = br_p[1:]
    #a_br = (1-var_br)*a_br+var_br*random.uniform(0,90)
    a_br = 45+random.uniform(-var_br*45,var_br*45)
    scale_f1, f_a, scale_f2, br_s = t_p
    guidepacks = []
    
    # guide instructions
    for i in range(number):
        s_br+=1
        random.seed(s_br)
        s_pick = random.randint(round(h_br*n), n-2)+1
        trans_vec = spine[s_pick]
        random.seed(s_br+1)
        a = random.random()*2*math.pi
        quat = Vector((0,0,1)).rotation_difference(spine[s_pick]-spine[s_pick-1])
        guide_vec = quat @ Vector((math.sin(math.radians(a_br))*math.cos(a),math.sin(math.radians(a_br))*math.sin(a), math.cos(math.radians(a_br)))).normalized()
        guide_vec *= m_p[1]*0.4*scale_f2((s_pick/n-h_br)/(1-h_br), br_s)*random.uniform(1-var_br, 1+var_br)
        guide_r = bl_math.clamp(scale_f1(s_pick/(n), f_a)*radius*0.8, 0, guide_vec.length/length*radius)
        guidepacks.append([trans_vec, guide_vec, guide_r])
    return guidepacks

#generates a single trunk, whether it will be branch or the main trunk
def trunk_gen(m_p, bd_p, r_p, t_p, guide):
    spine, n = spine_gen(m_p, bd_p, r_p, guide)
    verts = bark_gen(spine, n, m_p, t_p)
    
    return verts, spine

#returns newspinelist of the new branches
def branch_gen(spinelist, branchdata, vertslist, br_p, number, bd_p, r_p, t_p):
    newspinelist = []
    newvertslist = []
    newbranchdata = []
    newsides = int(bl_math.clamp(branchdata[-1][0][0]//2, 4, branchdata[-1][0][0]))
    for i in range(len(spinelist[-1])):
        #THIS CREATES GUIDES FOR ONE BRANCH IN ONE LEVEL
        guidepacks = branch_guides(spinelist[-1][i], number, branchdata[-1][i], br_p, t_p)
        for pack in guidepacks:
            #THIS CREATES THE SUBBRANCHES FOR THIS ONE BRANCH
            tm_p = [newsides, pack[1].length, pack[2], branchdata[-1][i][3], branchdata[-1][i][4]]
            newbranchdata.append(tm_p)
            r_p[2]+=1 #updating seeds
            br_p[-1]+=1
            bd_p[-1]+=1
            tbd_p = bd_p.copy()
            tbd_p[4]*=pack[2] #multiply weight setting by radius temporarily for the branch
            if tm_p[1]<tm_p[4]: #change 'l' if branch is not long enough
                tm_p[4] = tm_p[1]
            newverts, newspine = trunk_gen(tm_p, tbd_p, r_p, t_p, pack[1])
            newvertslist.append([vec+pack[0] for vec in newverts])
            newspinelist.append([vec+pack[0] for vec in newspine])
    spinelist.append(newspinelist)
    branchdata.append(newbranchdata)
    vertslist.append(newvertslist)

# THE MIGHTY TREE GENERATION
def tree_gen(m_p, br_p, bn_p, bd_p, r_p, t_p,facebool):
    #initial trunk
    verts, spine = trunk_gen(m_p, bd_p, r_p, t_p, Vector((0,0,1)))
    spinelist = [[spine]]
    branchdata = [[m_p]]
    vertslist = [[verts]]
    
    #branch levels
    if br_p[0] != 0:
        for i in range(br_p[0]):
            branch_gen(spinelist, branchdata, vertslist, br_p, bn_p[i], bd_p, r_p, t_p)
    
    #joining verts into one group
    verts = []
    for i in vertslist:
        for k in i:
            verts += k
    
    #making faces
    faces=[]
    if facebool:
        for i in range(br_p[0]+1):
            s = branchdata[i][0][0]
            for spi in spinelist[i]:
                faces.append(face_gen(s, len(spi)))
        while True:
            if len(faces) == 1:
                faces = faces[0]
                break
            faces[0] += [[i+max(faces[0][-1])+1 for i in tup] for tup in faces.pop(1)]
        verts = [vec*m_p[3] for vec in verts] #scales the tree
        return verts, faces
    else:
        spine = [vec*m_p[3] for vec in spine]
        return spine, []

class TreeGen_new(bpy.types.Operator):
    """creates a tree in cursor location"""
    bl_idname = 'object.create_tree'
    bl_label = 'Lob that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tps = context.window_manager.treegen_props

        # temporary parameters
        scale_lf1 = lambda x, a : 1/((x+1)**a)-(x/2)**a #this one is for trunk flare
        scale_lf2 = lambda x, a : ((1-(x-1)**2)/(a*(x-1)+1))**0.5  #this one is for branches scale

        #parameter lists, l is globally defined
        l=tps.Mlength/(tps.Mlength//(tps.Mratio*math.tan(2*math.pi/(2*tps.Msides))*tps.Mradius))

        m_p = [tps.Msides, tps.Mlength, tps.Mradius, tps.Mscale, l]
        br_p = [tps.branch_levels, tps.branch_angle, tps.branch_height, tps.branch_variety, tps.branch_seed]
        bn_p = [tps.branch_number1, tps.branch_number2, tps.branch_number3]
        bd_p = [tps.bends_amount, tps.bends_angle, bl_math.clamp(tps.bends_correction)*3.3, tps.bends_scale, tps.bends_weight, tps.bends_seed]
        t_p = [scale_lf1, tps.flare_amount, scale_lf2, tps.branch_shift]
        r_p = [tps.Rperlin_amount, tps.Rperlin_scale, tps.Rperlin_seed]

        #generates the trunk and lists of lists of stuff
        verts, faces = tree_gen(m_p, br_p, bn_p, bd_p, r_p, t_p, tps.facebool)

        #list of last meshes
        last_meshes = set(o.name for o in bpy.context.scene.objects if o.type == 'MESH')

        mesh = bpy.data.meshes.new("tree")
        object = bpy.data.objects.new("tree", mesh)
        bpy.context.collection.objects.link(object)
        mesh.from_pydata(verts ,[], faces)
        
        #list of new meshes
        new_meshes = set(o.name for o in bpy.context.scene.objects if o.type == 'MESH')
        
        #name of the created object and slecting it
        tps.treename = list(new_meshes-last_meshes)[0]
        this_object = bpy.data.objects[tps.treename]
        bpy.ops.object.select_all(action='DESELECT')
        this_object.select_set(True)
        bpy.context.view_layer.objects.active = this_object
        
        #writing properties
        bpy.context.object["main parameters"] = m_p
        bpy.context.object["branch parameters"] = br_p
        bpy.context.object["branch number parameters"] = bn_p
        bpy.context.object["bends parameters"] = bd_p
        bpy.context.object["temporary parameters"] = [t_p[1],t_p[3]]
        bpy.context.object["random parameters"] = r_p

        verts = []
        faces = []
        return {'FINISHED'}
        
class TreeGen_update(bpy.types.Operator):
    """creates a tree in cursor location"""
    bl_idname = 'object.update_tree'
    bl_label = 'update that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tps = context.window_manager.treegen_props

        # temporary parameters
        scale_lf1 = lambda x, a : 1/((x+1)**a)-(x/2)**a #this one is for trunk flare
        scale_lf2 = lambda x, a : ((1-(x-1)**2)/(a*(x-1)+1))**0.5  #this one is for branches scale

        #parameter lists, l is globally defined
        l=tps.Mlength/(tps.Mlength//(tps.Mratio*math.tan(2*math.pi/(2*tps.Msides))*tps.Mradius))

        m_p = [tps.Msides, tps.Mlength, tps.Mradius, tps.Mscale, l]
        br_p = [tps.branch_levels, tps.branch_angle, tps.branch_height, tps.branch_variety, tps.branch_seed]
        bn_p = [tps.branch_number1, tps.branch_number2, tps.branch_number3]
        bd_p = [tps.bends_amount, tps.bends_angle, bl_math.clamp(tps.bends_correction)*3.3, tps.bends_scale, tps.bends_weight, tps.bends_seed]
        t_p = [scale_lf1, tps.flare_amount, scale_lf2, tps.branch_shift]
        r_p = [tps.Rperlin_amount, tps.Rperlin_scale, tps.Rperlin_seed]

        #generates the trunk and lists of lists of stuff
        verts, faces = tree_gen(m_p, br_p, bn_p, bd_p, r_p, t_p, tps.facebool)
        
        selected_obj = bpy.context.object.data

        t_mesh = bpy.data.meshes.new('tree update')
        t_mesh.from_pydata(verts,[],faces)

        bm = bmesh.new()
        bm.from_mesh(t_mesh)

        bm.to_mesh(selected_obj)
        bm.free()
        bpy.data.meshes.remove(t_mesh)

        return {'FINISHED'}

class OBJECT_PT_TreeGenerator(bpy.types.Panel):
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
        col.label(text="Main Settings:")
        col.prop(wm.treegen_props, "facebool")
        col = layout.column(align=True)
        col.label(text="Main Parameters:")
        col.prop(wm.treegen_props, "Msides")
        col.prop(wm.treegen_props, "Mlength")
        col.prop(wm.treegen_props, "Mradius")
        col.prop(wm.treegen_props, "Mscale")
        col.prop(wm.treegen_props, "Mratio")

        col = layout.column(align=True)
        col.label(text="Bending Parameters:")
        col.prop(wm.treegen_props, "bends_amount")
        col.prop(wm.treegen_props, "bends_scale")
        col.prop(wm.treegen_props, "bends_angle")
        col.prop(wm.treegen_props, "bends_correction")
        col.prop(wm.treegen_props, "bends_weight")

        col = layout.column(align=True)
        col.label(text="Branch Parameters:")
        col.prop(wm.treegen_props, "branch_levels")
        col.prop(wm.treegen_props, "branch_number1")
        col.prop(wm.treegen_props, "branch_number2")
        col.prop(wm.treegen_props, "branch_number3")
        col.prop(wm.treegen_props, "branch_angle")
        col.prop(wm.treegen_props, "branch_height")
        

        
        col = layout.column(align=True)
        col.label(text="Perlin Parameters:")
        col.prop(wm.treegen_props, "Rperlin")
        col.prop(wm.treegen_props, "Rperlin_amount")
        col.prop(wm.treegen_props, "Rperlin_scale")

        col = layout.column(align=True)
        col.label(text="Seeds and variety:")
        col.prop(wm.treegen_props, "Rperlin_seed")
        col.prop(wm.treegen_props, "bends_seed")
        col.prop(wm.treegen_props, "branch_seed")
        col.prop(wm.treegen_props, "branch_variety")
        col = layout.column(align=True)
        col.label(text="Scale Parameters:")
        col.prop(wm.treegen_props, 'flare_amount')