import bpy
bpy.ops.preferences.addon_disable(module="CalmTree")
bpy.ops.preferences.addon_remove(module='CalmTree')
bpy.ops.wm.save_userpref()