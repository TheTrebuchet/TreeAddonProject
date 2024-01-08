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

    def prerequisits(self, total, h, l, p_length, progress, hstart, this_r, tipradius, scale_f2):
        self.length = scale_f2(hstart)*(p_length-total-h*l)
        self.radius = max(min((self.length+total+progress)/p_length*this_r, this_r), tipradius)
        self.ratio = self.radius/this_r
        self.prog = progress+total+h*l
        
    def generate(self):
        #at this point surface isn't relevant anymore
        return [self.origin,self.quat@self.direct*self.length, self.radius, self.prog]


class branch():
    def __init__(self, pack, pars, trunk):
        self.origin = pack[0]
        self.direction = pack[1]
        self.length = pack[1].length
        self.radius = pack[2]
        self.progress = pack[3]
        self.sides = max(4,round(pars.m_p[0]*pack[2]/pars.m_p[2])) #adjusting sides
        self.l = min(pars.m_p[5], self.length/2)
        self.trunk = trunk
        #determined while generation happens
        self.guidepacks=[]
        self.n = 0 
        self.spine=[]
        cutoff = self.progress/(self.length+self.progress)
        #total is the total absolute value length
        self.f12 = lambda total: max(pars.scale_f1(total/self.length*(1-cutoff)+cutoff)/pars.scale_f1(cutoff)*self.radius, pars.m_p[3])
        self.scalelist = []
        #so each branch has its local mp upon initiation, that has modified sides, length, radius and l, just for clarity really
        self.mp = [self.sides, self.length, self.radius, pars.m_p[3], pars.m_p[4], self.l]

    def generate_classic(self, pars):
        """
        This will generate the whole tree spine from its guide.
        It basically creates a new point, bends it, jiggles it and weighs it down based on predictions.
        Additionally the scalelist is created, so that each vert has a specified, relative radius.
        """
        self.n = round(self.length/self.l)+1 #number of verts on a spine is introduced
        
        self.spine = [Vector((0,0,0)), self.direction.normalized()*self.l] #spine two starting points
        self.scalelist.extend([self.f12(0), self.f12(self.l)]) #
        
        total=0
        while len(self.spine)<self.n:
            total+=self.l
            self.spine.append(self.l*((self.spine[-1] - self.spine[-2]).normalized())+self.spine[-1])
            self.spine = spine_bend(self.spine, self.n, pars.bd_p, self.l, self.direction)
            self.scalelist.append(self.f12(total))

        self.spine = spine_jiggle(self.spine, self.l, self.length, pars.r_p)
        self.spine = spine_weight(self.spine, self.n, self.l, self.radius, self.trunk, pars.bd_p)

        self.spine = [vec+self.origin for vec in self.spine]
    
    def generate_dynamic(self, pars):
        #defining all parameters
        lim = pars.lim
        qual = pars.e_p[2]
        Ythr = pars.d_p[0]
        Tthr = pars.d_p[1]

        parent_length = self.length
        parent_progress = self.progress

        pars_startlength = pars.m_p[1]*pars.br_p[3]
        parent_radius = self.radius
        tipradius = pars.m_p[3]
        l = self.l
        minang, maxang = pars.br_p[1:3]
        f1 = pars.scale_f1
        scale_f2 = pars.scale_f2
        
        random.seed(pars.br_p[-1])
        
        self.spine = [self.origin, self.direction.normalized()*l+self.origin]
        total = l
        self.scalelist = [self.f12(0), self.f12(l)]
        
        #build until startlength is reached
        while total<pars_startlength-l-self.progress:
            total+=l
            self.spine.append(l*((self.spine[-1] - self.spine[-2]).normalized())+self.spine[-1])
            self.spine = spine_bend(self.spine, self.n, pars.bd_p, l, self.direction)
            self.scalelist.append(self.f12(total))
        
        
        #adding an origin (0,0,0) so that the first split isn't always on the start
        guidelist = [guide(self.origin, self.origin)]

        #the build-guess-split begins
        while total<parent_length-Tthr:
            
            parent_quat = None
            this_r = self.f12(total)
            self.scalelist.append(this_r)
            for i in range(qual): #number of tries
                origin, surface, axis, h = guidetry(self.spine, 3*this_r) #generating the guess
                hstart = (total+h*l)/(parent_length)
                hglob = (total+h*l+self.progress)/(parent_length+self.progress)
                
                if (surface-guidelist[-1].surface).length>lim(hglob): #check for valid branches
                    
                    guess = guide(origin, surface) #the successful guess
                    guess.prerequisits(total, h, l, parent_length, parent_progress, hstart, this_r, tipradius, scale_f2)
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
            self.scalelist.append(self.f12(total))
        
        #weight, jiggle and finish everything
        #self.spine = spine_jiggle(self.spine, self.mp[5], self.mp[1], self.rp)
        self.n = len(self.spine)
        self.guidepacks = [g.generate() for g in guidelist[1:]]
    
    def regenerate(self):
        for i in range(2, self.n-1):
            quat = spine_bend(self.spine[i-2:i+1], self.n, self.bdp, self.mp[5], self.direction, quatmode=True)
            self.spine[i:] = [quat@(self.spine[k]-self.spine[i-1])+self.spine[i-1] for k in range(i,len(self.spine))]
        self.spine = spine_jiggle(self.spine, self.mp[5], self.mp[1], self.rp)
        self.spine = spine_weight(self.spine, self.n, self.mp[5], self.mp[2], self.trunk,self.bdp)
    
    def guidesgen(self, pars, lev):
        density = pars.bn_p[lev]
        typ = pars.e_p[1]

        if typ == 'fancy':
            self.guidepacks = guides_fancy(self.spine, self.mp, pars, lev, self.progress, self.scalelist)
        elif typ == 'fast': #this method should just be deprecated honestly
            num = lambda d, l: ceil((2.2*l+11)*d**(1.37*l**0.1)) #empiric equation
            self.guidepacks = guides_fast(self.spine, num(density, self.mp[1]), self.mp, pars.brp)
    
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

