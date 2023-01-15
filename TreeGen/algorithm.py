import math
import random
from mathutils import Vector, noise, Matrix, Quaternion
import bl_math
from .helper import *

# SPINE
# number of vertices, length
def spine_init(n, length, l, p_a, p_s, p_seed, guide):
    # quat rotates the spine, f1 and f2 jiggle the spine
    quat = Vector((0,0,1)).rotation_difference(guide)
    f1 = lambda z : p_a*(noise.noise(Vector([0, p_seed, p_s*z]))-0.5)
    f2 = lambda z : p_a*(noise.noise(Vector([0, p_seed, p_s*(z+length)]))-0.5)
    spine = [quat@Vector((f1(l*i), f2(l*i), l*i)) for i in range(n)]
    spine[0] = Vector((0,0,0))
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
    br_seed *= number
    # generating branch placements
    chosen = pseudo_poisson_disc(number, length/radius, br_seed)

    # guide instructions
    for i in range(number):
        height = chosen[i][1]*(1-start_h)+start_h
        pick = math.floor(n*height)
        trans_vec = spine[pick]*(height*n-pick)+spine[pick]*(pick+1-height*n) #translation vector

        random.seed(br_seed+1) #x axis angle
        x = (height-start_h)/(1-start_h)
        ang = minang*x+maxang*(1-x)
        ang += random.uniform(-var*ang,var*ang)

        a = chosen[i][0]*2*math.pi

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
    #making radius relative
    m_p[3]*=m_p[2]
    
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
    
    #flattening the base
    for i in range(m_p[0]):
        verts[i][2] = 0

    #scaling the tree
    verts = [vec*m_p[4] for vec in verts]
    
    return verts, [], faces, selection