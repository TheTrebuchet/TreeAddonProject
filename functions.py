import math
import mathutils
# number of sides, radius
def circle(n,r):
    circle = []
    if n<3 or r==0:
        return []
    else:
        for i in range(n):
            circle.append((r*math.cos(2*math.pi*i/n), r*math.sin(2*math.pi*i/n), 0))
    return circle

# number of vertices, length
def spine_gen(n, length, l, p_a, p_s, p_seed):
    f1 = lambda z : p_a*(mathutils.noise.noise(mathutils.Vector([0, p_seed, p_s*z]))-0.5)
    f2 = lambda z : p_a*(mathutils.noise.noise(mathutils.Vector([0, p_seed, p_s*(z+length)]))-0.5)
    spine = [mathutils.Vector((f1(l*i), f2(l*i), l*i)) for i in range(n)]
    return spine

# def spine_bend(spine, r_p)
def spine_bend(spine, r_p, length, l):
    b_a, b_s, b_seed = r_p[3:6]

    for i in range(len(spine)):
        rotz = mathutils.noise.noise((0, b_seed, i*l*b_s))
        rotx = b_a*(mathutils.noise.noise((0, b_seed+1, i*l*b_s)))
        print(rotx)
        mat_trans1 = mathutils.Matrix.Translation(-1*spine[i])
        mat_trans2 = mathutils.Matrix.Translation(spine[i])
        mat_rotz1 = mathutils.Matrix.Rotation(2*math.pi*rotz, 4, 'Z')
        mat_rotz2 = mathutils.Matrix.Rotation(-2*math.pi*rotz, 4, 'Z')
        mat_rotx = mathutils.Matrix.Rotation(2*math.pi*rotx, 4, 'X')
        mat = mat_trans1 @mat_rotz1 @ mat_rotx @ mat_rotz2 @ mat_trans2
        spine[i:] = [vec@mat for vec in spine[i:]]
    return spine
#number of sides, number of vertices, generates faces
def bark(s, n):
    faces = []
    for i in range(n-1):
        for j in range(s):
            if j != s-1:
                faces.append(tuple([j+s*i, j+1+s*i, j+1+(i+1)*s, j+(i+1)*s]))
            else:
                faces.append(tuple([j+s*i, s*i, s*(i+1), j+s*(i+1)]))
    return faces



'''
verts of the whole tree, combines multiple functions
1. makes a spine
2. modify spine to account for a bend
3.. for each 'n' create a circle
'''

def treegen(m_p, s_p, r_p):
    #parameters
    sides, length, radius, scale = m_p
    a, d = s_p
    p_a, p_s, p_seed = r_p[0:3]

    #number of circles in the tree
    n=int(length//(2*math.tan(2*math.pi/(2*sides))*radius))
    l = length/n

    #function for general shape
    f = lambda x : a*(1/(d+x)-(d+length-x)/(d*(d+length)))+radius*(1-x/length)
    scale_list = [f(h*l) for h in range(n)]

    #spine gen
    spine = spine_gen(n, length, l, p_a, p_s, p_seed)
    spine = spine_bend(spine, r_p, length, l)

    tree = []
    for x in range(n):
        for y in circle(sides,scale_list[x]):
            tree.append((mathutils.Vector(spine[x]) + mathutils.Vector(y))*scale)
    return tree, n

if __name__ == "__main__":
#place for testing
    s = 6
    r = 1
    l = 1
    n = 5
    print(bark(s, n))
