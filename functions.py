import math
import random
import mathutils

# SPINE

# number of vertices, length
def spine_init(n, length, l, p_a, p_s, p_seed):
    f1 = lambda z : p_a*(mathutils.noise.noise(mathutils.Vector([0, p_seed, p_s*z]))-0.5)
    f2 = lambda z : p_a*(mathutils.noise.noise(mathutils.Vector([0, p_seed, p_s*(z+length)]))-0.5)
    spine = [mathutils.Vector((f1(l*i), f2(l*i), l*i)) for i in range(n)]
    return spine

# bends the spine in a more meaningful way
def spine_bend(spine, b_a, b_s, b_seed, l):
    for i in range(1, len(spine)):
        rotz = mathutils.noise.noise((0, b_seed, i*l*b_s))
        rotx = b_a*(mathutils.noise.noise((0, b_seed+1, i*l*b_s)))
        
        #rotz correction for absurd angles
        vec = spine[i]- spine[i-1]
        x = vec.angle((0.0,0.0,1.0),0.0)/(2*math.pi)
        a = mathutils.Vector((-vec[0], -vec[1], 0.0)).angle((1.0,0.0,0.0),0.0)/(2*math.pi)
        rotz = (1-x)*rotz + x*(a)
        mat = mathutils.Matrix.Translation(-1*spine[i])
        mat = mat @ mathutils.Matrix.Translation(spine[i])
        mat = mat @ mathutils.Matrix.Rotation(2*math.pi*rotz, 4, 'Z')
        mat = mat @ mathutils.Matrix.Rotation(2*math.pi*rotx, 4, 'X')
        mat = mat @ mathutils.Matrix.Rotation(-2*math.pi*rotz, 4, 'Z')
        spine[i:] = [vec@mat for vec in spine[i:]]
    return spine

def spine_gen(m_p, r_p):
    #parameters
    sides, length, radius = m_p[:-1]
    p_a, p_s, p_seed, b_a, b_s, b_seed = r_p

    #number of circles in the tree
    n=int(length//(2*math.tan(2*math.pi/(2*sides))*radius))
    l = length/n

    #spine gen
    spine = spine_init(n, length, l, p_a, p_s, p_seed)
    spine = spine_bend(spine, b_a, b_s, b_seed, l)
    
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

def bark_gen(spine, l, n, m_p, s_p):
    
    #parameters
    sides, length, radius, scale = m_p
    a, d = s_p

    #tree-scale function, should be accessible from interface
    #function for scaling of individual circles, scale_list
    f = lambda x : a*(1/(d+x)-(d+length-x)/(d*(d+length)))+radius*(1-x/length)
    scale_list = [f(h*l) for h in range(n)]

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

def branch_guides(spine, verts, m_p, n, b_p):
    #parameters
    sides, scale = m_p[0], m_p[3]
    n_br, a_br, h_br, var_br = b_p
    trans = []
    guides = []
    guide_rel = [mathutils.Vector((0,0,0)), mathutils.Vector((0,0,0.1))]
    
    #guide_scale function, should be accessible from interface
    guide_f = lambda x : x
    #guide instructions
    for i in range(n_br):
        s_pick = random.randint(math.floor(n*h_br), n-1)
        v_pick = s_pick*sides+random.randint(0, sides-1)
        print(v_pick)
        trans_vec = verts[v_pick]
        quat = (mathutils.Vector((0,0,1))).rotation_difference(verts[v_pick]-spine[s_pick]*scale)
        for i in guide_rel:
            guides.append(tuple(trans_vec + (quat @ i)*guide_f(s_pick/n)))
    return guides






if __name__ == "__main__":
#place for testing
    s = 6
    r = 1
    l = 1
    n = 5
    print(bark_faces(s, n))
