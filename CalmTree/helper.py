from math import ceil, floor, sin, cos
import math
import random
import time
from mathutils import Vector
def pseudo_poisson_disc(n, length, radius, seed):
    result = []
    for i in range(n):
        seed+=1
        random.seed(seed)
        h = random.uniform(0, length/radius)**0.5*(length/radius)**0.5
        seed+=1
        random.seed(seed)
        a = (random.uniform(-math.pi,math.pi))
        result.append((a,h))
    return result

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    def ptgen(sp, pt, radius):
            random.seed(sp)
            r = random.uniform(radius,2*radius)
            random.seed(sp+1)
            phi = random.uniform(-math.pi,math.pi)
            random.seed(sp+2)
            theta = random.uniform(-math.pi,math.pi)
            npt = Vector((r*cos(phi)*sin(theta), r*sin(phi)*sin(theta), r*cos(theta)))+pt
            return npt
    
    def check(npt, grid, radius, spine, bounds):
        if all([abs((npt-p).length) > bounds for p in spine]):
            return False
        
        for p in grid:
            if abs((npt-p).length) < radius:
                return False
        return True

    def poisson(spine, k):
        sp = 1
        radius = 0.4
        active = []
        grid = []
        bounds = 0.5
        active.append(Vector((0,0,0)))
        grid += spine
        active += spine

        while active:
            pt = active[-1]
            found = False
            for i in range(k):
                sp+=1
                npt = ptgen(sp, pt, radius)
                test = check(npt, grid, radius, spine, bounds)
                if test:
                    grid.append(npt)
                    found = True
            if not found:
                active.pop(-1)

        return grid
    '''
    #poisson 1.0
    st = time.time()
    print(pseudo_poisson_disc)
    print(time.time()-st)
    '''
    #poisson 2.0
    st = time.time()
    spine = [Vector((0,0,0.3*i)) for i in range(20)]
    grid = poisson(spine, 8)
    print(len(grid))
    print(time.time()-st)

    ax = plt.figure().add_subplot(projection='3d')
    ax.scatter([p[0] for p in grid], [p[1] for p in grid], [p[2] for p in grid])
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_zlim(0,6)
    plt.show()