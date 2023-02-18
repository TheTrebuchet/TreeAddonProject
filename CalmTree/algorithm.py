import math
import random
from mathutils import Vector, noise, Matrix, Quaternion
import bl_math
from .helper import *

def spine_add(spine, l, guide):
    lensp = len(spine)
    if lensp<3:
        spine.append(Vector((0,0,1)).rotation_difference(guide)@Vector((0,0,l))+spine[-1])
    else:
        spine.append(l*(2*spine[-1] - spine[-2]).normalized()+spine[-1])

# bends the spine in a more meaningful way
def spine_bend(spine, n, bd_p, l, guide):
    b_a, b_up, b_c, b_s, b_w, b_seed = bd_p
    f_noise = lambda i, b_seed: b_a*noise.noise((0, b_seed, i*l*b_s))
    
    old_vec = spine[-2] - spine[-3] #get previous vector
    angle = (Vector((0,0,1)).angle(old_vec)) #calculate global angle
    quat = Quaternion(Vector((old_vec[1], -old_vec[0],0)), b_up*angle/(n-len(spine)+1)) #ideal progression
    new_vec = quat@old_vec
    
    bend_vec = Vector((f_noise(len(spine)-2, b_seed), f_noise(len(spine)-2, b_seed+10), 1)).normalized() #generate random vector        
    bend_vec = (Vector((0,0,1)).rotation_difference(new_vec))@bend_vec #rotating bend_vec to local direction
    x = bl_math.clamp(guide.angle(bend_vec,0.0)/math.radians(90))**2 #apply dampening, to be improved
    new_vec = bend_vec*(1-x) + new_vec.normalized()*x #mixing between random (bend_vec) and ideal (new_vec) vectors

    # transformation itself, rotating the remaining branch towards the new vector
    trans1 = Matrix.Translation(-1*spine[-2])
    trans2 = Matrix.Translation(spine[-2])
    quat = old_vec.rotation_difference(new_vec)
    spine[-1] = (trans2@(quat@(trans1@spine[-1])))
    return spine

def spine_weight(spine, n, l, r, trunk, bd_p):
    b_c, b_w = bd_p[2], bd_p[4]

    weight = lambda x, ang: math.sin(ang)*(1-x)*l*n #it has influences from trunk working cross section, weight of the branch (without child-branches), angle of the branch

    for i in range(n-2):
        vec = spine[i] - spine[i-1] #get previous vector
        angle = (Vector((0,0,1)).angle(vec))
        CM_lis = [spine[v]*(1-(v)/n) for v in range(i+1,n)]
        CM = Vector((0,0,0))
        for v in CM_lis:
            CM += v
        CM = CM/((n-i-1)*(n-i)/(2*n))-spine[i]
        w_angle = CM[0]**2+CM[1]**2-(r*math.cos(angle))**2
        if w_angle<0: w_angle = 0
        w_angle = weight(i/n, math.atan(w_angle**0.5/(CM[2]+r*math.sin(angle))))
        
        trans1 = Matrix.Translation(-1*spine[i])
        trans2 = Matrix.Translation(spine[i])
        quat = Quaternion(Vector((vec[1], -vec[0],0)), -w_angle*b_w)
        spine[i:] = [trans2@(quat@(trans1@vec)) for vec in spine[i:]]

    if trunk:
        CM = Vector([sum([i[0] for i in spine])/n, sum([i[1] for i in spine])/n, sum([i[2] for i in spine])/n])
        quat = Quaternion(Vector((CM[1],-CM[0],0)), Vector((0,0,1)).angle(CM)*b_c)
        spine[:] = [quat@i for i in spine]

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
    chosen = pseudo_poisson_disc(number, length, radius, br_seed)

    # guide instructions
    for i in range(number):
        height = chosen[i][1]*radius/length*(1-start_h)+start_h
        pick = math.floor(n*height)
        trans_vec = spine[pick]*(height*n-pick)+spine[pick]*(pick+1-height*n) #translation vector

        random.seed(br_seed+1) #x axis angle
        x = (height-start_h)/(1-start_h)
        ang = minang*x+maxang*(1-x)
        ang += random.uniform(-var*ang,var*ang)

        a = chosen[i][0]

        quat = Vector((0,0,1)).rotation_difference(spine[pick]-spine[pick-1]) #quaternion from 001 to vector alongside the spine
        dir_vec = Vector((math.sin(ang)*math.cos(a),math.sin(ang)*math.sin(a), math.cos(ang))).normalized() #bent vector from 001
        guide_vec = quat @ dir_vec #final guide
        guide_vec *= length*scaling*scale_f2(x, shift)*random.uniform(1-var, 1+var) #guide length update
        guide_r = bl_math.clamp(scale_f1(height, flare)*radius*0.8, tipradius, guide_vec.length/length*radius) #radius of the new branch between 1% and proportionate of parent
        guidepacks.append((trans_vec, guide_vec, guide_r)) #creating guidepack
    return guidepacks

