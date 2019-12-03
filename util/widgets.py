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
			