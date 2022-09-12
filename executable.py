import bpy
import math
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )

import functions

# this next part forces a reload in case you edit the source after you first start the blender session
import imp
imp.reload(functions)

# this is optional and allows you to call the functions without specifying the package name
from functions import *
# MAIN PARAMETERS
n = 5
res = 1
scale = 0.5
# ADDITIONAL PARAMETERS
s=6*res
r=res
l=r*2
tree = []
for x in spine(n, l):
    for y in circle(s,r):
        tree.append((mathutils.Vector(x) + mathutils.Vector(y))*scale)
faces = bark(tree, s, n)

mesh = bpy.data.meshes.new("tree")
object = bpy.data.objects.new("tree", mesh)

bpy.context.collection.objects.link(object)

mesh.from_pydata(tree,[], faces)
