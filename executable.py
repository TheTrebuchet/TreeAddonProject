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
sides = 20
length = 100
radius = 4
scale = 0.1

# RANDOM PARAMETERS
perlin = True
perlin_amount = 0.01
perlin_scale = 0.05
perlin_seed = 3

bends_amount = 0.5
bends_angle = 90
bends_correction = 0.2
bends_scale = 0.1
bends_seed = 8

# BRANCH PARAMETERS
branch_number = 4
branch_angle = 90
branch_height = 0.5
branch_weight = 0.2
branch_variety = 0.1
branch_seed = 1

# temporary parameters
flare_amount = 0.1
scale_lf1 = lambda x, h, r, a: (-r*x**0.5/h**0.5+r)*(1-a)+(-r*x/h+r)*a #this one is for trunk flare
branch_width = 20
branch_flare = 1.4
scale_lf2 = lambda x, a, b :  (a**(-2*(2*x-1))-(2*x-1)**2*a**(-2*(2*x-1)))**0.5*b #this one is for branches scale

#parameter lists
m_p = [sides, length, radius, scale]
b_p = [branch_number, branch_angle, branch_height, branch_variety]
t_p = [scale_lf1, flare_amount, scale_lf2, branch_width, branch_flare]
r_p = [perlin_amount, perlin_scale, perlin_seed, bends_amount, bends_angle, bends_correction, bends_scale, bends_seed]

def tree_gen(m_p, b_p, t_p, r_p, guide):
    # GENERATING SPINE
    spine, l, n = spine_gen(m_p, r_p)

    # GENERATING VERTS
    verts = bark_gen(spine, l, n, m_p, t_p)

    # GENERATING FACES
    faces = bark_faces(sides, n)

    guides = branch_guides(spine, verts, m_p, n, b_p, t_p)
    return verts, faces, guides

verts, faces, guides = tree_gen(m_p, b_p, t_p, r_p, mathutils.Vector((0,0,1)))
'''
for i in guides:
    m_p[1] = i.length()
    newverts, newfaces = tree_gen(m_p, b_p, t_p, r_p, i)
'''



print('-------------------------')
mesh = bpy.data.meshes.new("tree")
object = bpy.data.objects.new("tree", mesh)

bpy.context.collection.objects.link(object)

mesh.from_pydata(verts ,[], faces)

