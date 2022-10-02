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
branch_number = 30
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
m_p = [sides, length, radius, scale]
b_p = [branch_number, branch_angle, branch_height, branch_variety]
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
verts, faces, spine = tree_gen(m_p, t_p, r_p, mathutils.Vector((0,0,1)))
newvertslist = [verts]
vertslist = [verts]
faceslist = [faces]
newspinelist = [spine]

#generates branches on that trunk stored in new_ lists temporarily
newvertslist, newspinelist = branch_gen(newvertslist, faceslist, newspinelist, m_p, b_p, t_p, r_p)
vertslist += newvertslist #newlists are added to old lists
b_p[0] = 10
m_p[1]=5
newvertslist, newspinelist = branch_gen(newvertslist, faceslist, newspinelist, m_p, b_p, t_p, r_p)
vertslist += newvertslist

#faces are created from the list of lists, I am adding corrections to make it into a whole new list
adds = 0
for i in range(1, len(vertslist)):
    adds += len(vertslist[i-1])
    faces += [tuple([i+adds for i in j]) for j in faceslist[i]]

#verts are created from the list of lists
verts = []
for i in vertslist:
    verts += i
verts = [vec*m_p[-1] for vec in verts] #scales the tree

print('-------------------------')
mesh = bpy.data.meshes.new("tree")
object = bpy.data.objects.new("tree", mesh)

bpy.context.collection.objects.link(object)

mesh.from_pydata(verts ,[], faces)