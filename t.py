import sys
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file system view - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.model = QFileSystemModel()
        self.model.setRootPath('')
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)

        self.tree.setWindowTitle("Dir View")
        self.tree.resize(640, 480)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        self.setLayout(windowLayout)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

#
# import os
#
#
# def increment_strip(fp, increment=5):
#     bp, ext = os.path.splitext(fp)
#     with open(fp, "rb") as f:
#         d = f.read()
#
#     for i in range(increment):
#         with open(f"{bp}_{i}_strip{ext}", "wb") as fo:
#             fo.write(d[i:].rstrip(b"x\00"))
#         with open(f"{bp}_{i}{ext}", "wb") as fo:
#             fo.write(d[i:])
#
#
# # increment_strip("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/anim test/rot_x_0_22_42_def_c_new_end.maniskeys", increment=5)
#
#
# def add_level(out_bones, bone, level=0):
#     print(f"Level {level} {bone.name}")
#     tmp_bones = [child for child in bone.children]
#     tmp_bones.sort(key=lambda b: b.name)
#     print(tmp_bones)
#     out_bones += tmp_bones
#     for child in tmp_bones:
#         add_level(out_bones, child, level=level + 1)
#
#
# def get_level(bones, level=0):
#     level_children = []
#     for bone in bones:
#         print(f"Level {level} {bone.name}")
#         level_children.extend(bone.children)
#     level_children.sort(key=lambda b: bone_name_for_ovl(b.name))
#     return level_children
#
#
# def ovl_bones(b_armature_data):
#     # first just get the roots, then extend it
#     roots = [bone for bone in b_armature_data.bones if not bone.parent]
#     # this_level = []
#     out_bones = []
#     # next_level = []
#     # for bone in roots:
#     level_children = list(roots)
#     i = 0
#     while level_children:
#         print(level_children)
#         out_bones.extend(level_children)
#         level_children = get_level(level_children, level=i)
#         i += 1
#     # level_children = get_level(out_bones, level_children, level=0)
#     return [b.name for b in out_bones]
#
#
# def unpack_longint_vec(input, base):
#     """Unpacks and returns the self.raw_pos uint64"""
#     # numpy uint64 does not like the bit operations so we cast to default int
#     input = int(input)
#     # correct for size according to base, relative to 512
#     scale = base / 512 / 2048
#     # input = self.raw_pos
#     output = []
#     # print("inp",bin(input))
#     for i in range(3):
#         # print("\nnew coord")
#         # grab the last 20 bits with bitand
#         # bit representation: 0b11111111111111111111
#         twenty_bits = input & 0xFFFFF
#         # print("input", bin(input))
#         # print("twenty_bits = input & 0xFFFFF ", bin(twenty_bits), twenty_bits)
#         input >>= 20
#         # print("input >>= 20", bin(input))
#         # print("1",bin(1))
#         # get the rightmost bit
#         rightmost_bit = input & 1
#         # print("rightmost_bit = input & 1",bin(rightmost_bit))
#         # print(rightmost_bit, twenty_bits)
#         if not rightmost_bit:
#             # rightmost bit was 0
#             # print("rightmost_bit == 0")
#             # bit representation: 0b100000000000000000000
#             twenty_bits -= 0x100000
#         # print("final int", twenty_bits)
#         o = (twenty_bits + base) * scale
#         output.append(o)
#         # shift to skip the sign bit
#         input >>= 1
#     # input at this point is either 0 or 1
#     return output, input
#
# a = bytes.fromhex("CE 09 90 56 8E FB 9B B9 03 02 0B 40")
# a = bytes.fromhex("CE 09 90 56 03 02 0B 40")
# import struct
# b = struct.unpack("Q", a)[0]
# print(unpack_longint_vec(b, 512))


bl_info = {
    "name": "Flipped UVs Selector",
    "description": "Simple operator and menu item in UV editor for selecting faces with flipped UVs for active uv layer.",
    "author": "Simon Lusenc (50keda)",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "3D View > Quick Search; UV/Image Editor > Select > Flipped UVs",
    "category": "UV",
    "support": "COMMUNITY"
}

import bpy, bmesh, array
from mathutils import Vector

UP_VEC = Vector((0, 0, 1))


def is_flipped(uv_layer, poly):
    # from https://blenderartists.org/t/addon-flipped-uvs-selector/668111/5
    # order of polygon loop defines direction of face normal
    # and that same loop order is used in uv data.
    # With this knowladge we can easily say that cross product:
    # (v2.uv-v1.uv)x(v3.uv-v2.uv) gives us uv normal direction of part of the polygon. Further
    # this normal has to be used in dot product with up vector (0,0,1) and result smaller than zero
    # means uv normal is pointed in opposite direction than it should be (partial polygon v1,v2,v3 is flipped).

    # calculate uv differences between current and next face vertex for whole polygon
    diffs = []
    for l_i in poly.loop_indices:
        next_l = l_i + 1 if l_i < poly.loop_start + poly.loop_total - 1 else poly.loop_start

        next_v_uv = uv_layer[next_l].uv
        v_uv = uv_layer[l_i].uv

        diffs.append((next_v_uv - v_uv).to_3d())

    # go trough all uv differences and calculate cross product between current and next.
    # cross product gives us normal of the triangle. That normal then is used in dot product
    # with up vector (0,0,1). If result is negative we have found flipped part of polygon.
    for i, diff in enumerate(diffs):
        if i == len(diffs) - 1:
            break

        # as soon as we find partial flipped polygon we select it and finish search
        if diffs[i].cross(diffs[i + 1]) @ UP_VEC <= 0:
            return True
    return False



class FlippedUVSelector(bpy.types.Operator):
    """Select polygons with flipped UV mapping."""

    # order of polygon loop defines direction of face normal
    # and that same loop order is used in uv data.
    # With this knowladge we can easily say that cross product:
    # (v2.uv-v1.uv)x(v3.uv-v2.uv) gives us uv normal direction of part of the polygon. Further
    # this normal has to be used in dot product with up vector (0,0,1) and result smaller than zero
    # means uv normal is pointed in opposite direction than it should be (partial polygon v1,v2,v3 is flipped).

    bl_idname = "uv.select_flipped"
    bl_label = "Flipped UVs"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object and context.object.mode == "EDIT" and context.object.type == "MESH"

    def execute(self, context):
        ob = bpy.context.object

        bpy.ops.mesh.select_all(action="DESELECT")
        bpy.ops.object.mode_set(mode="OBJECT")

        for p in ob.data.polygons:
            p.select = is_flipped(ob.data.uv_layers.active.data, p)

        bpy.ops.object.mode_set(mode="EDIT")

        return {'FINISHED'}


def draw_item(self, context):
    self.layout.separator()
    self.layout.operator(FlippedUVSelector.bl_idname)


def register():
    bpy.utils.register_class(FlippedUVSelector)
    bpy.types.IMAGE_MT_select.append(draw_item)


def unregister():
    bpy.utils.register_class(FlippedUVSelector)
    bpy.types.IMAGE_MT_select.remove(draw_item)


if __name__ == '__main__':
    register()