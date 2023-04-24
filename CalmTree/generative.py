from .algorithm import *

class guide():
    def __init__(self,origin,h,direct,r):
        self.origin = origin
        self.h = h
        self.direct = direct
        self.r = r

class branch():
    def __init__(self, pack, m_p, bd_p, br_p, r_p, trunk):
        self.pack = pack
        self.mp = [m_p[0], self.pack[1].length, self.pack[2], m_p[3], m_p[4], bl_math.clamp(m_p[5], 0, self.pack[1].length/2)]
        self.bdp = bd_p
        self.brp = br_p
        self.rp = r_p
        self.trunk = trunk
        self.guidepacks=[]
        self.n = 0
        self.spine=[]
        
    def generate(self):
        self.n = round(self.mp[1]/self.mp[5])+1
        self.spine = [Vector((0,0,0))]
        self.spine.append((self.pack[1].normalized())*self.mp[5])

        while len(self.spine)<self.n:
            self.spine.append(self.mp[5]*((self.spine[-1] - self.spine[-2]).normalized())+self.spine[-1])
            self.spine = spine_bend(self.spine, self.n, self.bdp, self.mp[5], self.pack[1], 'spine')
        self.spine = spine_jiggle(self.spine, self.mp[5], self.mp[1], self.rp)
        self.spine = spine_weight(self.spine, self.n, self.mp[5], self.mp[2], self.trunk, self.bdp)

        self.spine = [vec+self.pack[0] for vec in self.spine]
        return self
    
    def generate_complete(self, density, t_p, qual):
        length, radius, tipradius= self.mp[1:4]
        l = self.mp[5]
        minang, maxang, start_h, hor, var, scaling, sd = self.brp[1:]
        scale_f1, flare, scale_f2, shift = t_p
        dist = 1/3*length*scaling

        allbrans=[]
        total = 0
        self.spine = [Vector((0,0,0))]
        self.spine.append((self.pack[1].normalized())*l)
        
        while total<length:
            for i in range(qual):
                pt1=self.spine[-1]
                pt2=self.spine[-2]
                h = random.random()
                r = scale_f1(total+h*l, flare)
                origin = h*pt1+(1-h)*pt2
                phi = random.uniform(-math.pi,math.pi)
                npt = Vector((0,0,1)).rotation_difference(pt1-pt2)@Vector((r*sin(phi), r*cos(phi),0))
                npt+=origin
                if npt-allbrans[-1].surface>1/density: allbrans.append(guide(origin,h,npt,r))
                
                #
                    #random h based on density
                    #get l and r from funcs
                    #get angle from funcs and IF REQUIREMENT radii ratio
                    #return h, r, l, ang (from stem)
                    #check with local group, maintain it based on density
                    #add for the first ok
        #if the branch got generated and requirement is met
            #shorten the new fragment
            #get rotation vector and generate branch and new segment
        self.spine.append(self.mp[5]*((self.spine[-1] - self.spine[-2]).normalized())+self.spine[-1])
        self.spine = spine_bend(self.spine, self.n, self.bdp, self.mp[5], self.pack[1], 'spine')
        #weight everything
        #jiggle everything
        self.n = len(spine)
        #return 



        return self
    
    def regenerate(self):
        for i in range(2, self.n-1):
            quat = spine_bend(self.spine[i-2:i+1], self.n, self.bdp, self.mp[5], self.pack[1], 'quat')
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

def toverts(branchlist, facebool, m_p, br_p, t_p, e_p):
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