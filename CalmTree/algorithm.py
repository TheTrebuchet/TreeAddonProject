import math
from math import floor, ceil
import random
from mathutils import Vector, noise, Matrix, Quaternion
from .helper import *

def clamper(x):
    return max(0,min(x,1))

# bends the spine in a more meaningful way
def spine_bend(spine, n, bd_p, l, guide, quatmode=False, nfactor=False):
    b_a, b_up, b_c, b_s, b_w, b_seed = bd_p
    f_noise = lambda i, b_seed: b_a*noise.noise((0, b_seed, i*l*b_s))
    old_vec = spine[-2] - spine[-3] #get previous vector
    angle = (Vector((0,0,1)).angle(old_vec)) #calculate global angle
    progress = 0
    if nfactor: progress = b_up*angle/n
    else: progress = b_up*angle/(n-len(spine)+1)
    quat = Quaternion(Vector((old_vec[1], -old_vec[0],0)), progress) #ideal progression
    new_vec = quat@old_vec
    
    bend_vec = Vector((f_noise(len(spine)-2, b_seed), f_noise(len(spine)-2, b_seed+10), 1)).normalized() #generate random vector        
    bend_vec = (Vector((0,0,1)).rotation_difference(new_vec))@bend_vec #rotating bend_vec to local direction
    x = clamper(guide.angle(bend_vec,0.0)/math.radians(90))**2 #apply dampening, to be improved
    new_vec = bend_vec*(1-x) + new_vec.normalized()*x #mixing between random (bend_vec) and ideal (new_vec) vectors

    # transformation itself, rotating the remaining branch towards the new vector
    quat = old_vec.rotation_difference(new_vec)
    if quatmode:
        return quat
    spine[-1] = quat@(spine[-1]-spine[-2])+spine[-2]
    return spine

def spine_weight(spine, n, l, r, trunk, bd_p):
    b_c, b_w = bd_p[2], bd_p[4]

    weight = lambda x, ang: math.sin(ang)*(1-x)*l*n #it has influences from trunk working cross section, weight of the branch (without child-branches), angle of the branch

    for i in range(n-2):
        vec = spine[i] - spine[i-1] #get previous vector
        angle = (Vector((0,0,1)).angle(vec))
        CM_lis = [spine[v]*(1-(v)/n) for v in range(i+1,n)]
        cm_point = Vector((0,0,0))
        for v in CM_lis:
            cm_point += v
        cm_point = cm_point/((n-i-1)*(n-i)/(2*n))-spine[i]
        w_angle = cm_point[0]**2+cm_point[1]**2-(r*math.cos(angle))**2
        if w_angle<0: w_angle = 0
        w_angle = weight(i/n, math.atan(w_angle**0.5/(cm_point[2]+r*math.sin(angle))))
        
        trans1 = Matrix.Translation(-1*spine[i])
        trans2 = Matrix.Translation(spine[i])
        quat = Quaternion(Vector((vec[1], -vec[0],0)), -w_angle*b_w)
        spine[i:] = [trans2@(quat@(trans1@vec)) for vec in spine[i:]]

    if trunk:
        cm_point = Vector([sum([i[0] for i in spine])/n, sum([i[1] for i in spine])/n, sum([i[2] for i in spine])/n])
        quat = Quaternion(Vector((cm_point[1],-cm_point[0],0)), Vector((0,0,1)).angle(cm_point)*b_c)
        spine[:] = [quat@i for i in spine]
    
    return spine

def spine_jiggle(spine, l, length, rp):
    p_a, p_s, p_seed = rp
    jigf = lambda z : p_a*(noise.noise(Vector([0, p_seed, p_s*z]))-0.5)
    st = spine[1]-spine[0]
    ref = []
    if st[0]!=st[1]:
        ref = st.cross(Vector((st[1],-st[0],0))).normalized()
    else:
        ref = st.cross(Vector((st[2],0,-st[0]))).normalized()
    for i in range(1,len(spine)):
        x = (st.rotation_difference(spine[i]-spine[i-1])@ref).normalized()
        y = x.cross(spine[i]-spine[i-1]).normalized()
        spine[i]+=x*(jigf(i*l)-jigf(0)) + y*(jigf(i*l+length)-jigf(length))
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

def bark_gen(branchlist, pars):
    # generating verts from spine and making info, selection
    # info should be [startingvert, lastvert, sides]
    # selection should be verts that should have leaves
    leaffactor = pars.e_p[3]
    verts = []
    info = []
    selection = []
    additive = 0
    for bran in branchlist:
        leafpoints = floor(bran.n*min(1, leaffactor*pars.m_p[1]/bran.length)) #number of points to generate leaves from
        selection.extend(range(bran.n*bran.sides-1-leafpoints*bran.sides+additive, additive+bran.n*bran.sides-1))
        info.append([additive, additive+bran.n*bran.sides-1, bran.sides])
        
        quat = Vector((0,0,1)).rotation_difference(bran.direction) #first quat
        circle = bark_circle(bran.sides, bran.radius)
        verts.extend([(quat@i)+bran.spine[0] for i in circle]) #first circle
        quat = Vector((0,0,1)).rotation_difference(bran.spine[2]-bran.spine[0]) #second quat
        circle = bark_circle(bran.sides, bran.scalelist[1])
        verts.extend([(quat@i)+bran.spine[1] for i in circle]) #second circle
        for k in range(2,bran.n-1):
            quat = (bran.spine[k]-bran.spine[k-2]).rotation_difference(bran.spine[k+1]-bran.spine[k-1])@quat
            circle = bark_circle(bran.sides,bran.scalelist[k])
            verts.extend([(quat@i)+bran.spine[k] for i in circle])
        circle = bark_circle(bran.sides,bran.scalelist[-1])
        verts.extend([(quat@i)+bran.spine[-1] for i in circle])

        additive+=bran.n*bran.sides #for info and selection in next bran
    return verts, selection, info

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

