'''
Copyright (C) 2022 Jan Kulczycki
jan.kulczycki1@gmail.com

Created by Jan Kulczycki

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "TreeGen",
    "author": "TheTrebuchet",
    "version": (0, 0, 1),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > Tree Generator (Create Tab)",
    "description": "Adds a generated tree at cursor",
    "warning": "still in development",
    "doc_url": "",
    "category": "Add Object",
}

import bpy

from . import treegen
from . import property_group

classes = [treegen.TreeGen, property_group.TreeGen_PG, treegen.Object_PT_TreeGenerator]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.treegen_props = bpy.props.PointerProperty(
        type=property_group.TreeGen_PG)

def unregister():
    del bpy.types.WindowManager.treegen_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()