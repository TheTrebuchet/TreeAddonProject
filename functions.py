import math
import random
import mathutils
import bl_math

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
    length, l = m_p[1], m_p[4]
    n = round(length/l)
    p_a, p_s, p_seed, b_a, b_ang, b_c, b_s, b_seed = r_p

    # spine gen
    spine = spine_init(n, length, l, p_a, p_s, p_seed, guide)
    spine = spine_bend(spine, b_a, b_ang, b_c, b_s, b_seed, l, guide)
    
    return spine, n

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

def bark_gen(spine, n, m_p, t_p, guide):
    # generating quat to adjust first and last circle, matters for the branch only
    quat = mathutils.Vector((0,0,1)).rotation_difference(guide)
    # parameters
    sides, radius = m_p[0], m_p[2]
    s_fun, f_a = t_p[:2]
    # s_fun function, should be accessible from interface, scales the circles
    scale_list = [s_fun(i/n, f_a)*radius for i in range(n)]

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
def branch_guides(spine, number, m_p, b_p, t_p):
    # parameters
    n = len(spine)
    radius = m_p[2]
    a_br, h_br, var_br, s_br = b_p[1:]
    scale_f1, f_a, scale_f2, br_s = t_p
    guides = []
    
    # guide instructions
    for i in range(number):
        s_br+=1
        random.seed(s_br)
        s_pick = random.randint(round(h_br*n), n-2)+1
        trans_vec = spine[s_pick]
        random.seed(s_br+1)
        a = random.random()*2*math.pi
        quat = mathutils.Vector((0,0,1)).rotation_difference(spine[s_pick]-spine[s_pick-1])
        guide_vec = quat @ mathutils.Vector((math.sin(math.radians(a_br))*math.cos(a),math.sin(math.radians(a_br))*math.sin(a), math.cos(math.radians(a_br)))).normalized()
        print((s_pick/n-h_br)/(1-h_br))
        guide_vec *= m_p[1]*scale_f2((s_pick/n-h_br)/(1-h_br), br_s)
        guide_r = scale_f1(s_pick/(n), f_a)*radius*0.8
        guides.append([trans_vec, guide_vec, guide_r])
    return guides

#generates a single trunk, whether it will be branch or the main trunk
def trunk_gen(m_p, t_p, r_p, guide):
    spine, n = spine_gen(m_p, r_p, guide)
    verts = bark_gen(spine, n, m_p, t_p, guide)
    faces = face_gen(m_p[0], n)
    
    return verts, faces, spine

#this function updates facelist of all trunks and branches
#returns newspinelist and newfacelist of the new branches
def branch_gen(faceslist, spinelist, branchdata, b_p, number, t_p, r_p):
    newspinelist = []
    newvertslist = []
    newbranchdata = []
    for i in range(len(spinelist)):
        #THIS CREATES GUIDES FOR ONE BRANCH IN ONE LEVEL
        guides = branch_guides(spinelist[i], number, branchdata[i], b_p, t_p)
        for pack in guides:
            #THIS CREATES THE SUBBRANCHES FOR THIS ONE BRANCH
            tm_p = [branchdata[i][0], pack[1].length, pack[2], branchdata[i][3], branchdata[i][4]]
            newbranchdata.append(tm_p)
            print(tm_p)
            r_p[2]+=1 #updating perlin seeds
            r_p[-1]+=1
            
            newverts, newfaces, newspine = trunk_gen(tm_p, t_p, r_p, pack[1])
            newverts = [vec+pack[0] for vec in newverts]
            newspine = [vec+pack[0] for vec in newspine]
            newspinelist.append(newspine)
            newvertslist.append(newverts)
            faceslist.append(newfaces)
    print('--')
    return newvertslist, newspinelist, newbranchdata

# THE MIGHTY TREE GENERATION
def tree_gen(m_p, b_p, bn_p, t_p, r_p):
    #initial trunk
    verts, faces, spine = trunk_gen(m_p, t_p, r_p, mathutils.Vector((0,0,1)))
    branchdata = [m_p]
    newvertslist = [verts]
    vertslist = [verts]
    faceslist = [faces]
    newspinelist = [spine]
    #generates branches on that trunk stored in new_lists temporarily
    #THIS CREATES BRANCH LEVELS
    if b_p[0] != 0:
        for i in range(b_p[0]):
            #THIS CREATES ONE BRANCH LEVEL
            #i update the starting parameters for the branches
            #now they will have reduced sides and reduced length
            for k in range(len(branchdata)):
                branchdata[k][0] = branchdata[k][0]//2 #sides update for every level
                if branchdata[k][0]<4:
                    branchdata[k][0]=4
                branchdata[k][1] *= 0.4
            newvertslist, newspinelist, branchdata = branch_gen(faceslist, newspinelist, branchdata, b_p, bn_p[i], t_p, r_p)
            vertslist += newvertslist #newlists are added to old lists and facelist is updated with new set
    #it is important that newvertslist is needed for new level of branches
    #faceslist is not, thats why it just gets updated instead of having newfaceslist

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


if __name__ == "__main__":
# place for testing
    s = 6
    r = 1
    l = 1
    n = 5
    print(face_gen(s, n))
