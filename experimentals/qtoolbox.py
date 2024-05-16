import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel, QToolBox, QPushButton, QTextEdit, QLineEdit)
from PyQt5.QtGui import QColor

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        layout = QGridLayout()

        styleSheet = """
                        QToolBox::tab {
                            border: 1px solid #C4C4C3;
                            border-bottom-color: RGB(0, 0, 255);                            
                        }
                        QToolBox::tab:selected {
                            background-color: #f14040;
                            border-bottom-style: none;
                        }
                     """

        toolbox = QToolBox()
        layout.addWidget(toolbox, 0, 0)

        # tab X
        w1 = QWidget()
        layout1 = QVBoxLayout()

        self.lineEdit = QLineEdit()
        layout1.addWidget(QLabel('Enter something'))
        layout1.addWidget(self.lineEdit)
        w1.setLayout(layout1)

        toolbox.addItem(w1, 'Tab X')

        # tab Y
        btn = QPushButton('My Button')
        btn.clicked.connect(self.printText)
        toolbox.addItem(btn, 'Tab Y')

        # tab Z
        self.textEditor = QTextEdit()
        toolbox.addItem(self.textEditor, 'Tab Z')

        toolbox.setCurrentIndex(1)
        toolbox.setStyleSheet(styleSheet)
        toolbox.setItemToolTip(1, 'This is tab Y')
        self.setLayout(layout)

    def printText(self):
        self.textEditor.setPlainText(self.lineEdit.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())