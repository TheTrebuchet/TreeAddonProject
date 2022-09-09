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

n = 50
r=1
verts = circle(n,r)
faces = [tuple(x for x in range(n))]

mesh = bpy.data.meshes.new("tree")
object = bpy.data.objects.new("tree", mesh)

bpy.context.collection.objects.link(object)

mesh.from_pydata(verts,[], faces)
