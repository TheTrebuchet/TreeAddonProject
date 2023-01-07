import bpy
import math
import random
from mathutils import Vector, noise, Matrix, Quaternion
import bl_math
import bmesh
from . import geogroup

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
def spine_bend(spine, bd_p, l, guide, r, trunk):
    f_noise = lambda b_a, b_seed, i, l, b_s: b_a*noise.noise((0, b_seed, i*l*b_s))
    weight = lambda x, ang: math.sin(ang)*(1-x)*l*len(spine) #it has influences from trunk working corss section, weight of the branch, angle of the branch
    
    b_a, b_up, b_c, b_s, b_w, b_seed = bd_p
    for i in range(1, len(spine)):

        old_vec = spine[i] - spine[i-1] #get previous vector
        angle = (Vector((0,0,1)).angle(old_vec)) #calculate global z angle

        quat = Quaternion(Vector((old_vec[1], -old_vec[0],0)), b_up*angle/(len(spine)-i)) #quat for this step ideal progression
        new_vec = quat@old_vec #rotating the vec
        
        bend_vec = Vector((f_noise(b_a, b_seed, i, l, b_s), f_noise(b_a, b_seed+10, i, l, b_s), 1)).normalized() #generate random vector        
        bend_vec = (Vector((0,0,1)).rotation_difference(new_vec))@bend_vec #rotating bend_vec to local direction
        x = bl_math.clamp(guide.angle(bend_vec,0.0)/math.radians(90))**2 #apply dampening, to be improved
        new_vec = bend_vec*(1-x) + new_vec.normalized()*x #mixing between random (bend_vec) and ideal (new_vec) vectors

        # transformation itself, rotating the remaining branch towards the new vector
        trans1 = Matrix.Translation(-1*spine[i])
        trans2 = Matrix.Translation(spine[i])
        quat = old_vec.rotation_difference(new_vec)
        spine[i:] = [trans2@(quat@(trans1@vec)) for vec in spine[i:]]
    
    for i in range(len(spine)):
        vec = spine[i] - spine[i-1] #get previous vector
        angle = (Vector((0,0,1)).angle(vec))

        CM = spine[(len(spine)+i)//2]-spine[i]
        w_angle = CM[0]**2+CM[1]**2-(r*math.cos(angle))**2
        if w_angle<0: w_angle = 0
        w_angle = weight(i/len(spine), math.atan(w_angle**0.5/(CM[2]+r*math.sin(angle))))
        
        trans1 = Matrix.Translation(-1*spine[i])
        trans2 = Matrix.Translation(spine[i])
        quat = Quaternion(Vector((vec[1], -vec[0],0)), -w_angle*b_w)
        spine[i:] = [trans2@(quat@(trans1@vec)) for vec in spine[i:]]

    if trunk:
        CM = Vector([sum([i[0] for i in spine])/len(spine), sum([i[1] for i in spine])/len(spine), sum([i[2] for i in spine])/len(spine)])
        quat = Quaternion(Vector((CM[1],-CM[0],0)), Vector((0,0,1)).angle(CM)*b_c)
        spine = [quat@i for i in spine]
    return spine

def spine_gen(m_p, bd_p, r_p, guide, trunk):
    # parameters
    length, r, l = m_p[1], m_p[2], m_p[5]
    n = round(length/l)+1
    p_a, p_s, p_seed = r_p

    # spine gen
    spine = spine_init(n, length, l, p_a, p_s, p_seed, guide)
    spine = spine_bend(spine, bd_p, l, guide, r, trunk)
    return spine

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

def bark_gen(spine, m_p, t_p):
    # parameters
    sides, radius, tipradius = m_p[0], m_p[2], m_p[3]
    flare_f, flare_a = t_p[:2]
    n = len(spine)

    scale_list = [bl_math.clamp(flare_f(i/n, flare_a)*radius, tipradius, radius) for i in range(n)]

    # generating bark with scaling and rotation based on parameters and spine
    quat = Vector((0,0,1)).rotation_difference(spine[1]-spine[0])
    bark = [(quat@i)+spine[0] for i in bark_circle(sides,scale_list[0])]
    
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
def guides_gen(spine, number, m_p, br_p, t_p):
    # parameters
    n = len(spine)
    length, radius, tipradius = m_p[1:4]
    minang, maxang, start_h, var, scaling, br_seed = br_p[1:]
    scale_f1, flare, scale_f2, shift = t_p
    guidepacks = []
    
    # guide instructions
    for i in range(number):
        br_seed+=1 #seed update
        
        random.seed(br_seed) #choosing placement of the branch
        height = random.uniform(start_h, 0.99)
        pick = math.floor(n*height)
        trans_vec = spine[pick]*(height*n-pick)+spine[pick]*(pick+1-height*n) #translation vector

        random.seed(br_seed+1) #x axis angle
        x = (height-start_h)/(1-start_h)
        ang = minang*x+maxang*(1-x)
        ang += random.uniform(-var*ang,var*ang)

        random.seed(br_seed+2) #z axis angle
        a = random.random()*2*math.pi 

        quat = Vector((0,0,1)).rotation_difference(spine[pick]-spine[pick-1]) #quaternion from 001 to vector alongside the spine
        dir_vec = Vector((math.sin(math.radians(ang))*math.cos(a),math.sin(math.radians(ang))*math.sin(a), math.cos(math.radians(ang)))).normalized() #bent vector from 001
        guide_vec = quat @ dir_vec #final guide
        guide_vec *= length*scaling*scale_f2(x, shift)*random.uniform(1-var, 1+var) #guide length update
        guide_r = bl_math.clamp(scale_f1(height, flare)*radius*0.8, tipradius, guide_vec.length/length*radius) #radius of the new branch between 1% and proportionate of parent
        guidepacks.append([trans_vec, guide_vec, guide_r]) #creating guidepack
    return guidepacks

#generates a single trunk, whether it will be branch or the main trunk
def trunk_gen(m_p, bd_p, r_p, guide, trunk):
    spine= spine_gen(m_p, bd_p, r_p, guide, trunk)
    
    return spine

#returns newspinelist of the new branches
def branch_gen(spinelist, branchdata, br_p, number, bd_p, r_p, t_p):
    newspinelist = []
    newbranchdata = []
    newsides = int(bl_math.clamp(branchdata[-1][0][0]//2, 4, branchdata[-1][0][0]))
    for i in range(len(spinelist[-1])):
        #THIS CREATES GUIDES FOR ONE BRANCH IN ONE LEVEL
        guidepacks = guides_gen(spinelist[-1][i], number, branchdata[-1][i], br_p, t_p)
        for pack in guidepacks:
            #THIS CREATES THE SUBBRANCHES FOR THIS ONE BRANCH
            tm_p = [newsides, pack[1].length, pack[2], branchdata[-1][i][3], branchdata[-1][i][4] ,branchdata[-1][i][5]] #last level, i branch, parameter
            newbranchdata.append(tm_p)
            r_p[2]+=1 #updating seeds
            br_p[-1]+=1
            bd_p[-1]+=1
            if tm_p[1]<tm_p[5]: #change 'l' if branch is not long enough
                tm_p[5] = tm_p[1]
            newspine = trunk_gen(tm_p, bd_p, r_p, pack[1], False)
            newspinelist.append([vec+pack[0] for vec in newspine])
    spinelist.append(newspinelist)
    branchdata.append(newbranchdata)

# THE MIGHTY TREE GENERATION
def tree_gen(m_p, br_p, bn_p, bd_p, r_p, t_p,facebool):
    #initial trunk
    spine = trunk_gen(m_p, bd_p, r_p, Vector((0,0,1)), True)
    spinelist = [[spine]]
    branchdata = [[m_p]]
    
    #creating the rest of levels
    if br_p[0] != 0:
        for i in range(br_p[0]):
            branch_gen(spinelist, branchdata, br_p, bn_p[i], bd_p, r_p, t_p)

    #if the user doesn't need faces I provide a spine
    if not facebool:
        spine = []
        edges =[]
        for i in spinelist:
            for k in i:
                spine += k
                if edges: edges += [[n+edges[-1][1]+1,n+2+edges[-1][1]] for n in range(len(k))][:-1]
                else: edges += [(n,n+1) for n in range(len(k))][:-1]
        spine = [vec*m_p[4] for vec in spine] #scale update
        return spine, edges, [], []

    #generating verts from spine
    vertslist = []
    for i in range(len(spinelist)):
        level = []
        for k in range(len(spinelist[i])):
            level.append(bark_gen(spinelist[i][k], branchdata[i][k], t_p))
        vertslist.append(level)

    #generating faces and making verts from vertslist
    faces=[]
    verts=[]
    for i in vertslist:
        for k in i:
            verts += k
    selection = [len(verts) - i for i in range(sum([len(k) for k in vertslist[-1]]))]
    
    for i in range(br_p[0]+1):
        s = branchdata[i][0][0]
        for spi in spinelist[i]:
            faces.append(face_gen(s, len(spi)))
    
    while True:
        if len(faces) == 1:
            faces = faces[0]
            break
        faces[0] += [[i+max(faces[0][-1])+1 for i in tup] for tup in faces.pop(1)]
    
    verts = [vec*m_p[4] for vec in verts] #scales the tree
    
    return verts, [], faces, selection

class TreeGen_OT_new(bpy.types.Operator):
    """creates a tree at (0,0,0) according to user panel input"""
    bl_idname = 'object.tree_create'
    bl_label = 'Lob that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tps = context.window_manager.treegen_props

        # temporary parameters
        scale_lf1 = lambda x, a : 1/((x+1)**a)-(x/2)**a #this one is for trunk flare
        scale_lf2 = lambda x, a : ((1-(x-1)**2)/(a*(x-1)+1))**0.5  #this one is for branches scale

        #parameter lists, l is globally defined
        l=tps.Mlength/tps.Mvres

        m_p = [tps.Msides, tps.Mlength, tps.Mradius, tps.Mtipradius, tps.Mscale, l]
        br_p = [tps.branch_levels, tps.branch_minangle, tps.branch_maxangle, tps.branch_height, tps.branch_variety, tps.branch_scaling, tps.branch_seed]
        bn_p = [tps.branch_number1, tps.branch_number2, tps.branch_number3]
        bd_p = [tps.bends_amount, tps.bends_up, tps.bends_correction, tps.bends_scale, tps.bends_weight/(tps.Mlength), tps.bends_seed]
        t_p = [scale_lf1, tps.flare_amount, scale_lf2, tps.branch_shift]
        r_p = [tps.Rperlin_amount, tps.Rperlin_scale, tps.Rperlin_seed]
        seeds = [br_p[-1], bd_p[-1], r_p[-1]]

        #generates the trunk and lists of lists of stuff
        verts, edges, faces, selection = tree_gen(m_p, br_p, bn_p, bd_p, r_p, t_p, tps.facebool)

        #creating the tree
        mesh = bpy.data.meshes.new("tree")
        object = bpy.data.objects.new("tree", mesh)
        bpy.context.collection.objects.link(object)
        mesh.from_pydata(verts ,edges, faces)
        
        #name of the created object and selecting it
        bpy.ops.object.select_all(action='DESELECT')
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.shade_smooth()
        object.matrix_world.translation = context.scene.cursor.location

        #writing properties
        br_p[-1], bd_p[-1], r_p[-1] = seeds
        bpy.context.object["main parameters"] = m_p[:-1] +[tps.Mvres]
        bpy.context.object["branch parameters"] = br_p
        bpy.context.object["branch number parameters"] = bn_p
        bpy.context.object["bends parameters"] = bd_p
        bpy.context.object["temporary parameters"] = [t_p[1],t_p[3]]
        bpy.context.object["random parameters"] = r_p

        #adding vertex group for furthest branches
        if selection:
            v_group = object.vertex_groups.new(name="leaves")
            v_group.add(selection, 1.0, 'ADD')


        if 'TreeGen_nodegroup' not in bpy.data.node_groups:
            geogroup.TreeGen_nodegroup_exec()
        ng = bpy.data.node_groups['TreeGen_nodegroup']
        if 'TreeGen' not in bpy.context.object.modifiers:
            bpy.context.object.modifiers.new(name = 'TreeGen',type = 'NODES')
        geo_mod = bpy.context.object.modifiers['TreeGen']
        if not geo_mod.node_group:
            geo_mod.node_group = ng
        bpy.ops.object.geometry_nodes_input_attribute_toggle(prop_path="[\"Input_2_use_attribute\"]", modifier_name="TreeGen")
        bpy.context.object.modifiers["TreeGen"]["Input_2_attribute_name"] = "leaves"

        verts = []
        faces = []
        return {'FINISHED'}
        
class TreeGen_OT_update(bpy.types.Operator):
    """updates the tree according to user panel input"""
    bl_idname = 'object.tree_update'
    bl_label = 'update that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try: 
            bpy.context.object["main parameters"]
        except: 
            self.report({"INFO"}, "I can't update an object that isn't a tree")
            return {'FINISHED'}
        
        tps = context.window_manager.treegen_props
        selected_obj = bpy.context.object.data

        # temporary parameters
        scale_lf1 = lambda x, a : 1/((x+1)**a)-(x/2)**a #this one is for trunk flare
        scale_lf2 = lambda x, a : ((1-(x-1)**2)/(a*(x-1)+1))**0.5  #this one is for branches scale

        #parameter lists, l is globally defined
        l=tps.Mlength/tps.Mvres

        m_p = [tps.Msides, tps.Mlength, tps.Mradius, tps.Mtipradius, tps.Mscale, l]
        br_p = [tps.branch_levels, tps.branch_minangle, tps.branch_maxangle, tps.branch_height, tps.branch_variety, tps.branch_scaling, tps.branch_seed]
        bn_p = [tps.branch_number1, tps.branch_number2, tps.branch_number3]
        bd_p = [tps.bends_amount, tps.bends_up, tps.bends_correction, tps.bends_scale, tps.bends_weight/(tps.Mlength), tps.bends_seed]
        t_p = [scale_lf1, tps.flare_amount, scale_lf2, tps.branch_shift]
        r_p = [tps.Rperlin_amount, tps.Rperlin_scale, tps.Rperlin_seed]
        seeds = [br_p[-1], bd_p[-1], r_p[-1]]

        #generates the trunk and lists of lists of stuff
        verts, edges, faces, selection = tree_gen(m_p, br_p, bn_p, bd_p, r_p, t_p, tps.facebool)
        
        
        #updating mesh, tree update is a temporary object
        t_mesh = bpy.data.meshes.new('tree update')
        t_mesh.from_pydata(verts,edges,faces)

        bm = bmesh.new()
        bm.from_mesh(t_mesh)

        bm.to_mesh(selected_obj)
        bm.free()
        bpy.data.meshes.remove(t_mesh)
        for f in selected_obj.polygons:
            f.use_smooth = True
        
        v_group = bpy.context.object.vertex_groups['leaves']
        v_group.remove([i for i in range(len(verts))])
        v_group.add(selection, 1.0, 'REPLACE')
        
        br_p[-1], bd_p[-1], r_p[-1] = seeds
        bpy.context.object["main parameters"] = m_p[:-1] + [tps.Mvres]
        bpy.context.object["branch parameters"] = br_p
        bpy.context.object["branch number parameters"] = bn_p
        bpy.context.object["bends parameters"] = bd_p
        bpy.context.object["temporary parameters"] = [t_p[1],t_p[3]]
        bpy.context.object["random parameters"] = r_p

        return {'FINISHED'}

class TreeGen_OT_sync(bpy.types.Operator):
    """syncs tps property group with custom properties"""
    bl_idname = 'object.tree_sync'
    bl_label = 'sync that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try: 
            bpy.context.object["main parameters"]
        except: 
            self.report({"INFO"}, "I can't sync an object that isn't a tree")
            return {'FINISHED'}
        
        selection_name = bpy.context.object.name
        
        tps = bpy.data.window_managers["WinMan"].treegen_props

        tps.sync_complete = False

        m_p = bpy.data.objects[selection_name]['main parameters']
        br_p = bpy.data.objects[selection_name]['branch parameters']
        bn_p = bpy.data.objects[selection_name]['branch number parameters']
        bd_p = bpy.data.objects[selection_name]['bends parameters']
        r_p = bpy.data.objects[selection_name]['temporary parameters']
        t_p = bpy.data.objects[selection_name]['random parameters']
        
        tps.Msides = int(m_p[0])
        tps.Mlength = float(m_p[1])
        tps.Mradius = float(m_p[2])
        tps.Mtipradius = float(m_p[3])
        tps.Mscale = float(m_p[4])
        tps.Mvres = float(m_p[6])
        tps.branch_levels = int(br_p[0])
        tps.branch_minangle = float(br_p[1])
        tps.branch_maxangle = float(br_p[2])
        tps.branch_height = float(br_p[3])
        tps.branch_variety = float(br_p[4])
        tps.branch_scaling = float(br_p[5])
        tps.branch_seed = int(br_p[6])
        tps.branch_number1 = int(bn_p[0])
        tps.branch_number2 = int(bn_p[1])
        tps.branch_number3 = int(bn_p[2])
        tps.bends_amount = float(bd_p[0])
        tps.bends_up = float(bd_p[1])
        tps.bends_correction = float(bd_p[2])
        tps.bends_scale = float(bd_p[3])
        tps.bends_weight = float(bd_p[4])
        tps.bends_seed = int(bd_p[5])
        tps.flare_amount = float(r_p[0])
        tps.branch_shift = float(r_p[1])
        tps.Rperlin_amount = float(t_p[0])
        tps.Rperlin_scale = float(t_p[1])
        tps.Rperlin_seed = int(t_p[2])

        tps.sync_complete = True

        return {'FINISHED'}

class TreeGen_OT_default(bpy.types.Operator):
    """returns all values to default"""
    bl_idname = 'object.tree_sync'
    bl_label = 'sync that tree'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        tps = bpy.data.window_managers["WinMan"].treegen_props
        tps.sync_complete=True
        tps.facebool=True
        tps.Msides=10
        tps.Mlength=100.0
        tps.Mradius=4
        tps.Mtipradius=0.03
        tps.Mscale=0.1
        tps.Mvres=30
        tps.Rperlin_amount=0.3
        tps.Rperlin_scale=0.4
        tps.Rperlin_seed=1
        tps.bends_amount=0.5
        tps.bends_up=0.3
        tps.bends_correction=0.2
        tps.bends_weight=0.5
        tps.bends_scale=0.1
        tps.bends_seed=1
        tps.branch_levels=2
        tps.branch_number1=30
        tps.branch_number2=5
        tps.branch_number3=2
        tps.branch_maxangle=70.0
        tps.branch_minangle=30.0
        tps.branch_height=0.3
        tps.branch_variety=0.1
        tps.branch_scaling=0.3
        tps.branch_seed=1
        tps.branch_shift=0.6
        tps.flare_amount=0.8
        return {'FINISHED'}

class TreeGen_PT_panel(bpy.types.Panel):
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
        tps = bpy.data.window_managers["WinMan"].treegen_props
        layout.label(text="Aight lad, lob that tree over there would ya?")

        col.operator('object.tree_create', text = 'Create a Tree')
        layout.separator()
        col.operator('object.tree_sync', text = 'Sync a Tree')
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Main Settings:")
        col.prop(wm.treegen_props, "facebool")
        col = layout.column(align=True)
        col.label(text="Main Parameters:")
        col.prop(wm.treegen_props, "Msides")
        col.prop(wm.treegen_props, "Mvres")
        col.prop(wm.treegen_props, "Mlength")
        col.prop(wm.treegen_props, "Mradius")
        col.prop(wm.treegen_props, "Mtipradius")
        

        col = layout.column(align=True)
        col.label(text="Bending Parameters:")
        col.prop(wm.treegen_props, "bends_amount")
        col.prop(wm.treegen_props, "bends_scale")
        col.prop(wm.treegen_props, "bends_correction")
        col.prop(wm.treegen_props, "bends_up")
        col.prop(wm.treegen_props, "bends_weight")

        col = layout.column(align=True)
        col.label(text="Branch Parameters:")
        col.prop(wm.treegen_props, "branch_levels")
        for i in range(tps.branch_levels):
            col.prop(wm.treegen_props, "branch_number"+str(i+1))
        col.prop(wm.treegen_props, "branch_scaling")
        col.prop(wm.treegen_props, "branch_minangle")
        col.prop(wm.treegen_props, "branch_maxangle")
        col.prop(wm.treegen_props, "branch_height")
        
        col = layout.column(align=True)
        col.label(text="Simple Jiggle:")
        col.prop(wm.treegen_props, "Rperlin_amount")
        col.prop(wm.treegen_props, "Rperlin_scale")

        col = layout.column(align=True)
        col.label(text="Seeds and Variety:")
        col.prop(wm.treegen_props, "Rperlin_seed")
        col.prop(wm.treegen_props, "bends_seed")
        col.prop(wm.treegen_props, "branch_seed")
        col.prop(wm.treegen_props, "branch_variety")
        col = layout.column(align=True)
        col.label(text="Scale and Shape:")
        col.prop(wm.treegen_props, "Mscale")
        col.prop(wm.treegen_props, 'flare_amount')
        col.prop(wm.treegen_props, 'branch_shift')