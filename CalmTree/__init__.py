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
    "name": "CalmTree",
    "author": "Jan Kulczycki",
    "version": (0, 0, 3),
    "blender": (3, 3, 0),
    "location": "View3D > Sidebar > CalmTree (Create Tab)",
    "description": "Procedurally generates a tree at cursor location",
    "doc_url": "https://calmtree.notion.site/Welcome-to-CalmTree-docs-3e43e110732a4bba8bd2f54655787226",
    "category": "Add Object",
}

import bpy

from .calmtree import *
from .property_group import *
from .panel import *

classes = (
CALMTREE_OT_new,
CALMTREE_OT_update,
CALMTREE_OT_sync,
CALMTREE_OT_default,
CALMTREE_PG_props,
CALMTREE_PT_createmain,
CALMTREE_PT_createsubpanel,
CALMTREE_PT_createedit,
CALMTREE_OT_leaf,
CALMTREE_OT_draw,
CALMTREE_OT_regrow)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.calmtree_props = bpy.props.PointerProperty(type=property_group.CALMTREE_PG_props)

def unregister():
    del bpy.types.WindowManager.calmtree_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()