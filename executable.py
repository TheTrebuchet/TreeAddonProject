import bpy
import sys
import os
#this part is for reloading the file
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
import functions
import imp
imp.reload(functions)
from functions import *

# MAIN PARAMETERS
sides = 10
length = 100
radius = 4
scale = 0.05

# RANDOM PARAMETERS
perlin = True
perlin_amount = 0.1
perlin_scale = 0.05
perlin_seed = 3

bends = True
bends_amount = 0.01
bends_scale = 0.05
bends_seed = 2

# BRANCH PARAMETERS
n_branch = 100
a_branch = 45
h_branch = 0.2
var_branch = 0.1
seed_branch = 1

# temporary parameters
flare_amount = 0.1
scale_lf1 = lambda x, h, r, a: (-r*x**0.5/h**0.5+r)*(1-a)+(-r*x/h+r)*a #this one is for trunk flare
branch_width = 10
branch_flare = 1.4
scale_lf2 = lambda x, a, b :  (a**(-2*(2*x-1))-(2*x-1)**2*a**(-2*(2*x-1)))**0.5*b #branches scale

#parameter lists
m_p = [sides, length, radius, scale]
b_p = [n_branch, a_branch, h_branch, var_branch]
t_p = [scale_lf1, flare_amount, scale_lf2, branch_width, branch_flare]
r_p = [perlin_amount, perlin_scale, perlin_seed, bends_amount, bends_scale, bends_seed]

# GENERATING SPINE
spine, l, n = spine_gen(m_p, r_p)

# GENERATING VERTS
verts = bark_gen(spine, l, n, m_p, t_p)

# GENERATING FACES
faces = bark_faces(sides, n)

verts += branch_guides(spine, verts, m_p, n, b_p, t_p)

mesh = bpy.data.meshes.new("tree")
object = bpy.data.objects.new("tree", mesh)

bpy.context.collection.objects.link(object)

mesh.from_pydata(verts ,[], faces)

