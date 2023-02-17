from math import ceil, floor
import math
import random
import time
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
    fig = plt.figure()
    h=200
    r=2
    l = (40**2+200**2)**0.5
    a = r/l
    plt.plot([0, math.pi*r],[0, l*math.cos(math.pi*a)], c='blue')
    plt.plot([0, -math.pi*r],[0, l*math.cos(math.pi*a)], c='blue')
    plt.plot([math.sin(math.pi*2*(-a/2+a*i/100))*l for i in range(0,100)], [math.cos(math.pi*2*(-a/2+a*i/100))*l for i in range(100)], c='blue')
    xy = pseudo_poisson_disc(200,l,r,1)
    plt.scatter([math.sin(i[0]*a)*i[1]*r for i in xy], [math.cos(i[0]*a)*i[1]*r for i in xy], s=0.1)
    plt.xlim(-math.pi*r, math.pi*r)
    plt.ylim(0,l+10)
    fig.set_figwidth(math.pi*2*r/50)
    fig.set_figheight(l/50)
    plt.show()