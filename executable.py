import bpy
import mathutils
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
sides = 12
length = 100
radius = 6
scale = 0.1
m_p = [sides, length, radius, scale]
# SIDE PARAMETERS
height = length
base = radius
angle = 4.7
d = 5
s_p = [height, base, angle, d]

# GENERATING VERTS
verts, n = treegen(m_p, s_p)

# GENERATING FACES
faces = bark(sides, n)

mesh = bpy.data.meshes.new("tree")
object = bpy.data.objects.new("tree", mesh)

bpy.context.collection.objects.link(object)

mesh.from_pydata(verts ,[], faces)
