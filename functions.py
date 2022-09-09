def circle(n,r):
    circle = []
    if n<3 or r==0:
        return []
    else:
        for i in range(n+1):
            circle.append((r*math.cos(2*math.pi*i/n), r*math.sin(2*math.pi*i/n))0)
