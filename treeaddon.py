import bpy

class TreeGen(bpy.types.Operator):
    """creates a tree in cursor location"""
    bl_idname = 'object.simple_operator'
    bl_label = 'Simple Object Operator'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        verts = [(1,0,0),(0,1,0),(0,0,1)]
        faces = [(0,1,2)]
        mesh = bpy.data.meshes.new("tree")
        object = bpy.data.objects.new("tree", mesh)

        bpy.context.collection.objects.link(object)

        mesh.from_pydata(verts ,[], faces)
        return {'FINISHED'}

    


class TreeGenerator(bpy.types.Panel):
    """Creates a Panel in the Object properties window for tree creation, use with caution"""
    bl_label = "Tree_Gen"
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = "Create"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label('aight lad')
        layout.separator()

        row = layout.row()
        row.operator(TreeGen)
    

def register():
    bpy.utils.register_class(TreeGenerator)
    bpy.utils.register_class(TreeGen)


def unregister():
    bpy.utils.unregister_class(TreeGenerator)
    bpy.utils.unregister_class(TreeGen)

if __name__ == '__main__':
    register()
