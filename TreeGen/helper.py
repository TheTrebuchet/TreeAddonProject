from math import ceil, floor
import random
def pseudo_poisson_disc(n, ratio, seed):
    result = []
    m = ceil((n/ratio)**0.5)
    k = ceil((n*ratio)**0.5)
    result = [[(i%m+0.5*(i//m%2))/m,(floor(i/m)+0.5)/k] for i in range(m*k)]
    for i in result:
        random.seed(seed)
        seed+=1
        i[0]+=0.3*random.uniform(-1,1)/m
        random.seed(seed)
        seed+=1
        i[1]+=0.3*random.uniform(-1,1)/k
    for i in range(m*k-n):
        random.seed(seed)
        seed+=1
        result.pop(random.randint(0,len(result)-1))
    print(len(result), n)
    return result

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    l=200
    r=10
    for ratio in range(1,10):
        xy = pseudo_poisson_disc(200,ratio,1)
        fig, ax = plt.subplots()
        ax.scatter([i[0] for i in xy], [i[1] for i in xy])
        plt.xlim(0,1)
        plt.ylim(0,1)
        plt.show()