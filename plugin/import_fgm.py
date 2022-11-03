import os
import bpy

from plugin.modules_import.material import create_material


def load(filepath):
    messages = set()
    in_dir, material_ext = os.path.split(filepath)
    material, ext = os.path.splitext(material_ext)
    b_mat = create_material(in_dir, material)
    b_me = bpy.context.object.data
    b_me.materials.append(b_mat)

    messages.add(f"Finished fgm import")
    return messages
