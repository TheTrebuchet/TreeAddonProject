import math
import random
import mathutils
import bl_math

# SPINE

## number of vertices, length
def spine_init(n, length, l, p_a, p_s, p_seed, guide):
    ### quat rotates the spine, f1 and f2 jiggle the spine
    quat = mathutils.Vector((0,0,1)).rotation_difference(guide)
    f1 = lambda z : p_a*(mathutils.noise.noise(mathutils.Vector([0, p_seed, p_s*z]))-0.5)
    f2 = lambda z : p_a*(mathutils.noise.noise(mathutils.Vector([0, p_seed, p_s*(z+length)]))-0.5)
    spine = [quat@mathutils.Vector((f1(l*i), f2(l*i), l*i)) for i in range(n)]
    return spine

## bends the spine in a more meaningful way
def spine_bend(spine, b_a, b_ang, b_c, b_s, b_seed, l, guide):
    for i in range(1, len(spine)):
        noise = lambda b_a, b_seed, i, l, b_s: b_a*mathutils.noise.noise((0, b_seed, i*l*b_s))
        bend_vec = mathutils.Vector((noise(b_a, b_seed, i, l, b_s), noise(b_a, b_seed+10, i, l, b_s), 1)).normalized()
        
        ### correction for absurd angles
        vec = spine[i] - spine[i-1]
        x = bl_math.clamp(vec.angle(guide.normalized(),0.0)/math.radians(b_ang))**b_c**b_c
        vec = (guide.rotation_difference((0,0,1)))@vec
        bend_vec = bend_vec*(1-x) + mathutils.Vector((-vec[0],-vec[1], vec[2])).normalized()*x
        
        ### transformation itself
        trans1 = mathutils.Matrix.Translation(-1*spine[i])
        trans2 = mathutils.Matrix.Translation(spine[i])
        quat = mathutils.Vector(((0,0,1))).rotation_difference(bend_vec)
        spine[i:] = [trans2@(quat@(trans1@vec)) for vec in spine[i:]]

        ### correction for tree being completely sideways
    ''' 
    vec_c = spine[-1] - spine[0]
    quat = vec_c.rotation_difference(mathutils.Vector((0.0,0.0,1.0)))
    spine = [quat@i for i in spine]
    '''
    return spine

def spine_gen(m_p, r_p, guide):
    ### parameters
    sides, length, radius = m_p[:-1]
    p_a, p_s, p_seed, b_a, b_ang, b_c, b_s, b_seed = r_p

    ### number of circles in the tree
    n=int(length//(2*math.tan(2*math.pi/(2*sides))*radius))
    l = length/n

    ### spine gen
    spine = spine_init(n, length, l, p_a, p_s, p_seed, guide)
    spine = spine_bend(spine, b_a, b_ang, bl_math.clamp(b_c)*3.3, b_s, b_seed, l, guide)
    
    return spine, l, n


# BARK

## number of sides, radius
def bark_circle(n,r):
    circle = []
    if n<3 or r==0:
        return []
    else:
        for i in range(n):
            circle.append(mathutils.Vector((r*math.cos(2*math.pi*i/n), r*math.sin(2*math.pi*i/n), 0)))
    return circle

def bark_gen(spine, l, n, m_p, t_p, guide):
    ### generating quat to adjust first and last circle, matters for the branch only
    quat = mathutils.Vector((0,0,1)).rotation_difference(guide)
    ### parameters
    sides, length, radius = m_p[:-1]
    s_fun, f_a = t_p[:2]

    ### s_fun function, should be accessible from interface, scales the circles
    scale_list = [s_fun(h*l, length, radius, f_a) for h in range(n)]

    ### generating bark with scaling and rotation based on parameters and spine
    bark = [quat@i for i in bark_circle(sides,scale_list[0])]
    
    for x in range(1, n-1):
        vec = spine[x+1] - spine[x-1]
        quat = mathutils.Vector((0,0,1)).rotation_difference(vec)
        new_circle = [quat @ i for i in bark_circle(sides,scale_list[x])]
        for y in new_circle:
            bark.append((mathutils.Vector(spine[x]) + mathutils.Vector(y)))
    
    bark += [(quat@i + mathutils.Vector(spine[-1])) for i in bark_circle(sides,scale_list[-1])]
    return bark

##number of sides, number of vertices, generates faces
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

## outputs [place of the branch, vector that gives branch angle and size, radius of the branch]
def branch_guides(spine, verts, m_p, n, b_p, t_p):
    ### parameters
    sides = m_p[0]
    n_br, a_br, h_br, var_br = b_p
    scale_f, br_w, br_f = t_p[2:]
    guides = []
    guide_rel = [mathutils.Vector((0,0,0)), mathutils.Vector((0,0,0.1))]
    
    ### guide instructions
    for i in range(n_br):
        s_pick = random.randint(math.floor(n*h_br), n-1)
        v_pick = s_pick*sides+random.randint(0, sides-1)
        trans_vec = spine[s_pick]
        quat = mathutils.Quaternion(((mathutils.Vector((0,0,1))).cross(verts[v_pick]-spine[s_pick])).normalized(), math.radians(70))
        guide_vec = (quat @ mathutils.Vector((0,0,1)))*scale_f(s_pick/n, br_f, br_w)
        radius = (verts[v_pick]-spine[s_pick]).length
        guides.append([trans_vec, guide_vec, radius])
    return guides






if __name__ == "__main__":
### place for testing
    s = 6
    r = 1
    l = 1
    n = 5
    print(bark_faces(s, n))
