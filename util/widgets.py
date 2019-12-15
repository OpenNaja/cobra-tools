import os
from PyQt5 import QtGui, QtCore, QtWidgets

from util import config, qt_theme

myFont=QtGui.QFont()
myFont.setBold(True)

def startup(cls):
	appQt = QtWidgets.QApplication([])
	
	#style
	appQt.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
	appQt.setPalette(qt_theme.dark_palette)
	appQt.setStyleSheet("QToolTip { color: #ffffff; background-color: #353535; border: 1px solid white; }")
	
	win = cls()
	win.show()
	appQt.exec_()
	config.write_config("config.ini", win.cfg)

def abort_open_new_file(parent, newfile, oldfile):
	# only return True if we should abort
	if newfile == oldfile:
		return True
	if oldfile:
		qm = QtWidgets.QMessageBox
		return qm.No == qm.question(parent.parent,'', "Do you really want to load "+os.path.basename(newfile)+"? You will lose unsaved work on "+os.path.basename(oldfile)+"!", qm.Yes | qm.No)

def showdialog(str):
	msg = QtWidgets.QMessageBox()
	msg.setIcon(QtWidgets.QMessageBox.Information)
	msg.setText(str)
	#msg.setInformativeText("This is additional information")
	msg.setWindowTitle("Error")
	#msg.setDetailedText("The details are as follows:")
	msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
	retval = msg.exec_()

def vbox(parent, grid):
	"""Adds a grid layout"""
	# vbox = QtWidgets.QVBoxLayout()
	# vbox.addLayout(grid)
	# vbox.addStretch(1.0)
	# vbox.setSpacing(0)
	# vbox.setContentsMargins(0,0,0,0)
	parent.setLayout(grid)

class LabelEdit(QtWidgets.QWidget):
	def __init__(self, name):
		QtWidgets.QWidget.__init__(self,)
		self.shader_container = QtWidgets.QWidget()
		self.label = QtWidgets.QLabel(name)
		self.entry = QtWidgets.QLineEdit()
		vbox = QtWidgets.QHBoxLayout()
		vbox.addWidget(self.label)
		vbox.addWidget(self.entry)
		# vbox.addStretch(1)
		self.setLayout(vbox)

class MySwitch(QtWidgets.QPushButton):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.setCheckable(True)
		self.setMinimumWidth(66)
		self.setMinimumHeight(22)

	def setValue(self, v):
		self.setChecked(v)

	def paintEvent(self, event):
		label = "ON" if self.isChecked() else "OFF"
		bg_color = QtCore.Qt.green if self.isChecked() else QtCore.Qt.red

		radius = 10
		width = 32
		center = self.rect().center()

		painter = QtGui.QPainter(self)
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		painter.translate(center)
		painter.setBrush(QtGui.QColor(0,0,0))

		pen = QtGui.QPen(QtCore.Qt.black)
		pen.setWidth(2)
		painter.setPen(pen)

		painter.drawRoundedRect(QtCore.QRect(-width, -radius, 2*width, 2*radius), radius, radius)
		painter.setBrush(QtGui.QBrush(bg_color))
		sw_rect = QtCore.QRect(-radius, -radius, width + radius, 2*radius)
		if not self.isChecked():
			sw_rect.moveLeft(-width)
		painter.drawRoundedRect(sw_rect, radius, radius)
		painter.drawText(sw_rect, QtCore.Qt.AlignCenter, label)

