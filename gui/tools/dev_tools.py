import sys
from pathlib import PurePath
from typing import TYPE_CHECKING

from utils import is_dev_environment

try:
	import faulthandler
	from PyQt5.QtCore import qInstallMessageHandler, QtMsgType
except ImportError:
	# Handle case where PyQt5 might not be installed yet
	qInstallMessageHandler = None

if TYPE_CHECKING:
	from PyQt5.QtCore import QMessageLogContext, QtMsgType


def _qt_message_handler(mode: 'QtMsgType', context: 'QMessageLogContext', message: str) -> None:
	"""Internal Qt message handler to dump tracebacks on fatal errors."""
	from PyQt5.QtCore import QtMsgType
	category = f" [{context.category}]" if context.category != "default" else ""
	if QtMsgType is not None:
		if mode == QtMsgType.QtSystemMsg:
			print(f"QT_SYSTEM |{category} {message}")
		elif mode == QtMsgType.QtWarningMsg:
			print(f"QT_WARNING |{category} {message}")
		elif mode == QtMsgType.QtCriticalMsg:
			print(f"QT_CRITICAL |{category} {message}", file=sys.stderr)
		elif mode == QtMsgType.QtFatalMsg:
			print(f"QT_FATAL |{category} {message}", file=sys.stderr)
			faulthandler.dump_traceback(file=sys.stderr)
			sys.exit(1)


def setup_dev_diagnostics():
	"""
	Sets up developer-specific diagnostic tools.
	- Enables faulthandler to dump tracebacks on crashes.
	- Installs a custom Qt message handler to catch fatal Qt errors.
	"""
	if not is_dev_environment():
		return
	import logging
	logging.basicConfig(level=logging.DEBUG)

	# Enable faulthandler
	try:
		faulthandler.enable(all_threads=True)
	except Exception as e:
		print(f"Failed to enable faulthandler: {e}")

	# Install Qt message handler
	if qInstallMessageHandler:
		try:
			qInstallMessageHandler(_qt_message_handler)
		except Exception as e:
			print(f"Failed to install Qt message handler: {e}")
