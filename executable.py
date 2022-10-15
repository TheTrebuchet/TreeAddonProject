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
Msides = 10
Mlength = 100
Mradius = 4
Mscale = 0.1
Mratio = 2

# RANDOM PARAMETERS
Rperlin = True
Rperlin_amount = 0.01
Rperlin_scale = 0.05
Rperlin_seed = 3

Rbends_amount = 0.5
Rbends_angle = 90
Rbends_correction = 0.2
Rbends_scale = 0.1
Rbends_seed = 8

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
flare_amount = 0.8

# temporary parameters
scale_lf1 = lambda x, a : 1/((x+1)**a)-(x/2)**a #this one is for trunk flare
branch_shift = 0
scale_lf2 = lambda x, a : ((1-(2*x-1)**2)/(a*(2*x-1)+1))**0.5  #this one is for branches scale

for x in range(100):
    print(scale_lf2(x/100, branch_shift))
#parameter lists
l=Mlength/(Mlength//(Mratio*math.tan(2*math.pi/(2*Msides))*Mradius))
m_p = [Msides, Mlength, Mradius, Mscale, l]
b_p = [branch_levels, branch_angle, branch_height, branch_variety, branch_seed]
bn_p = [branch_number1, branch_number2, branch_number3]
t_p = [scale_lf1, flare_amount, scale_lf2, branch_shift]
r_p = [Rperlin_amount, Rperlin_scale, Rperlin_seed, Rbends_amount, Rbends_angle, bl_math.clamp(Rbends_correction)*3.3, Rbends_scale, Rbends_seed]
'''
ok so let me get this straight
faceslist just gets added to in the branch function and later gets corrected to become faces
newvertslist is the output of branch function, it updates the verts list and is used in the next branch function
vertslist is what later becomes the verts
newspinelist is just what branch function needs for a new set of branches
'''
#generates the trunk and lists of lists of stuff

verts, faces = tree_gen(m_p, b_p, bn_p, t_p, r_p)

print('-------------------------')
mesh = bpy.data.meshes.new("tree")
object = bpy.data.objects.new("tree", mesh)

bpy.context.collection.objects.link(object)

mesh.from_pydata(verts ,[], faces)