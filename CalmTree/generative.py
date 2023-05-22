from .algorithm import *

def guidetry(spine, l, total, length, prog, stlen, R):
    pt1=spine[-1]
    pt2=spine[-2]
    h = random.random()
    hloc = (h*l+total)/(length-prog)
    hglob = (h*l+total+prog)/(length)
    hstart = (h*l+total+prog-stlen)/(length+prog-stlen)
    origin = (1-h)*pt1+h*pt2
    phi = random.uniform(-math.pi,math.pi)
    direction = R*(Vector((0,0,1)).rotation_difference(pt1-pt2)@Vector((sin(phi), cos(phi),0)))
    surface = direction+origin
    axis = direction.cross(pt1-pt2)
    return origin, surface, hloc, hglob, hstart, axis, h

class guide():
    def __init__(self, origin, surface, hloc, hglob, hstart):
        self.origin = origin
        self.hloc = hloc
        self.hglob = hglob
        self.hstart = hstart
        self.surface = surface
        self.direct = (self.surface-self.origin).normalized()
        self.quat = 0

    def prerequisits(self, length, prog, baseR, tipradius, scale_f1, flare, scale_f2, shift):
        tipmod = (1-self.hglob)*length*scale_f2(self.hstart,shift) #the shortened length of the new guide
        self.lenmod = tipmod+self.hglob*length #the new length of the whole path
        self.R = min(max(tipmod*baseR/(length-prog), tipradius), 0.9*scale_f1(self.hglob, flare)*baseR)
        self.ratio = self.R/(scale_f1(self.hglob, flare)*baseR)
        
    def generate(self, length):
        #at this point surface isn't relevant anymore
        return [self.origin,self.quat@self.direct*self.lenmod, self.R, self.hglob*length]


