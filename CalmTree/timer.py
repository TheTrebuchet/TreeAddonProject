from algorithm import *
from calmtree import branch
from generative import outgrow_dynamic, toverts

class test_parameters:
    def __init__(self):
        self.m_p = [10, 7.0, 0.25, 0.004999999888241291, 1.0, 0.23333333333333334]
        self.br_p = [2, 0.3490658402442932, 1.2217304706573486, 0.25, 0.10000000149011612, 0.10000000149011612, 0.30000001192092896, 1]
        self.bn_p = [1.2000000476837158, 1.0, 1.0]
        self.bd_p = [0.20000000298023224, 0.20000000298023224, 0.30000001192092896, 1.5, 0.05714285799435207, 1]
        self.r_p = [0.10000000149011612, 1.0, 1]
        self.e_p = [0, 'fancy', 4, 0.10000000149011612]
        self.d_p = [0.699999988079071, 0.7000000104308128]
        self.facebool = True

        self.lim = lambda x: 1 / (x * self.bn_p[0] + (1 - x) * self.bn_p[1])
        
        # this one is for trunk flare
        fa=1.0
        self.scale_f1 = lambda x: 1-x+fa*(1-x)**10
        # this one is for branches scale
        bs = 0.5
        self.scale_f2 = lambda x: (4*x*(1-x)*((1-bs**2)**0.5+1)/(2*(bs*(2*x-1)+1)))**(0.5+0.5*abs(bs))

pars = test_parameters()
seeds = [pars.br_p[-1], pars.bd_p[-1], pars.r_p[-1]]
st_pack = [Vector((0, 0, 0)), Vector((0, 0, pars.m_p[1])), pars.m_p[2], 0]
stbran = branch(st_pack, pars, True)
stbran.generate_dynamic(pars)
branchlist = [stbran]
branchlist = outgrow_dynamic(branchlist, pars)
verts, edges, faces, selection, info = toverts(branchlist, pars)