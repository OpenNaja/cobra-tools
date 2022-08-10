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
# import logging
# import sys
# import time
#
# from PyQt5 import Qt
# from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QApplication
#
# from generated.formats.ovl import OvlFile
# s = time.time()
# ovl_path = "C:/Program Files (x86)/Steam/steamapps/common/Jurassic World Evolution 2/Win64/ovldata/Content0/Main.ovl"
# ovl_data = OvlFile()
# file_names_list = ovl_data.load(ovl_path, commands={"get_file_names": True})
# print(time.time()-s)
# # print(new_hashes)
# from PyQt5.QtCore import QObject, QThread, pyqtSignal
# # Snip...
# from ovl_util.config import logging_setup, get_version_str, get_commit_str
#
# logging_setup("ovl_tool_gui")
#
# # ovl_path = "C:/Program Files (x86)/Steam/steamapps/common/Jurassic World Evolution 2/Win64/ovldata/Content2/Main.ovl"
# ovl_path = "C:/Program Files (x86)/Steam/steamapps/common/Jurassic World Evolution 2/Win64/ovldata/Content2/Init.ovl"
#
# # Step 1: Create a worker class
# class Worker(QObject):
#     finished = pyqtSignal()
#     progress = pyqtSignal(int)
#
#     def __init__(self, function, *args, **kwargs):
#         super().__init__()
#
#         self.function_name = function
#         self.args = args
#         self.kwargs = kwargs
#         # self.start.connect(self.run)
#
#     def run(self):
#         """Long-running task."""
#         # logging.info(self.kwargs["filepath"])
#         # self.thread().ovl.load(self.kwargs["filepath"])
#
#         func = getattr(self.thread().ovl, self.function_name)
#         func(*self.args, **self.kwargs)
#         self.finished.emit()
#
#
# class Window(QMainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.clicksCount = 0
#         self.setupUi()
#         self.ovl = OvlFile()
#
#     def setupUi(self):
#         self.setWindowTitle("Freezing GUI")
#         self.resize(300, 150)
#         self.centralWidget = QWidget()
#         self.setCentralWidget(self.centralWidget)
#         # Create and connect widgets
#         self.clicksLabel = QLabel("Counting: 0 clicks", self)
#         # self.clicksLabel.setAlignment(AlignHCenter | Qt.AlignVCenter)
#         self.stepLabel = QLabel("Long-Running Step: 0")
#         # self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#         self.countBtn = QPushButton("Click me!", self)
#         self.countBtn.clicked.connect(self.countClicks)
#         self.longRunningBtn = QPushButton("Long-Running Task!", self)
#         self.longRunningBtn.clicked.connect(self.runLongTask)
#         self.quitBtn = QPushButton("Cancel", self)
#         self.quitBtn.clicked.connect(self.quitTask)
#         # Set the layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.clicksLabel)
#         layout.addWidget(self.countBtn)
#         layout.addStretch()
#         layout.addWidget(self.stepLabel)
#         layout.addWidget(self.longRunningBtn)
#         layout.addWidget(self.quitBtn)
#         self.centralWidget.setLayout(layout)
#
#     def countClicks(self):
#         self.clicksCount += 1
#         self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")
#
#     def reportProgress(self, n):
#         self.stepLabel.setText(f"Long-Running Step: {n}")
#     # Snip...
#     def runLongTask(self):
#         self.run_threaded("load", ovl_path)
#
#     def run_threaded(self, function_name, *args, **kwargs):
#         # Step 2: Create a QThread object
#         self.thread = QThread()
#         self.thread.ovl = self.ovl
#         # Step 3: Create a worker object
#         self.worker = Worker(function_name, *args, **kwargs)
#         # Step 4: Move worker to the thread
#         self.worker.moveToThread(self.thread)
#         # Step 5: Connect signals and slots
#         self.thread.started.connect(self.worker.run)
#         self.worker.finished.connect(self.thread.quit)
#         self.worker.finished.connect(self.worker.deleteLater)
#         self.thread.finished.connect(self.thread.deleteLater)
#         self.worker.progress.connect(self.reportProgress)
#         # Step 6: Start the thread
#         self.thread.start()
#
#         # Final resets
#         self.longRunningBtn.setEnabled(False)
#         self.thread.finished.connect(
#             lambda: self.longRunningBtn.setEnabled(True)
#         )
#         self.thread.finished.connect(
#             lambda: self.stepLabel.setText("Long-Running Step: 0")
#         )
#
#     def quitTask(self):
#         logging.info(f"Quit")
#         self.thread.quit()
#
#     def do_sth(self):
#         logging.info(f"Done")
#         logging.info(f"{self.thread.ovl}")
#
# app = QApplication(sys.argv)
# win = Window()
# win.show()
# sys.exit(app.exec())