class VectorEntry():
	def __init__(self, attrib, tooltips={}):
		"""attrib must be pyffi attrib object"""
		# QtWidgets.QWidget.__init__(self,)
		self.attrib = attrib
		self.label = QtWidgets.QLabel(attrib.name)
		
		self.data = QtWidgets.QWidget()
		layout = QtWidgets.QHBoxLayout()
		buttons = [self.create_field(i) for i in range(len(attrib.value))]
		for button in buttons:
			layout.addWidget(button)
		self.data.setLayout(layout)

		# get tooltip
		tooltip = tooltips.get(self.attrib.name, "Undocumented attribute.")
		self.data.setToolTip(tooltip)
		self.label.setToolTip(tooltip)

	
	def create_field(self, ind):
		default = self.attrib.value[ind]

		def update_ind( v):
			# use a closure to remember index
			# print(self.attrib, ind, v)
			self.attrib.value[ind] = v

		t = str(type(default))
		if "float" in t:
			field = QtWidgets.QDoubleSpinBox()
			field.setDecimals(3)
			field.setRange(-10000, 10000)
			field.setSingleStep(.05)
			field.valueChanged.connect(update_ind)
		elif "bool" in t:
			# field = QtWidgets.QSpinBox()
			field = MySwitch()
			field.clicked.connect(update_ind)
		elif "int" in t:
			field = QtWidgets.QSpinBox()
			field.setRange(-10000, 10000)
			field.valueChanged.connect(update_ind)

		field.setValue(default)
		field.setMinimumWidth(50)
		return field
	
	# @property
	# def fft_size(self): return int(self.fft_c.currentText())
	
	# @property
	# def fft_overlap(self): return int(self.overlap_c.currentText())
	
	# def update_fft_settings(self,):
	# 	self.canvas.compute_spectra(self.canvas.filenames,
	# 								fft_size = self.fft_size,
	# 								fft_overlap = self.fft_overlap)
		
	# def update_show_settings(self):
	# 	show = self.show_c.currentText()
				
	# def update_cmap(self):
	# 	self.canvas.set_colormap(self.cmap_c.currentText())	

class FileWidget(QtWidgets.QLineEdit):
	"""An entry widget that starts a file selector when clicked and also accepts drag & drop.
	Displays the current file's basename.
	"""

	def __init__(self, parent, cfg, description="", ask_user=True):
		super(FileWidget, self).__init__(parent)
		self.parent = parent
		self.cfg = cfg
		if not self.cfg:
			self.cfg["dir_in"]  = "C://"
		self.setDragEnabled(True)
		self.setReadOnly(True)
		self.filepath = ""
		self.description = description
		self.setToolTip(self.description)
		self.ask_user = ask_user
			
	def abort_open_new_file(self, new_filepath):
		# only return True if we should abort
		if not self.ask_user:
			return False
		if new_filepath == self.filepath:
			return True
		if self.filepath:
			qm = QtWidgets.QMessageBox
			return qm.No == qm.question(self,'', "Do you really want to load "+os.path.basename(new_filepath)+"? You will lose unsaved work on "+os.path.basename(self.filepath)+"!", qm.Yes | qm.No)
			
	def accept_file(self, filepath):
		if os.path.isfile(filepath):
			if os.path.splitext(filepath)[1].lower() in (".flac", ".wav"):
				if not self.abort_open_new_file(filepath):
					self.filepath = filepath
					self.cfg["dir_in"], filename = os.path.split(filepath)
					self.setText(filename)
					self.parent.poll()
			else:
				showdialog("Unsupported File Format")
				
	def get_files(self, event):
		data = event.mimeData()
		urls = data.urls()
		if urls and urls[0].scheme() == 'file':
			return urls
		
	def dragEnterEvent(self, event):
		if self.get_files(event):
			event.acceptProposedAction()
			self.setFocus(True)

	def dragMoveEvent(self, event):
		if self.get_files(event):
			event.acceptProposedAction()
			self.setFocus(True)

	def dropEvent(self, event):
		urls = self.get_files(event)
		if urls:
			filepath = str(urls[0].path())[1:]
			self.accept_file(filepath)
			
	def ask_open(self):
		filepath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open '+self.description, self.cfg["dir_in"], "Audio files (*.flac *.wav)")[0]
		self.accept_file(filepath)
		
	def mousePressEvent(self, event):
		self.ask_open()

class MainWindow(QtWidgets.QMainWindow):

	def __init__(self, name, ):
		QtWidgets.QMainWindow.__init__(self)		
		
		self.central_widget = QtWidgets.QWidget(self)
		self.setCentralWidget(self.central_widget)
		
		self.name = name
		# self.resize(720, 400)
		self.setWindowTitle(name)
		try:
			base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
			self.setWindowIcon(QtGui.QIcon(os.path.join(base_dir,'icons/frontier.png')))
		except: pass
		
		self.cfg = config.read_config("config.ini")
		

	def update_file(self, filepath):
		self.cfg["dir_in"], file_name = os.path.split(filepath)
		self.setWindowTitle(self.name+" "+ file_name)
		
	def add_to_menu(self, button_data):
		for submenu, name, func, shortcut in button_data:
			button = QtWidgets.QAction(name, self)
			button.triggered.connect(func)
			if shortcut: button.setShortcut(shortcut)
			submenu.addAction(button)
			