import os
import bpy

from plugin.modules_import.material import create_material


def load(reporter, filepath="", replace=True):
    in_dir, material_ext = os.path.split(filepath)
    name, ext = os.path.splitext(material_ext)

    # if material exists, save a ref and rename or return
    print(f'loading {name}')
    o_mat = bpy.data.materials.get(name)
    if o_mat:
        if not replace:
            return "{'CANCELLED'}"
        o_mat.name = 'marked_for_removal'
    else:
        o_mat = bpy.data.materials.get(name.lower())

    # create the new one
    b_mat = create_material(reporter, in_dir, name)

    if o_mat:
        # the material already existed, we have just updated, make
        # sure we update all objects using it
        for obj in bpy.data.objects:
            for slot in obj.material_slots:
                if slot.material == o_mat:
                    slot.material = b_mat

        # remove the old material
        bpy.data.materials.remove(o_mat)

    reporter.show_info(f"Imported {name}")
