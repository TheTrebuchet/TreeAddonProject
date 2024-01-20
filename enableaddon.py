import bpy
import os
bpy.ops.preferences.addon_install(filepath=os.getcwd()+'/CalmTree.zip')
bpy.ops.preferences.addon_enable(module='CalmTree')
bpy.ops.wm.save_userpref()