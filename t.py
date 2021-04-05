# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class EditableCombo(QComboBox):

	def __init__(self, parent):
		super().__init__(parent)


class CleverCombo(QtWidgets.QComboBox):
	""""A combo box that supports setting content (existing or new), and a callback"""

	def __init__(self, options=[], link_inst=None, link_attr=None, *args, **kwargs):
		super(CleverCombo, self).__init__(*args, **kwargs)
		self.addItems(options)
		self.link_inst = link_inst
		self.link_attr = link_attr
		if link_inst and link_attr:
			name = str(getattr(link_inst, link_attr))
			self.setText(name)
			self.currentIndexChanged.connect(self.update_name)

	def setText(self, txt):
		flag = QtCore.Qt.MatchFixedString
		indx = self.findText(txt, flags=flag)
		# add new item if not found
		if indx == -1:
			self.addItem(txt)
			indx = self.findText(txt, flags=flag)
		self.setCurrentIndex(indx)

	def update_name(self, ind):
		"""Change data on pyffi struct if gui changes"""
		setattr(self.link_inst, self.link_attr, self.currentText())


class EditCombo(QtWidgets.QWidget):
	def __init__(self, parent, ):
		super(EditCombo, self).__init__(parent)
		self.add_button = QtWidgets.QPushButton("+")
		self.delete_button = QtWidgets.QPushButton("-")
		self.entry = QtWidgets.QComboBox()
		self.entry.setEditable(True)
		vbox = QtWidgets.QHBoxLayout(self)
		vbox.addWidget(self.entry)
		vbox.addWidget(self.add_button)
		vbox.addWidget(self.delete_button)

	def setText(self, txt):
		flag = QtCore.Qt.MatchFixedString
		indx = self.findText(txt, flags=flag)
		# add new item if not found
		if indx == -1:
			self.addItem(txt)
			indx = self.findText(txt, flags=flag)
		self.setCurrentIndex(indx)

	def set_data(self, items):
		self.entry.clear()
		self.entry.addItems(items)


class Window(QMainWindow):

	def __init__(self):
		super().__init__()

		# setting title
		self.setWindowTitle("Python ")

		# setting geometry
		self.setGeometry(100, 100, 600, 400)

		# calling method
		self.UiComponents()

		# showing all the widgets
		self.show()

	# method for widgets
	def UiComponents(self):
		# creating a combo box widget
		# geek list
		options = ["Geek", "Geeky Geek", "Legend Geek", "Ultra Legend Geek"]
		self.combo_box = LabelCombo(self, )

		# setting geometry of combo box
		# self.combo_box.setGeometry(200, 150, 120, 30)

		# creating a editable combo box
		# self.combo_box.setEditable(True)


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())