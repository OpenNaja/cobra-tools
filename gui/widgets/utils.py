

def get_main_window():
	from PyQt5.QtWidgets import qApp
	from gui.widgets.window import MainWindow
	for w in qApp.topLevelWidgets():
		if isinstance(w, MainWindow):
			return w
