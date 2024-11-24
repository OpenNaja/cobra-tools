# from https://stackoverflow.com/questions/64252654/pyqt5-drag-and-drop-into-system-file-explorer-with-delayed-encoding?noredirect=1&lq=1

import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import tempfile
import os

# Use win32api on Windows because the pynput and mouse packages cause lag
# https://github.com/moses-palmer/pynput/issues/390
if os.name == 'nt':
    import win32api


    def mouse_pressed():
        return win32api.GetKeyState(0x01) not in [0, 1]
else:
    import mouse


    def mouse_pressed():
        return mouse.is_pressed()


class DelayedMimeData(QtCore.QMimeData):
    def __init__(self):
        super().__init__()
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def retrieveData(self, mime_type: str, preferred_type: QtCore.QVariant.Type):
        if not mouse_pressed():
            for callback in self.callbacks.copy():
                self.callbacks.remove(callback)
                callback()

        return QtCore.QMimeData.retrieveData(self, mime_type, preferred_type)


class Navigator(QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setHeaderLabels(["Name"])
        QtWidgets.QTreeWidgetItem(self, ['Test1'])
        QtWidgets.QTreeWidgetItem(self, ['Test2'])
        QtWidgets.QTreeWidgetItem(self, ['Test3'])

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(self.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(self.ExtendedSelection)
        self.setSelectionBehavior(self.SelectRows)

        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def startDrag(self, actions):
        drag = QtGui.QDrag(self)
        names = [item.text(0) for item in self.selectedItems()]
        mime = DelayedMimeData()
        path_list = []
        for name in names:
            path = os.path.join(tempfile.gettempdir(), 'DragTest', name + '.txt')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            print(path)

            def write_to_file(path=path, name=name, widget=self):
                with open(path, 'w+') as f:
                    print("Writing large file(s)...")
                    time.sleep(2)  # Sleep to simulate long file write
                    f.write(f"Contents of {name}")

            mime.add_callback(write_to_file)
            path_list.append(QtCore.QUrl.fromLocalFile(path))

        mime.setUrls(path_list)
        # mime.setData('application/x-qabstractitemmodeldatalist',
        #              self.mimeData(self.selectedItems()).data('application/x-qabstractitemmodeldatalist'))
        drag.setMimeData(mime)
        drag.exec_(Qt.MoveAction)
        super().startDrag(actions)


app = QtWidgets.QApplication([])

nav = Navigator()
nav.show()
app.exec_()