def guides_fancy(spine, m_p, pars, lev, p_prog, scalelist):
    """
    uses functions from helper file
    check for checking if the point is valid
    ptgen for generating new point
    goes top to bottom
    total fucking mess
    """
    lim = 1/pars.bn_p[lev]
    p_length, p_radius, p_tipradius = m_p[1:4]
    minang, maxang, start_h, hor_factor, var, scaling, sd = pars.br_p[1:]
    qual = pars.e_p[2]
    scale_f2 = pars.scale_f2
    
    if p_radius == p_tipradius: #see if there is any point to this, should be outside of this function
        return []
    
    #no need for the base and the tip, should speed up iteration
    total_idx = len(spine)-1
    cutoff_idx = floor(start_h*len(spine))
    spine = spine[cutoff_idx:]
    idx = len(spine)-2
    
    random.seed(sd) #seems to be necessary
    
    grid = [[]] #guides with global coordinates, for the algorithm
    guides = [] #guides with local coordinates
    orgs = [] #origins of the branches
    h_glob = [] #height factor, from bottom to the top
    h_loc = [] #height factor, from startlength to the top
    steric_dist = 1/3*p_length*scaling #distance at which branches get too close
    ran = ceil(len(spine)/4) #range to verify the generated branches
    
    #this generates the new branches
    while idx>=0:
        found = False
        for i in range(qual):
            npt_global, npt_local, origin, x = ptgen(spine, steric_dist+scalelist[idx], idx, hor_factor)
            if check(npt_global, grid, lim, idx, ran):
                grid[-1].append(npt_global) #for the algorithm
                guides.append(npt_local) #for the result
                orgs.append(origin) #for the result
                h_glob.append((cutoff_idx+idx+x)/total_idx) #for the result, represents the factor of height on the total spine
                h_loc.append((idx+x)/(total_idx-cutoff_idx))
                found = True
        if not found:
            idx-=1
            grid.append([])

    set_length = lambda hloc : p_length*scaling*scale_f2(hloc)
    guides = [guides[i]*set_length(h_loc[i]) for i in range(len(guides))] #making local guides, adjusting length
    scalemix = lambda x: ((x%1)*scalelist[floor(x*total_idx)]+(1-x%1)*scalelist[ceil(x*total_idx)])
    radii = lambda hglob, guide_l: min(max(scalemix(hglob), p_tipradius), guide_l/p_length*p_radius)

    #further adjusting angles to match the set gradient from top to bottom, with randomization
    for i in range(len(guides)):
        hl = h_loc[i]
        ang = (math.pi/2-(hl*minang+(1-hl)*maxang))*random.uniform(1-var,1+var)
        guides[i] = (Quaternion((spine[floor(hl)]-spine[ceil(hl)]).cross(guides[i]), ang)@guides[i])*random.uniform(1-var, 1+var)
    
    #putting in the [origin point, local guide point, radius, length, progress] in separate guidepacks
    guidepacks = [[orgs[i], guides[i], radii(h_glob[i], guides[i].length), h_glob[i]*p_length+p_prog] for i in range(len(guides))] #creating guidepacks and radii
    return guidepacks

def guides_fast(spine, number, m_p, br_p, t_p):
    #uses pseudo_poisson_disc in helper
    n = len(spine)
    length, radius, tipradius = m_p[1:4]
    minang, maxang, start_h, horizontal, var, scaling, br_seed = br_p[1:]
    scale_f1, flare, scale_f2, shift = t_p
    guidepacks = []
    random.seed(br_seed)
    chosen = pseudo_poisson_disc(number, length, radius)
    for i in range(number):
        height = chosen[i][1]*radius/length*(1-start_h)+start_h
        pick = math.floor(n*height)
        trans_vec = spine[pick]*(height*n-pick)+spine[pick]*(pick+1-height*n)
        x = (height-start_h)/(1-start_h)
        ang = minang*x+maxang*(1-x)
        ang += random.uniform(-var*ang,var*ang)
        a = chosen[i][0]
        quat = Vector((0,0,1)).rotation_difference(spine[pick]-spine[pick-1])
        dir_vec = Vector((math.sin(ang)*math.cos(a),math.sin(ang)*math.sin(a), math.cos(ang))).normalized()
        guide_vec = quat @ dir_vec
        guide_vec *= length*scaling*scale_f2(x, shift)*random.uniform(1-var, 1+var)
        guide_r = clamper(scale_f1(height, flare)*radius*0.8, tipradius, guide_vec.length/length*radius)
        guidepacks.append((trans_vec, guide_vec, guide_r))
    return guidepacks