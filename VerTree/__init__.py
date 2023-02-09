'''
Copyright (C) 2023 Jan Kulczycki
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
    "name": "VerTree",
    "author": "Jan Kulczycki",
    "version": (0, 1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > Tree Generator (Create Tab)",
    "description": "Procedurally generates a tree at cursor location",
    "doc_url": "https://vertree-docs.readthedocs.io/en/latest/",
    "category": "Add Object",
}

import bpy

from .vertree import *
from .property_group import *

classes = (
VERTREE_OT_new,
VERTREE_OT_update,
VERTREE_OT_sync,
VERTREE_OT_default,
VERTREE_PG_props,
VERTREE_PT_createmain,
VERTREE_PT_createsubpanel,
VERTREE_PT_createedit,
VERTREE_OT_leaf,
VERTREE_OT_draw,
VERTREE_OT_regrow)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.vertree_props = bpy.props.PointerProperty(type=property_group.VERTREE_PG_props)

def unregister():
    del bpy.types.WindowManager.vertree_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()