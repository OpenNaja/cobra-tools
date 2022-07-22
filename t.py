# import sys
# from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout
# from PyQt5.QtGui import QIcon
#
#
# class App(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 file system view - pythonspot.com'
#         self.left = 10
#         self.top = 10
#         self.width = 640
#         self.height = 480
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#
#         self.model = QFileSystemModel()
#         self.model.setRootPath('')
#         self.tree = QTreeView()
#         self.tree.setModel(self.model)
#
#         self.tree.setAnimated(False)
#         self.tree.setIndentation(20)
#         self.tree.setSortingEnabled(True)
#
#         self.tree.setWindowTitle("Dir View")
#         self.tree.resize(640, 480)
#
#         windowLayout = QVBoxLayout()
#         windowLayout.addWidget(self.tree)
#         self.setLayout(windowLayout)
#
#         self.show()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())

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

import struct

import numpy as np
from numba import jit

from generated.formats.fgm import TextureInfo
from generated.formats.ms2.bitfield.ModelFlag import ModelFlag
from generated.formats.ovl_base import OvlContext


innormals = (
    [0, 164, 127, 254],  # [  9, 127,  78]
    [0, 190, 127, 254],  # [ 37, 127,  37]
    [0, 216, 127, 254],  # [ 78, 127,   9]
    [0, 253, 127, 254],  # [126, 127,   0]
    [254, 216, 127, 254],  # [175, 127,   9]
    [254, 190, 127, 254],  # [216, 127,  37]
    [254, 164, 127, 254],  # [244, 127,  78]
    [254, 127, 127, 254],  # [254, 127, 126]
    [216, 127, 127, 254],  # [244, 127, 175]
    [190, 127, 127, 254],  # [216, 127, 216]
    [164, 127, 127, 254],  # [175, 127, 244]
    [127, 127, 127, 254],  # [127, 127, 254]
    [89, 127, 127, 254],  # [ 78, 127, 244]
    [63, 127, 127, 254],  # [ 37, 127, 216]
    [37, 127, 127, 254],  # [  9, 127, 175]
    [0, 127, 127, 254],  # [  0, 127, 127]
    [0, 164, 127, 254],  # [  9, 127,  78]
    [0, 164, 127, 254],  # [  9, 127,  78]
    [0, 190, 127, 254],  # [ 37, 127,  37]
    [0, 216, 127, 254],  # [ 78, 127,   9]
    [0, 253, 127, 254],  # [126, 127,   0]
    [254, 216, 127, 254],  # [175, 127,   9]
    [254, 190, 127, 254],  # [216, 127,  37]
    [254, 164, 127, 254],  # [244, 127,  78]
    [254, 127, 127, 254],  # [254, 127, 126]
    [216, 127, 127, 254],  # [244, 127, 175]
    [190, 127, 127, 254],  # [216, 127, 216]
    [164, 127, 127, 254],  # [175, 127, 244]
    [127, 127, 127, 254],  # [127, 127, 254]
    [89, 127, 127, 254],  # [ 78, 127, 244]
    [63, 127, 127, 254],  # [ 37, 127, 216]
    [37, 127, 127, 254],  # [  9, 127, 175]
    [0, 127, 127, 254],  # [  0, 127, 127]
    [0, 164, 127, 254],  # [  9, 127,  78]
    [127, 254, 0, 122],  # [127, 254, 126]
    [127, 254, 0, 131],  # [127, 254, 127]
    [127, 254, 0, 123],  # [127, 254, 126]
    [127, 254, 0, 130],  # [127, 254, 127]
    [127, 254, 0, 127],  # [127, 254, 127]
    [127, 254, 0, 126],  # [127, 254, 127]
    [127, 254, 0, 127],  # [127, 254, 127]
    [127, 254, 1, 127],  # [127, 254, 127]
    [127, 254, 2, 127],  # [127, 254, 127]
    [127, 254, 0, 131],  # [127, 254, 127]
    [127, 254, 0, 128],  # [127, 254, 127]
    [127, 254, 0, 129],  # [127, 254, 127]
    [127, 254, 3, 127],  # [127, 254, 127]
    [127, 254, 3, 127],  # [127, 254, 127]
    [127, 254, 4, 127],  # [127, 254, 126]
    [127, 254, 4, 127],  # [127, 254, 127]
    [127, 254, 4, 127])  # [127, 254, 127]

in_ubtyes = [struct.pack("BB", u[0], u[1]) for u in innormals]
in_ushorts = [struct.unpack("H", u)[0] for u in in_ubtyes]
print(in_ushorts)
count = len(innormals)
inp = np.zeros(dtype=np.uint16, shape=(count))
out = np.zeros(dtype=np.float32, shape=(count, 3))
# inp[0] = 61059
# inp[1] = 36357
# inp[2] = 42563
# inp[3] = 36357
# inp[4] = 32702
for i in range(count):
    inp_ushort = in_ushorts[i]
    ush_str = str(bin(inp_ushort))[2:]
    print(f"{ush_str:>16}", innormals[i][:2])
    # print(flag)
# print(out)
# print(np.linalg.norm(out, axis=1))
# ([-0,40625, 0,125, 0,34375]
# ([-0,8125, 0,25, 0,6875], 1)
#
# flags = [512, 513, 517, 528, 529, 533, 545, 565, 821, 853, 885, 1013, ]
# for flag in flags:
#     f = ModelFlag.from_value(flag)
#     print(f)

context = OvlContext()
tex = TextureInfo(context, arg=0, template=None, set_default=True)
print(tex)
