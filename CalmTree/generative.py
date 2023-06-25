from .algorithm import *

def guidetry(spine, R):
    pt1=spine[-1]
    pt2=spine[-2]
    h = random.random()
    origin = (1-h)*pt1+h*pt2
    phi = random.uniform(-math.pi,math.pi)
    direction = R*(Vector((0,0,1)).rotation_difference(pt1-pt2)@Vector((sin(phi), cos(phi),0)))
    surface = direction+origin
    axis = direction.cross(pt1-pt2)
    return origin, surface, axis, h

class guide():
    def __init__(self, origin, surface):
        self.origin = origin
        self.surface = surface
        self.direct = (self.surface-self.origin).normalized()
        self.quat = None

    def prerequisits(self, total, h, l, p_length, progress, hstart, p_radius, tipradius, scale_f2):
        self.length = scale_f2(hstart)*(p_length-total-h*l)
        self.radius = max(min(self.length/p_length*p_radius, 0.9*p_radius), tipradius)
        self.ratio = self.radius/p_radius
        self.prog = progress+total+h*l
        
    def generate(self):
        #at this point surface isn't relevant anymore
        return [self.origin,self.quat@self.direct*self.length, self.R, self.prog]


class branch():
    def __init__(self, pack, m_p, trunk):
        #so each branch has its local mp upon initiation
        self.origin = pack[0]
        self.direction = pack[1]
        self.length = pack[1].length
        self.radius = pack[2]
        self.progress=pack[3]
        
        self.sides = m_p[0]
        self.l = min(m_p[5], self.length/2)
        self.trunk = trunk
        self.guidepacks=[]
        self.n = 0
        self.spine=[]
        
        self.mp = [self.sides, self.length, self.radius, m_p[3], m_p[4], self.l]

    def generate(self, pars):
        self.n = round(self.length/self.l)+1
        self.spine = [Vector((0,0,0)), self.direction.normalized()*self.l]
        length = self.length
        l = self.l
        radius = self.radius
        direction = self.direction

        while len(self.spine)<self.n:
            self.spine.append(l*((self.spine[-1] - self.spine[-2]).normalized())+self.spine[-1])
            self.spine = spine_bend(self.spine, self.n, pars.bd_p, l, direction)

        self.spine = spine_jiggle(self.spine, l, length, pars.r_p)
        self.spine = spine_weight(self.spine, self.n, l, radius, self.trunk, pars.bd_p)

        self.spine = [vec+self.pack[0] for vec in self.spine]
        return self
    
    def generate_dynamic(self, pars):
        #defining all parameters
        lim = pars.lim
        qual = pars.e_p[2]
        Ythr = pars.d_p[0]
        Tthr = pars.d_p[1]

        pars_length = pars.mp[1]
        parent_length = self.length
        parent_progress = self.progression

        pars_startlength = pars.m_p[1]*pars.br_p[3]
        parent_radius = pars.m_p[2]
        tipradius = pars.mp[3]
        l = self.l
        minang, maxang = pars.br_p[1:3]
        scale_f1 = pars.scale_lf1
        scale_f2 = pars.scale_lf2
        
        print('new branch')
        random.seed(pars.br_p[7])
        
        self.spine = [self.origin, self.direction.normalized()*l+self.origin]
        
        #build until startlength is reached
        total = 0
        while total<pars_startlength-l:
            total+=l
            self.spine.append(l*((self.spine[-1] - self.spine[-2]).normalized())+self.spine[-1])
            self.spine = spine_bend(self.spine, self.n, pars.bd_p, l, self.pack[1])
        
        #adding an origin (0,0,0) so that the first split isn't always on the start
        guidelist = [guide(self.origin, self.origin)]

        #the build-guess-split begins
        while total<parent_length+parent_progress-Tthr:
            
            parent_quat = None
            
            for i in range(qual): #number of tries
                cutoff = parent_progress/pars_length
                this_r = scale_f1(total/parent_length*(1-cutoff)+cutoff)*parent_radius
                origin, surface, axis, h = guidetry(self.spine, this_r) #generating the guess
                hstart = (total+h*l+parent_progress)/(parent_length + parent_progress)
                
                if (surface-guidelist[-1].surface).length>lim(hstart): #check for valid branches
                    guess = guide(origin, surface) #the successful guess
                    guess.prerequisits(total, h, l, parent_length, hstart, this_r, tipradius, scale_f2)
                    ang = hstart*minang+(1-hstart)*maxang #angle between the new branches
                    
                    if guess.ratio>Ythr: #if split can happen
                        self.spine[-1] = origin
                        total-=(1-h)*l
                        parent_quat = Quaternion(axis,ang*guess.ratio/2)
                        guess.quat = Quaternion(axis,(math.pi/2-ang)+guess.ratio*ang/2)
                    
                    else:
                        guess.quat = Quaternion(axis,(math.pi/2-ang))
                    guidelist.append(guess)
                    break
            
            extension = l*(self.spine[-1]-self.spine[-2]).normalized()
            
            if parent_quat: #rotate new point
                extension = parent_quat@extension
            
            self.spine.append(extension+self.spine[-1])
            self.spine = spine_bend(self.spine, len(self.spine), pars.bd_p, l, self.direction, nfactor=True)
            total+=l
        
        #the rest to the tip
        while total<parent_length-l:
            total+=l
            self.spine.append(l*((self.spine[-1] - self.spine[-2]).normalized())+self.spine[-1])
            self.spine = spine_bend(self.spine, len(self.spine), pars.bd_p, l, self.direction, nfactor=True)
        
        #weight, jiggle and finish everything
        #self.spine = spine_jiggle(self.spine, self.mp[5], self.mp[1], self.rp)
        self.n = len(self.spine)
        self.guidepacks = [g.generate() for g in guidelist[1:]]
    
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
        for parentbranch in branchlist[-2]:
            parentbranch.guidesgen(bn_p[lev], t_p, e_p[1], e_p[2])
            children = parentbranch.guidepacks
            for pack in children:
                r_p[2] +=1
                bd_p[-1] +=1
                br_p[-1] +=1
                branchlist[-1].append(branch(pack, parentbranch.childmp, bd_p, br_p, r_p, False).generate())
        br_p[3]=br_p[3]**2 #temporary workaround
    br_p[3]=br_p[3]**((0.5)**br_p[0]) 
    return branchlist

def outgrow_dynamic(ready, pars):
    tobuild = ready[0].guidepacks.copy()
    m_p = pars.m_p
    d_p = pars.d_p
    random.seed(pars.bd_p[-1])
    while tobuild:
        pack = tobuild.pop(0)
        tmp = m_p.copy()
        tmp[0] = max(4,round(m_p[0]*pack[2]/m_p[2])) #adjusting sides
        bran = branch(pack, tmp, False)

        if bran.mp[1]>d_p[1]: #if length of the branch is longer then threshold, generate with branches
            bran.generate_dynamic(pars)
            tobuild.extend(bran.guidepacks)
        else: #else generate like always
            bran.generate(pars)
        
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

def toverts_dynamic(branchlist, pars):
    m_p = pars.m_p
    e_p = pars.e_p
    d_p = pars.d_p
    if not pars.facebool:
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
