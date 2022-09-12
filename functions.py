import math

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
#number of sides, number of vertices
def bark(s, n):
    faces = []
    for i in range(n-1):
        for j in range(s):
            if j != s-1:
                faces.append(tuple([j+s*i, j+1+s*i, j+1+(i+1)*s, j+(i+1)*s]))
            else:
                faces.append(tuple([j+s*i, s*i, s*(i+1), j+s*(i+1)]))
    return faces


if __name__ == "__main__":
#place for testing
    s = 6
    r = 1
    l = 1
    n = 5
    print(bark(s, n))
