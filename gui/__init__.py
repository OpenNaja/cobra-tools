import os
import sys
import time
import logging
import shutil
from pathlib import Path
from ovl_util import logs, config
from gui import qt_theme
from gui.widgets import MainWindow

from PyQt5.QtWidgets import QApplication, QStyleFactory


def check_python() -> None:
	"""Require Python >= 3.11"""
	if (sys.version_info.major, sys.version_info.minor) < (3, 11):
		logging.critical("Python 3.11 or later is required. Please update your Python installation.")
		time.sleep(60)


def init(cls: type[MainWindow], filepath: str, app: QApplication | None = None) -> tuple[MainWindow, QApplication]:
	"""Initialize the window class, logs, and QApplication if necessary"""
	log_name = Path(filepath).stem
	handler = logs.logging_setup(log_name)
	check_python()
	if app is None:
		app = QApplication([])
	win = cls()
	win.set_log_name(log_name)
	win.stdout_handler = handler
	win.activateWindow()
	return win, app


def startup(cls: type[MainWindow], filepath: str, app: QApplication | None = None) -> None:
	"""Startup the window, set the theme, handle config and logs on application exit"""
	win, app_qt = init(cls, filepath, app)
	win.show()
	if not win.cfg.get("light_theme", False):
		app_qt.setStyle(QStyleFactory.create('Fusion'))
		app_qt.setPalette(qt_theme.dark_palette)
		app_qt.setStyleSheet("QToolTip { color: #ffffff; background-color: #353535; border: 1px solid white; }")
	app_qt.exec_()
	config.save_config(win.cfg)
	logging.shutdown()