#generates a single trunk, whether it will be branch or the main trunk
class branch():
    def __init__(self, pack, m_p, bd_p, br_p, r_p, trunk):
        self.pack = pack
        self.mp = [m_p[0], self.pack[1].length, self.pack[2], m_p[3], m_p[4], bl_math.clamp(m_p[5], 0, self.pack[1].length/2)]
        self.bdp = bd_p
        self.brp = br_p
        self.rp = r_p
        self.trunk = trunk
        self.guidepacks=[]
        self.n = 0
        self.spine=[]
        
    def generate(self):
        self.n = round(self.mp[1]/self.mp[5])+1
        self.spine = [Vector((0,0,0))]
        spine_add(self.spine, self.mp[5], self.pack[1])

        while len(self.spine)<self.n:
            spine_add(self.spine, self.mp[5], self.pack[1])
            spine_bend(self.spine, self.n, self.bdp, self.mp[5], self.pack[1])
        spine_jiggle(self.spine, self.mp[5], self.mp[1], self.rp)
        spine_weight(self.spine, self.n, self.mp[5], self.mp[2], self.trunk, self.bdp)

        self.spine = [vec+self.pack[0] for vec in self.spine]
        return self
    
    def regenerate(self):
        for i in range(self.n-2):
            spine_bend(self.spine, self.n, self.bdp, self.mp[5], self.pack[1])
        spine_jiggle(self.spine, self.mp[5], self.mp[1], self.rp)
        spine_weight(self.spine, self.n, self.mp[5], self.mp[2], self.trunk,self.bdp)
    
    def guidesgen(self, number, t_p):
        self.childmp = [int(bl_math.clamp(self.mp[0]//2+1, 4, self.mp[0])), self.mp[1], self.mp[2], self.mp[3], self.mp[4], self.mp[5]]
        self.guidepacks = guides_gen(self.spine, number, self.mp, self.brp, t_p)

# THE MIGHTY TREE GENERATION

def outgrow(branchlist, br_p, bn_p, bd_p, r_p, t_p):
    #creating the rest of levels
    for lev in range(br_p[0]):
        branchlist.append([])
        for parent in branchlist[-2]:
            parent.guidesgen(bn_p[lev], t_p)
            children = parent.guidepacks
            for pack in children:
                r_p[2] +=1
                bd_p[-1] +=1
                br_p[-1] +=1
                branchlist[-1].append(branch(pack, parent.childmp, bd_p, br_p, r_p, False).generate())
    return branchlist

def toverts(branchlist, facebool, m_p, br_p, t_p):
    #if the user doesn't need faces I provide only a spine
    if not facebool:
        verts = []
        edges =[]
        for lev in branchlist:
            for bran in lev:
                verts.extend(bran.spine)
                if edges: edges += [[n+edges[-1][1]+1,n+2+edges[-1][1]] for n in range(len(bran.spine))][:-1]
                else: edges += [(n,n+1) for n in range(len(bran.spine))][:-1]
        verts = [vec*m_p[4] for vec in verts] #scale update
        return verts, edges, [], []
    
    faces=[]

    #generating faces, needs branches
    for lev in range(br_p[0]+1):
        for bran in branchlist[lev]:
            faces.append(face_gen(bran.mp[0], bran.n))
    #combining faces
    while True:
        if len(faces) == 1:
            faces = faces[0]
            break
        faces[0].extend([[i+max(faces[0][-1])+1 for i in tup] for tup in faces.pop(1)])
    
    #generating verts from spine and making selection
    verts = []
    selection=[0]
    for lev in range(len(branchlist)):
        if lev == len(branchlist)-1:
            selection[0] = len(verts)
        for bran in branchlist[lev]:
            verts.extend(bark_gen(bran.spine, bran.mp, t_p))
    selection = list(range(selection[0], len(verts)))

    #flattening the base, 
    for lev in range(m_p[0]):
        verts[lev][2] = 0

    #scaling the tree
    verts = [vec*m_p[4] for vec in verts]
    
    return verts, [], faces, selection

def branchinit(verts, m_p, bd_p, br_p, r_p):
    m_p[3]*=m_p[2]
    st_pack = (verts[0],(verts[1]-verts[0]).normalized()*m_p[1], m_p[2])
    bran = branch(st_pack, m_p, bd_p, br_p, r_p, True)
    bran.n = len(verts)
    bran.spine = verts
    bran.regenerate()
    return [[bran]]