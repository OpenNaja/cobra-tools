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
