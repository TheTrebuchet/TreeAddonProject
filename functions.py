import math

def circle(n,r):
    circle = []
    if n<3 or r==0:
        return []
    else:
        for i in range(n):
            circle.append((r*math.cos(2*math.pi*i/n), r*math.sin(2*math.pi*i/n), 0))
    return circle

if __name__ == "__main__":
    print(circle(4,1))
