import os
import bpy

from plugin.modules_import.material import create_material


def load(filepath):
    created_materials = []
    in_dir, material_ext = os.path.split(filepath)
    material, ext = os.path.splitext(material_ext)
    b_me = bpy.context.object.data
    # import_material(created_materials, in_dir, b_me, material)

    b_mat = create_material(in_dir, material)
    b_me.materials.append(b_mat)
