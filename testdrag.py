import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import tempfile
import os


class DelayedMimeData(QtCore.QMimeData):
    def __init__(self):
        super().__init__()
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def retrieveData(self, mime_type: str, preferred_type: QtCore.QVariant.Type):
        for callback in self.callbacks.copy():
            result = callback()
            if result:
                self.callbacks.remove(callback)
        return QtCore.QMimeData.retrieveData(self, mime_type, preferred_type)


class DragTest(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.addItems(['one', 'two', 'three', 'four'])
        self.setSelectionMode(self.MultiSelection)

    def startDrag(self, actions):
        drag = QtGui.QDrag(self)
        names = [item.text() for item in self.selectedItems()]
        print("DRAGGING", names)
        mime = DelayedMimeData()
        path_list = []
        for name in names:
            path = os.path.join(tempfile.gettempdir(), 'DragTest', name + ".txt")
            os.makedirs(os.path.dirname(path), exist_ok=True)

            def write_to_file(path=path, contents=name, widget=self):
                print(path)
                if widget.underMouse():
                    return False
                else:
                    with open(path, 'w') as f:
                        import time
                        time.sleep(1)  # simulate large file
                        f.write(contents)

                    return True

            mime.add_callback(write_to_file)

            path_list.append(QtCore.QUrl.fromLocalFile(path))
        mime.setUrls(path_list)
        drag.setMimeData(mime)
        drag.exec_(Qt.CopyAction)


if __name__ == "__main__":
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    w = DragTest()
    w.show()

    app.exec_()