class branch():
    def __init__(self, pack, m_p, bd_p, br_p, r_p, trunk):
        self.pack = pack
        self.mp = [m_p[0], self.pack[1].length, self.pack[2], m_p[3], m_p[4], min(m_p[5], self.pack[1].length/2)]
        self.bdp = bd_p
        self.brp = br_p
        self.rp = r_p
        self.trunk = trunk
        self.guidepacks=[]
        self.n = 0
        self.spine=[]
        self.progress=0
    def generate(self):
        self.n = round(self.mp[1]/self.mp[5])+1
        self.spine = [Vector((0,0,0))]
        self.spine.append((self.pack[1].normalized())*self.mp[5])

        while len(self.spine)<self.n:
            self.spine.append(self.mp[5]*((self.spine[-1] - self.spine[-2]).normalized())+self.spine[-1])
            self.spine = spine_bend(self.spine, self.n, self.bdp, self.mp[5], self.pack[1])
        self.spine = spine_jiggle(self.spine, self.mp[5], self.mp[1], self.rp)
        self.spine = spine_weight(self.spine, self.n, self.mp[5], self.mp[2], self.trunk, self.bdp)

        self.spine = [vec+self.pack[0] for vec in self.spine]
        return self
    
    def generate_dynamic(self, lim, t_p, qual, Ythr, Tthr, startlength, baseR):
        print('new branch')
        length, radius, tipradius = self.mp[1:4]
        l = self.mp[5]
        minang, maxang, start_h, hor, var, scaling, sd = self.brp[1:]
        scale_f1, flare, scale_f2, shift = t_p
        
        
        self.spine = [self.pack[0]]
        self.spine.append((self.pack[1].normalized())*l+self.spine[0])
        total = l
        if self.progress<startlength:
            stn = int(abs(startlength-self.progress)//l)
            total += l*stn
            for i in range(stn):
                self.spine.append(l*((self.spine[-1] - self.spine[-2]).normalized())+self.spine[-1])
                self.spine = spine_bend(self.spine, self.n, self.bdp, l, self.pack[1])
        random.seed(sd)
        allbrans = [guide(self.pack[0], self.pack[0], 0, 0, 0)] #adding new guide object
        while total<length-self.progress:
            print('normal progress')
            quatM = 0
            if length-total-self.progress>Tthr: #check if that is the end of branch
                for i in range(qual): 
                    workingR = scale_f1(total/length-self.progress, flare)*baseR
                    origin, surface, hloc, hglob, hstart, axis, h = guidetry(self.spine, l, total, length, self.progress, startlength, workingR)
                    if (surface-allbrans[-1].surface).length>lim(hstart): #check for valid branches
                        print('found branch')
                        guess = guide(origin, surface, hloc, hglob, hstart)
                        guess.prerequisits(length, self.progress, baseR, tipradius, scale_f1, flare, scale_f2, shift)
                        ang = guess.hglob*minang+(1-guess.hglob)*maxang
                        if guess.ratio>Ythr:
                            print('split')
                            self.spine[-1] = origin
                            total-=(1-h)*l
                            quatM = Quaternion(axis,ang*guess.ratio/2)
                            guess.quat = Quaternion(axis,(math.pi/2-ang)+guess.ratio*ang/2)
                        else:
                            print('no split')
                            guess.quat = Quaternion(axis,(math.pi/2-ang))
                        allbrans.append(guess)
                        break
            addition = l*(self.spine[-1]-self.spine[-2]).normalized()
            if quatM:
                addition = quatM@addition
            self.spine.append(addition+self.spine[-1])
            self.spine = spine_bend(self.spine, int((length-self.progress-total)//l)+1, self.bdp, l, self.pack[1], nfactor=True)
            total+=l
            print(total)
        print('done')
        #weight everything
        self.spine = spine_jiggle(self.spine, self.mp[5], self.mp[1], self.rp)
        self.n = len(self.spine)
        self.guidepacks = [g.generate(length) for g in allbrans[1:]]
        print('branch finished')
    
    def regenerate(self):
        for i in range(2, self.n-1):
            quat = spine_bend(self.spine[i-2:i+1], self.n, self.bdp, self.mp[5], self.pack[1], quatmode=True)
            self.spine[i:] = [quat@(self.spine[k]-self.spine[i-1])+self.spine[i-1] for k in range(i,len(self.spine))]
        self.spine = spine_jiggle(self.spine, self.mp[5], self.mp[1], self.rp)
        self.spine = spine_weight(self.spine, self.n, self.mp[5], self.mp[2], self.trunk,self.bdp)
    
    def guidesgen(self, density, t_p, typ, qual):
        self.childmp = [int(max(self.mp[0]//2+1, 3)), self.mp[1], self.mp[2], self.mp[3], self.mp[4], self.mp[5]]
        if typ == 'fancy':
            self.guidepacks = guides_gen(self.spine, 1/density, self.mp, self.brp, t_p, qual)
        elif typ == 'fast':
            num = lambda d, l: ceil((2.2*l+11)*d**(1.37*l**0.1))
            self.guidepacks = fastguides_gen(self.spine, num(density, self.mp[1]), self.mp, self.brp, t_p)
    
    def interpolate(self, lev):
        if len(self.spine)>3:
            sp = self.spine
            a=0.1
            for l in range(lev):
                pt = (0.5+a)*sp[1]+(0.5+a)*sp[2]-a*(sp[0]+sp[3])
                sp.insert(2, pt)
                i = 3
                while i<len(sp)-2:
                    pt = (0.5+a)*sp[i]+(0.5+a)*sp[i+1]-a*(sp[i-2]+sp[i+2])
                    sp.insert(i+1, pt)
                    i+=2
            self.spine = sp
            self.n = len(sp)

# THE MIGHTY TREE GENERATION

def outgrow(branchlist, br_p, bn_p, bd_p, r_p, t_p, e_p):
    #creating the rest of levels
    for lev in range(br_p[0]):
        branchlist.append([])
        for parent in branchlist[-2]:
            parent.guidesgen(bn_p[lev], t_p, e_p[1], e_p[2])
            children = parent.guidepacks
            for pack in children:
                r_p[2] +=1
                bd_p[-1] +=1
                br_p[-1] +=1
                branchlist[-1].append(branch(pack, parent.childmp, bd_p, br_p, r_p, False).generate())
        br_p[3]=br_p[3]**2 #temporary workaround
    br_p[3]=br_p[3]**((0.5)**br_p[0]) 
    return branchlist

def outgrow_dynamic(ready, lim, m_p, br_p, bd_p, r_p, t_p, e_p, d_p):
    tobuild = ready[0].guidepacks.copy()
    startlength = m_p[1]*br_p[3]
    trunkradius = m_p[2]

    random.seed(bd_p[-1])
    while tobuild:
        gp = tobuild.pop(0)
        tmp = m_p.copy()
        tmp[0] = max(4,round(m_p[0]*gp[2]/m_p[2])) #adjusting sides
        tbrp = br_p.copy()
        bran = branch(gp, tmp, bd_p, tbrp, r_p, False)
        bran.progress = gp[3]

        if bran.mp[1]>d_p[1]:
            bran.generate_dynamic(lim, t_p, e_p[2],d_p[0],d_p[1], startlength, trunkradius)
            tobuild.extend(bran.guidepacks)
        else:
            bran.generate()
        
        ready.append(bran)

    return ready

def toverts(branchlist, facebool, m_p, br_p, t_p, e_p):
    #reorganising branchlist
    for lev in range(len(branchlist)-1):
        bran_i = 0
        while bran_i<len(branchlist[lev]):
            if branchlist[lev][bran_i].mp[2]==branchlist[lev][bran_i].mp[3]:
                branchlist[-1].insert(0, branchlist[lev].pop(bran_i))
            else:bran_i+=1


    #IF NOT FACEBOOL
    if not facebool:
        verts = []
        edges =[]
        for lev in branchlist:
            for bran in lev:
                if e_p[0]!=0:bran.interpolate(e_p[0])
                verts.extend(bran.spine)
                if edges: edges += [[n+edges[-1][1]+1,n+2+edges[-1][1]] for n in range(len(bran.spine))][:-1]
                else: edges += [(n,n+1) for n in range(len(bran.spine))][:-1]
        verts = [vec*m_p[4] for vec in verts] #scale update
        return verts, edges, [], [], []
    
    #FACEBOOL
    faces=[]
    
    #generating faces
    for lev in range(br_p[0]+1):
        for bran in branchlist[lev]:
            if e_p[0]!=0:bran.interpolate(e_p[0])
            faces.append(face_gen(bran.mp[0], bran.n))
            
    #combining faces
    while True:
        if len(faces) == 1:
            faces = faces[0]
            break
        faces[0].extend([[i+max(faces[0][-1])+1 for i in tup] for tup in faces.pop(1)])

    #generating verts from spine and making selection
    verts = []
    selection=[0]
    info=[]
    for lev in range(len(branchlist)):
        if lev == len(branchlist)-1:
            selection[0] = len(verts)
        for bran in branchlist[lev]:
            info.append([0,bran.mp[0]*bran.n-1, bran.mp[0]])
            verts.extend(bark_gen(bran.spine, bran.mp, t_p))
    
    selection = list(range(selection[0], len(verts)))
    
    for i in range(1,len(info)):
        info[i][0]=info[i-1][1]+1
        info[i][1]+=info[i][0]

    #flattening the base, 
    for lev in range(m_p[0]):
        verts[lev][2] = 0

    #scaling the tree
    verts = [vec*m_p[4] for vec in verts]
    
    return verts, [], faces, selection, info

def branchinit(verts, m_p, bd_p, br_p, r_p):
    m_p[3]*=m_p[2]
    st_pack = (verts[0],(verts[1]-verts[0]).normalized()*m_p[1], m_p[2])
    bran = branch(st_pack, m_p, bd_p, br_p, r_p, True)
    bran.n = len(verts)
    bran.spine = verts
    bran.regenerate()
    return [[bran]]

def toverts_dynamic(branchlist, facebool, m_p, br_p, t_p, e_p, d_p):
    if not facebool:
        verts = []
        edges = []
        for bran in branchlist:
            if e_p[0]:bran.interpolate(e_p[0])
            verts.extend(bran.spine)
            if edges: edges += [[n+edges[-1][1]+1,n+2+edges[-1][1]] for n in range(len(bran.spine))][:-1]
            else: edges += [(n,n+1) for n in range(len(bran.spine))][:-1]
        verts = [vec*m_p[4] for vec in verts] #scale update
        return verts, edges, [], [], []
    
    #FACEBOOL
    faces=[]
    
    #generating faces
    for bran in branchlist:
        if e_p[0]:bran.interpolate(e_p[0])
        faces.append(face_gen(bran.mp[0], bran.n))
            
    #combining faces
    while True:
        if len(faces) == 1:
            faces = faces[0]
            break
        faces[0].extend([[i+max(faces[0][-1])+1 for i in tup] for tup in faces.pop(1)])

    # generating verts from spine and making info, selection
    # info should be [startingvert, lastvert, sides]
    # selection should be verts that should have leaves
    trunk = branchlist[0]
    verts = [bark_gen(bran.spine, bran.mp, t_p, bran.H)]
    selection = list(range(round((trunk.n-1)*(1-d_p[1]))*trunk.mp[0],(trunk.n-1)*trunk.mp[0]))
    info = [0,bran.mp[0]*bran.n-1, bran.mp[0]]
    for bran in branchlist[1:]:
        verts.append(bark_gen(bran.spine, bran.mp, t_p, bran.H))
        info.append([info[-1][0]+1,bran.mp[0]*bran.n-1+info[-1][0], bran.mp[0]])
        start = round((bran.n-1)*(1-d_p[1]))*bran.mp[0]+verts[-1]+1
        end = (bran.n-1)*bran.mp[0]+verts[-1]
        selection.extend(list(range(start,end)))

    #flattening the base
    quat = (trunk.spine[1]-trunk.spine[0]).rotation_difference(Vector((0,0,1)))
    for i in range(trunk.mp[0]):verts[i]=quat@verts[i]

    #scaling the tree
    verts = [vec*m_p[4] for vec in verts]
    
    return verts, [], faces, selection, info    
