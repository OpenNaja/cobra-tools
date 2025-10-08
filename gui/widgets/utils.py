from PyQt5 import QtWidgets


def get_main_window():
	from gui.widgets.window import MainWindow
	for w in QtWidgets.qApp.topLevelWidgets():
		if isinstance(w, MainWindow):
			return w
