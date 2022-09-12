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
def spine(n, l):
    spine = [(0, 0, l*i) for i in range(n)]
    return spine
# vertices, number of sides, number of circles
def bark(verts, s, n):
    faces =[]
    for x in range(0,n):
        for x in range(s):
                faces.append(tuple())
    return faces



if __name__ == "__main__":
#place for testing
    n = 4
    r = 1
    l = 1
    tree = []
    for x in spine(n, l):
        for y in circle(n,r):
            tree.append(tuple(mathutils.vector(x) + mathutils.vector(y)))
    print(tree)
