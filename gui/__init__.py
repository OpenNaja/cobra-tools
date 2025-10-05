import sys
import time
import logging
import platform
from dataclasses import dataclass
from typing import NamedTuple, Optional
from pathlib import Path
from ovl_util import auto_updater, logs
from ovl_util.config import save_config
from gui.widgets import MainWindow
from gui.tools.layout_visualizer import install_layout_visualizer
from gui import qt_theme

from PyQt5.QtCore import Qt, qVersion
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication, QStyleFactory

root_dir = Path(__file__).resolve().parent.parent

def check_64bit_env() -> None:
	is_64bits = sys.maxsize > 2 ** 32
	if not is_64bits:
		logging.warning(
			"Either your operating system or your python installation is not 64 bits. "
			"Large OVLs will crash unexpectedly!")

def register_fonts(directory: Path):
	"""
	Scans a directory for .ttf files and registers them with the QApplication.
	"""
	if not directory.is_dir():
		print(f"Error: Font directory not found at '{directory}'")
		return

	# Iterate over all files in the directory with a .ttf extension
	for font_file in directory.glob("*.ttf"):
		try:
			font_id = QFontDatabase.addApplicationFont(str(font_file))
			# QFontDatabase.addApplicationFont returns -1 on failure
			if font_id == -1:
				print(f"Error: Failed to load font: {font_file.name}")
		except Exception as e:
			print(f"Error: An exception occurred while loading {font_file.name}: {e}")


class Size(NamedTuple):
	width: int
	height: int


@dataclass
class GuiOptions:
	"""
	A dataclass to hold GUI and application configuration options.
	
	The 'size' attribute can be initialized with either a Size object or a
	tuple like (width, height), and it will be automatically converted.
	"""
	log_name: str
	log_to_file: bool = True
	log_to_stdout: bool = True
	log_backup_count: int = 4
	size: Size = Size(800, 600)
	logger_width: int = 320
	logger_height: int = 200
	qapp: Optional[QApplication] = None
	frameless: bool = True
	style: str = "Fusion"
	qss_file: str = ""
	stylesheet: str = R"""
		QToolTip { color: #ffffff; background-color: #353535; border: 1px solid white; }
	"""
	debug_layout: bool = False

	def __post_init__(self):
		if isinstance(self.size, tuple):
			# Convert it to a proper Size NamedTuple instance.
			self.size = Size(*self.size)


def init(cls: type[MainWindow], opts: GuiOptions) -> tuple[MainWindow, QApplication]:
	"""Initialize the window class, logs, and QApplication if necessary"""
	handler = logs.logging_setup(opts.log_name,
								 log_to_file=opts.log_to_file,
								 log_to_stdout=opts.log_to_stdout,
								 backup_count=opts.log_backup_count)
	check_64bit_env()
	app = opts.qapp
	if app is None:
		if qVersion().startswith("5."):
			QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
			QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
			QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
		app = QApplication([])

	# Register Fonts
	font_dir = root_dir / 'gui' / 'fonts'
	register_fonts(font_dir)

	win = cls(opts=opts)
	win.set_log_name(opts.log_name)
	win.stdout_handler = handler
	win.activateWindow()
	return win, app


def startup(cls: type[MainWindow], opts: GuiOptions) -> None:
	"""Startup the window, set the theme, handle config and logs on application exit"""
	auto_updater.run_update_check(tool_name=opts.log_name)
	if platform.system() == "Windows":
		import ctypes
		myappid = 'Open Naja OVL Tools'  # arbitrary string
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
	win, app_qt = init(cls, opts)

	app_qt.setStyle(QStyleFactory.create(opts.style))
	app_qt.setPalette(win.get_palette_from_cfg())
	if opts.qss_file:
		with open(opts.qss_file, "r") as qss:
			app_qt.setStyleSheet(qss.read())
	elif opts.stylesheet:
		app_qt.setStyleSheet(opts.stylesheet)

	if opts.debug_layout:
		install_layout_visualizer(win)

	win.show()
	app_qt.exec_()
	cfg_path = Path(__file__).resolve().parent.parent / "config.json"
	save_config(cfg_path, win.cfg)
	logging.shutdown()