import time, sys
# from pyqtgraph.Qt import QtGui, QtCore
# from PyQt4.Qt import QMutex
# import pyqtgraph as pg
from random import randint
from copy import copy

import pyqtgraph as pyqtgraph
from PyQt5 import QtCore, QtWidgets, QtGui


class DataGenerator(QtCore.QObject):
    newData = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, sizey=100, rangey=[0, 100], delay=1000):
        QtCore.QObject.__init__(self)
        self.parent = parent
        self.sizey = sizey
        self.rangey = rangey
        self.delay = delay
        self.mutex = QtCore.QMutex()
        self.y = [0 for i in range(sizey)]
        self.run = True

    def generateData(self):
        while self.run:
            try:
                self.mutex.lock()
                for i in range(self.sizey):
                    self.y[i] = randint(*self.rangey)
                self.mutex.unlock()
                self.newData.emit(self.y)
                QtCore.QThread.msleep(self.delay)
            except:
                pass


class MainWin(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        x_axis_min_range = 0
        x_axis_max_range = 100

        y_axis_min_range = 0
        y_axis_max_range = 100

        win2 = pyqtgraph.GraphicsWindow(title="Test Plots")
        win2.resize(640, 480)
        pyqtgraph.setConfigOptions(antialias=True)
        self.setCentralWidget(win2)

        self.p1 = win2.addPlot(title="Plot 1")
        self.p1curve = self.p1.plot(pen=(255, 0, 0))
        self.p1.showGrid(x=True, y=True)
        self.p1.setYRange(y_axis_min_range, y_axis_max_range)
        self.p1.setXRange(x_axis_min_range, x_axis_max_range)

        self.p2 = win2.addPlot(title="Plot 2")
        self.p2curve = self.p2.plot(pen=(0, 255, 0))
        self.p2.showGrid(x=True, y=True)
        self.p2.setYRange(y_axis_min_range, y_axis_max_range)
        self.p2.setXRange(x_axis_min_range, x_axis_max_range)

        self.x1 = range(1, 101)
        self.thread1 = QtCore.QThread()
        self.dgen1 = DataGenerator(self, len(self.x1), [0, 100], 1000)
        self.dgen1.moveToThread(self.thread1)
        self.dgen1.newData.connect(self.update_plot1)
        self.thread1.started.connect(self.dgen1.generateData)
        self.thread1.start()

        self.x2 = range(1, 101)
        self.thread2 = QtCore.QThread()
        self.dgen2 = DataGenerator(self, len(self.x2), [0, 100], 1)
        self.dgen2.moveToThread(self.thread2)
        self.dgen2.newData.connect(self.update_plot2)
        self.thread2.started.connect(self.dgen2.generateData)
        self.thread2.start()

    def update_plot1(self, y):
        if self.dgen1.mutex.tryLock():
            y1 = copy(y)
            self.dgen1.mutex.unlock()
            self.p1curve.setData(self.x1, y1)

    def update_plot2(self, y):
        if self.dgen2.mutex.tryLock():
            y2 = copy(y)
            self.dgen2.mutex.unlock()
            self.p2curve.setData(self.x2, y2)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWin()
    main.show()
    sys.exit(app.exec_())