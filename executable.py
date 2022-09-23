import bpy
import math
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )

import functions
import random
# this next part forces a reload in case you edit the source after you first start the blender session
import imp
imp.reload(functions)

# this is optional and allows you to call the functions without specifying the package name
from functions import *

# MAIN PARAMETERS
sides = 4
length = 100
radius = 4
scale = 0.05

#RANDOM PARAMETERS
perlin = True
perlin_amount = 0.1
perlin_scale = 0.05
perlin_seed = 3

bends = True
bends_amount = 0.01
bends_scale = 0.05
bends_seed = 2

#BRANCHES
n_branch = 3
a_branch = 45
h_branch = 0.2
var_branch = 0.5



# SIDE PARAMETERS
angle = 4.7
d = 5

#-----------------------------------
m_p = [sides, length, radius, scale]
b_p = [n_branch, a_branch, h_branch, var_branch]
s_p = [angle, d]
r_p = [perlin_amount, perlin_scale, perlin_seed, bends_amount, bends_scale, bends_seed]

# GENERATING SPINE
spine, l, n = spine_gen(m_p, r_p)

# GENERATING VERTS
verts = bark_gen(spine, l, n, m_p, s_p)

# GENERATING FACES
faces = bark_faces(sides, n)

verts += branch_guides(spine, verts, m_p, n, b_p)

mesh = bpy.data.meshes.new("tree")
object = bpy.data.objects.new("tree", mesh)

bpy.context.collection.objects.link(object)

mesh.from_pydata(verts ,[], faces)

