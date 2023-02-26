from math import sin, cos
import math
import random
from mathutils import Vector, Matrix

def pseudo_poisson_disc(n, length, radius, seed):
    result = []
    for i in range(n):
        seed+=1
        random.seed(seed)
        h = random.uniform(0, length/radius)**0.5*(length/radius)**0.5
        seed+=1
        a = (random.uniform(-math.pi,math.pi))
        result.append((a,h))
    return result

def ptgen(spine, radius, idx, scale_f1, flare, hor):
        pt = spine[idx]
        pt2 = spine[idx+1]
        x = random.random()
        origin = x*pt+(1-x)*pt2
        h = (idx+x)/len(spine)
        radius += scale_f1(h, flare)
        phi = random.uniform(-math.pi,math.pi)
        npt = Vector((0,0,1)).rotation_difference(pt2-pt)@Vector((radius*sin(phi), radius*cos(phi),0))
        if hor > 0.01:
            npt = (Matrix.Scale(0.0,4,(pt2-pt))@(npt*Vector((1,1,1-hor)))).normalized()
        
        return npt+origin, origin, h
    
def check(npt, grid, lim, idx, ran):
    current = [v for lis in grid[max(-ran, -len(grid)):] for v in lis]
    for p in current:
        if abs((npt-p).length) < lim:
            return False
    return True

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    #poisson 2.0
    for lim in range(1,30):
        k=7
        radius = 1
        grid = []
        ran = 5
        lim *= 0.1
        spine = [Vector((0.0, 0.0, 0.0)), Vector((-0.04053265228867531, 0.1525326669216156, 0.5666670203208923)), Vector((-0.05233679339289665, 0.2162090241909027, 1.1513268947601318)), Vector((0.08932508528232574, 0.07073953002691269, 1.7034058570861816)), Vector((0.3351735472679138, -0.1757250726222992, 2.1775729656219482)), Vector((0.603615939617157, -0.4416947364807129, 2.628371238708496)), Vector((0.9189794659614563, -0.7344887852668762, 3.0294179916381836)), Vector((1.2864696979522705, -1.0440350770950317, 3.3687584400177)), Vector((1.5507733821868896, -1.3234150409698486, 3.813856601715088)), Vector((1.4413506984710693, -1.4571164846420288, 4.376147747039795)), Vector((1.1136771440505981, -1.5123927593231201, 4.861530303955078)), Vector((0.7895124554634094, -1.5705634355545044, 5.3489251136779785)), Vector((0.40334513783454895, -1.6063776016235352, 5.791208267211914)), Vector((-0.05430370569229126, -1.612501621246338, 6.160719394683838)), Vector((-0.49577754735946655, -1.616670846939087, 6.549442768096924)), Vector((-0.767345666885376, -1.5683027505874634, 7.068993091583252)), Vector((-0.6747534275054932, -1.3740949630737305, 7.616468906402588)), Vector((-0.3822815418243408, -1.097188115119934, 8.04518985748291))]
        #grid = poisson()
        #print(test(grid, radius))
        print(len(grid))

        ax = plt.figure().add_subplot(projection='3d')
        ax.scatter([p[0] for p in grid], [p[1] for p in grid], [p[2] for p in grid])
        ax.scatter([p[0] for p in spine], [p[1] for p in spine], [p[2] for p in spine], c='red')
        ax.set_xlim(-5,5)
        ax.set_ylim(-5,5)
        ax.set_zlim(0,5)
        plt.show()