def outgrow_classic(branchlist, pars):
    for lev in range(pars.br_p[0]):
        branchlist.append([])
        for parentbranch in branchlist[-2]:
            parentbranch.guidesgen(pars, lev)
            children = parentbranch.guidepacks
            for pack in children:
                pars.r_p[2] +=1
                pars.bd_p[-1] +=1
                pars.br_p[-1] +=1 
                bran = branch(pack, pars, False)
                bran.generate_classic(pars)
                branchlist[-1].append(bran)
        pars.br_p[3]**=2 #temporary workaround, startlength factor is squared so it lowers for each level
    pars.br_p[3]**=((0.5)**pars.br_p[0]) #reverting the startlength
    return branchlist

def outgrow_dynamic(ready, pars):
    tobuild = ready[0].guidepacks.copy()
    d_p = pars.d_p
    while tobuild:
        pack = tobuild.pop(0)
        bran = branch(pack, pars, False)
        pars.br_p[-1]+=1
        if bran.mp[1]>d_p[1]: #if length of the branch is longer then threshold, generate with branches
            bran.generate_dynamic(pars)
            tobuild.extend(bran.guidepacks)
        else: #else generate like always
            bran.generate_classic(pars)
        
        ready.append(bran)

    return ready

def toverts(branchlist, pars):
    if type(branchlist[0])==list: branchlist = [a for b in branchlist for a in b]
    m_p = pars.m_p
    e_p = pars.e_p
    verts = []
    edges = []
    if not pars.facebool:
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

    verts, selection, info = bark_gen(branchlist, pars)
        
    #flattening the base
    trunk = branchlist[0]
    quat = (trunk.spine[1]-trunk.spine[0]).rotation_difference(Vector((0,0,1)))
    for i in range(trunk.mp[0]):verts[i]=quat@verts[i]

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