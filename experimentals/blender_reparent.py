import bpy
import mathutils


def append_armature_modifier(b_obj, b_armature):
    """Append an armature modifier for the object."""
    if b_obj and b_armature:
        b_obj.parent = b_armature
        armature_name = b_armature.name
        b_mod = b_obj.modifiers.new(armature_name, 'ARMATURE')
        b_mod.object = b_armature
        b_mod.use_bone_envelopes = False
        b_mod.use_vertex_groups = True


def join(obs):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in obs:
        obj.select_set(True)
    # got to set active object first for viewlayer
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.join()


obs = bpy.context.selected_objects

mesh_obs = [ob for ob in obs if ob.type == "MESH" and ob.parent and ob.parent_type == "BONE"]
for ob in mesh_obs:
    # get name of parent bone
    bone_name = ob.parent_bone
    # print(f"bone_name {bone_name}")

    # assign all vers to this bone
    ob.vertex_groups.new(name=bone_name)
    ob.vertex_groups[bone_name].add(list(range(len(ob.data.vertices))), 1.0, 'REPLACE')
    # change parenting to object (armature is same as with armature modifier)
    # ob.parent_type = "ARMATURE"
    ob.parent_type = "OBJECT"
    append_armature_modifier(ob, ob.parent)

    ob.data.transform(ob.matrix_world)
    ob.matrix_world = mathutils.Matrix().to_4x4()
    ob.parent_bone = ""
join(mesh_obs)
