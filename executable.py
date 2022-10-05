from re import M
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
scale = 0.1
ratio = 2

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
branch_levels = 2
branch_number1 = 30
branch_number2 = 5
branch_number3 = 2
branch_angle = 70
branch_height = 0.3
branch_weight = 0.5
branch_variety = 0.1
branch_seed = 1

# temporary parameters
flare_amount = 0.1
scale_lf1 = lambda x, h, r, a: (-r*x**0.5/h**0.5+r)*(1-a)+(-r*x/h+r)*a #this one is for trunk flare
branch_width = 30
branch_flare = 1.2
scale_lf2 = lambda x, a, b :  (a**(-2*(2*x-1))-(2*x-1)**2*a**(-2*(2*x-1)))**0.5*b #this one is for branches scale

#parameter lists
l=length/(length//(ratio*math.tan(2*math.pi/(2*sides))*radius))
m_p = [sides, length, radius, scale, l]
b_p = [branch_levels, branch_number1, branch_number2, branch_number3, branch_angle, branch_height, branch_variety, branch_seed]
t_p = [scale_lf1, flare_amount, scale_lf2, branch_width, branch_flare]
r_p = [perlin_amount, perlin_scale, perlin_seed, bends_amount, bends_angle, bends_correction, bends_scale, bends_seed]

'''
ok so let me get this straight
faceslist just gets added to in the branch function and later gets corrected to become faces
newvertslist is the output of branch function, it updates the verts list and is used in the next branch function
vertslist is what later becomes the verts
newspinelist is just what branch function needs for a new set of branches
'''
#generates the trunk and lists of lists of stuff

verts, faces = tree_gen(m_p, b_p, t_p, r_p)

print('-------------------------')
mesh = bpy.data.meshes.new("tree")
object = bpy.data.objects.new("tree", mesh)

bpy.context.collection.objects.link(object)

mesh.from_pydata(verts ,[], faces)