import os
import bpy

from plugin.modules_import.material import create_material


def object_has_material(obj, material):
    for slot in obj.material_slots:
        if slot.material.name == material:
            return True
    return False


def load(reporter, filepath=""):
    in_dir, material_ext = os.path.split(filepath)
    material, ext = os.path.splitext(material_ext)

    # if material exists, save a ref
    print(f'loading {material}')
    o_mat = bpy.data.materials.get(material)

    # create the new one
    b_mat = create_material(in_dir, material)

    if o_mat:
        # the material already existed, we have just updated, make
        # sure we update all objects using it
        for obj in bpy.data.objects:
            for slot in obj.material_slots:
                if slot.material == o_mat:
                    slot.material = b_mat

        # remove the old material
        bpy.data.materials.remove(o_mat)
        # rename the new material (probably has a .00x sub added)
        b_mat.name = material

    # I think this should only be appended if the material didn't really exist before
    # for this object?
    # todo: decide what to do with the selected object and the new material
    if not object_has_material(bpy.context.object, material):
        #b_me = bpy.context.object.data
        #b_me.materials.append(b_mat)
        pass

    reporter.show_info(f"Imported {material}")
