import math
import random
import mathutils
import bl_math

# SPINE

# number of vertices, length
def spine_init(n, length, l, p_a, p_s, p_seed):
    f1 = lambda z : p_a*(mathutils.noise.noise(mathutils.Vector([0, p_seed, p_s*z]))-0.5)
    f2 = lambda z : p_a*(mathutils.noise.noise(mathutils.Vector([0, p_seed, p_s*(z+length)]))-0.5)
    spine = [mathutils.Vector((f1(l*i), f2(l*i), l*i)) for i in range(n)]
    return spine

# bends the spine in a more meaningful way
def spine_bend(spine, b_a, b_m, b_s, b_seed, l):
    for i in range(1, len(spine)):
        rotz = mathutils.noise.noise((0, b_seed, i*l*b_s))
        rotx = b_a*(mathutils.noise.noise((0, b_seed+1, i*l*b_s)))**2

        #rotz correction for absurd angles
        vec = spine[i]- spine[i-1]
        x = bl_math.clamp(vec.angle((0.0,0.0,1.0),0.0)/math.radians(b_m))
        a = (-(math.atan2(vec[0], vec[1])/(2*math.pi) + 0.5)+2.25)%1
        rotz = (1-x)*rotz + x*(a)
        print(rotz)
        #transformation itself
        trans1 = mathutils.Matrix.Translation(-1*spine[i])
        trans2 = mathutils.Matrix.Translation(spine[i])
        quat = mathutils.Quaternion(mathutils.Vector((math.cos(2*math.pi*rotz+math.pi/2), math.sin(2*math.pi*rotz+math.pi/2), 0)), rotx)
        spine[i:] = [trans2@(quat@(trans1@vec)) for vec in spine[i:]]
    return spine

def spine_gen(m_p, r_p):
    #parameters
    sides, length, radius = m_p[:-1]
    p_a, p_s, p_seed, b_a, b_m, b_s, b_seed = r_p

    #number of circles in the tree
    n=int(length//(2*math.tan(2*math.pi/(2*sides))*radius))
    l = length/n

    #spine gen
    spine = spine_init(n, length, l, p_a, p_s, p_seed)
    spine = spine_bend(spine, b_a, b_m, b_s, b_seed, l)
    
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

def bark_gen(spine, l, n, m_p, t_p):
    
    #parameters
    sides, length, radius, scale = m_p
    s_fun, f_a = t_p[:2]

    #tree-scale function, should be accessible from interface
    #function for scaling of individual circles, scale_list
    scale_list = [s_fun(h*l, length, radius, f_a) for h in range(n)]

    #generating bark with scaling and rotation based on parameters and supplied spine
    bark = [i*scale for i in bark_circle(sides,scale_list[0])]
    for x in range(1, n-1):
        vec = spine[x+1] - spine[x-1]
        quat = mathutils.Vector((0,0,1)).rotation_difference(vec)
        new_circle = [quat @ i for i in bark_circle(sides,scale_list[x])]
        for y in new_circle:
            bark.append((mathutils.Vector(spine[x]) + mathutils.Vector(y))*scale)
    bark += [(i + mathutils.Vector(spine[-1]))*scale for i in bark_circle(sides,scale_list[-1])]
    return bark

#number of sides, number of vertices, generates faces
def bark_faces(s, n):
    faces = []
    for i in range(n-1):
        for j in range(s):
            if j != s-1:
                faces.append(tuple([j+s*i, j+1+s*i, j+1+(i+1)*s, j+(i+1)*s]))
            else:
                faces.append(tuple([j+s*i, s*i, s*(i+1), j+s*(i+1)]))
    return faces

# BRANCHES

def branch_guides(spine, verts, m_p, n, b_p, t_p):
    #parameters
    sides, scale = m_p[0], m_p[3]
    n_br, a_br, h_br, var_br = b_p
    scale_f, br_w, br_f = t_p[2:]
    guides = []
    guide_rel = [mathutils.Vector((0,0,0)), mathutils.Vector((0,0,0.1))]
    
    #guide instructions
    for i in range(n_br):
        s_pick = random.randint(math.floor(n*h_br), n-1)
        v_pick = s_pick*sides+random.randint(0, sides-1)
        trans_vec = verts[v_pick]
        quat = mathutils.Quaternion(((mathutils.Vector((0,0,1))).cross(verts[v_pick]-spine[s_pick]*scale)).normalized(), math.radians(45))
        for i in guide_rel:
            guides.append(tuple(trans_vec + (quat @ i)*scale_f(s_pick/n, br_f, br_w)))
    return guides






if __name__ == "__main__":
#place for testing
    s = 6
    r = 1
    l = 1
    n = 5
    print(bark_faces(s, n))
