from __future__ import annotations
from __version__ import VERSION, COMMIT_HASH, COMMIT_TIME
import logging
import os
import platform
import sys
import tempfile
from functools import partialmethod, partial
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
from queue import Queue
from typing import TextIO

from ovl_util.config import load_config
# TODO: log_dir and config_path used in this file should be parameterized instead of hardcoded based on root_dir
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
cfg_path = os.path.join(root_dir, "config.json")

shorten_paths = {
	root_dir: os.path.basename(root_dir),
	tempfile.gettempdir(): "TEMP",
	os.path.expanduser('~'): "USER",
}
for game_name, game_path in load_config(cfg_path).get("games", {}).items():
	prefix, suffix = game_path.split(game_name)
	pre_path = os.path.normpath(os.path.join(prefix, game_name))
	shorten_paths[pre_path] = game_name


def shorten_str(msg):
	for k, v in shorten_paths.items():
		msg = msg.replace(k, v)
		msg = msg.replace(k.replace("\\", "/"), v)
		msg = msg.replace(k.replace("/", "\\"), v)
	return msg


class ANSI:
	""" ANSI color codes """
	BLACK = "\x1b[0;30m"
	RED = "\x1b[0;31m"
	GREEN = "\x1b[0;32m"
	YELLOW = "\x1b[0;33m"
	BLUE = "\x1b[0;34m"
	PURPLE = "\x1b[0;35m"
	CYAN = "\x1b[0;36m"
	LIGHT_GRAY = "\x1b[0;37m"
	DARK_GRAY = "\x1b[1;30m"
	LIGHT_RED = "\x1b[1;31m"
	LIGHT_GREEN = "\x1b[1;32m"
	LIGHT_YELLOW = "\x1b[1;33m"
	LIGHT_BLUE = "\x1b[1;34m"
	LIGHT_PURPLE = "\x1b[1;35m"
	LIGHT_CYAN = "\x1b[1;36m"
	LIGHT_WHITE = "\x1b[1;37m"
	BOLD = "\x1b[1m"
	FAINT = "\x1b[2m"
	ITALIC = "\x1b[3m"
	UNDERLINE = "\x1b[4m"
	BLINK = "\x1b[5m"
	NEGATIVE = "\x1b[7m"
	CROSSED = "\x1b[9m"
	END = "\x1b[0m"

	# Cancel SGR codes if we don't write to a colored terminal
	if not sys.stdout.isatty() or (platform.system() == "Windows" and platform.release() not in ("10", "11")):
		for _ in dir():
			if isinstance(_, str) and _[0] != "_":
				locals()[_] = ""
	else:
		# Set Windows console
		if platform.system() == "Windows":
			os.system("color")


class ShorteningFormatter(logging.Formatter):

	def format(self, record):
		msg = super().format(record)
		return shorten_str(msg)


class LogBackupFileHandler(RotatingFileHandler):

	def __init__(self, filename: str, mode: str = "a", maxBytes: int = 0,
				 backupCount: int = 0, encoding: str | None = None, delay: bool = False, errors: str | None = None) -> None:
		super().__init__(filename, mode, maxBytes, backupCount, encoding, delay, errors)
		self.log_dir = os.path.join(root_dir + "/logs")
		os.makedirs(self.log_dir, exist_ok=True)

	def doRollover(self) -> None:
		if self.stream:
			self.stream.close()
			self.stream = None
		if self.backupCount > 0:
			try:
				path, ext = os.path.splitext(self.baseFilename)
				dir_path, basename = os.path.split(path)
				for i in range(self.backupCount - 1, 0, -1):
					sfn = self.rotation_filename(f"{self.log_dir}/{basename}-{i}{ext}")
					dfn = self.rotation_filename(f"{self.log_dir}/{basename}-{i+1}{ext}")
					if os.path.exists(sfn):
						if os.path.exists(dfn):
							os.remove(dfn)
						os.rename(sfn, dfn)
				dfn = self.rotation_filename(f"{self.log_dir}/{basename}-1{ext}")
				if os.path.exists(dfn):
					os.remove(dfn)
				self.rotate(self.baseFilename, dfn)
			except OSError:
				# The base log is opened by another process
				pass
		if not self.delay:
			self.stream = self._open()


class ColoredFormatter(logging.Formatter):

	def format(self, record):
		formatter = self.FORMATTERS.get(record.levelno)
		return formatter.format(record)


class LoggerFormatter(ColoredFormatter):
	"""A ColoredFormatter for rich text usage"""
	def __init__(self, fmt: str, datefmt: str = None, *args, **kwargs):
		super().__init__(fmt, datefmt, *args, **kwargs)
		fmt_n = "%(levelname)s | %(message)s\n%(details)s"
		self.FORMATS = {
			logging.DEBUG: fmt_n,
			logging.INFO: fmt_n,
			logging.INFO + 5: fmt_n, # SUCCESS
			logging.WARNING: fmt_n,
			logging.ERROR: fmt_n,
			logging.CRITICAL: fmt_n,
		}
		self.FORMATTERS = {key: logging.Formatter(_fmt, datefmt) for key, _fmt in self.FORMATS.items()}


class HtmlFormatter(ColoredFormatter):
	"""A ColoredFormatter for rich text usage"""
	# Special char for finding end of message
	eol = "\u00A0"

	def __init__(self, fmt: str, datefmt: str = None, *args, **kwargs):
		super().__init__(fmt, datefmt, *args, **kwargs)
		fmt_n = f"%(levelname)s | %(message)s | <div class='msg_%(levelname)s'><span>%(message)s</span></div>{self.eol}%(details)s"
		fmt_b = f"%(levelname)s | %(message)s | <div class='msg_%(levelname)s'><span><b>%(message)s</b></span></div>{self.eol}%(details)s"
		self.FORMATS = {
			logging.DEBUG: fmt_n,
			logging.INFO: fmt_n,
			logging.INFO + 5: fmt_b, # SUCCESS
			logging.WARNING: fmt_n,
			logging.ERROR: fmt_b,
			logging.CRITICAL: fmt_b,
		}
		self.FORMATTERS = {key: logging.Formatter(_fmt, datefmt) for key, _fmt in self.FORMATS.items()}


class AnsiFormatter(ColoredFormatter):

	def __init__(self, fmt: str, datefmt: str = None, *args, **kwargs):
		super().__init__(fmt, datefmt, *args, **kwargs)
		self.FORMATS = {
			logging.DEBUG: f"{ANSI.DARK_GRAY}{self._fmt}{ANSI.END}",
			logging.INFO: f"{ANSI.LIGHT_WHITE}{self._fmt}{ANSI.END}",
			logging.INFO + 5: f"{ANSI.LIGHT_GREEN}{self._fmt}{ANSI.END}", # SUCCESS
			logging.WARNING: f"{ANSI.YELLOW}{self._fmt}{ANSI.END}",
			logging.ERROR: f"{ANSI.RED}{self._fmt}{ANSI.END}",
			logging.CRITICAL: f"{ANSI.LIGHT_RED}{self._fmt}{ANSI.END}"
		}
		self.FORMATTERS = {key: logging.Formatter(_fmt, datefmt) for key, _fmt in self.FORMATS.items()}


_global_listener: QueueListener | None = None
def get_global_listener() -> QueueListener | None:
	"""
	Returns the application-wide QueueListener instance
	"""
	return _global_listener


def addLoggingLevel(levelName, levelNum, methodName=None):
	"""
	Comprehensively adds a new logging level to the `logging` module and the
	currently configured logging class.

	`levelName` becomes an attribute of the `logging` module with the value
	`levelNum`. `methodName` becomes a convenience method for both `logging`
	itself and the class returned by `logging.getLoggerClass()` (usually just
	`logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
	used.

	Example
	-------
	>>> addLoggingLevel('TRACE', logging.DEBUG - 5)
	>>> logging.getLogger(__name__).setLevel("TRACE")
	>>> logging.getLogger(__name__).trace('that worked')
	>>> logging.trace('so did this')
	>>> logging.TRACE
	5

	"""
	if not methodName:
		methodName = levelName.lower()

	if hasattr(logging, levelName):
		return
	if hasattr(logging, methodName):
		return
	if hasattr(logging.getLoggerClass(), methodName):
		return

	logging.addLevelName(levelNum, levelName)
	setattr(logging, levelName, levelNum)
	setattr(logging.getLoggerClass(), methodName, partialmethod(logging.getLoggerClass().log, levelNum))
	setattr(logging, methodName, partial(logging.log, levelNum))


def logging_setup(log_name: str, log_to_file: bool = True,
				  log_to_stdout: bool = True, backup_count: int = 4) -> StreamHandler[TextIO]:
	"""
	Creates a colored ANSI formatter for stdout, and a file handler with log backups.
	This should be called before any logging statements, and logging statements in this
	function until after logger.addHandler().
	"""
	# Custom SUCCESS level
	addLoggingLevel('SUCCESS', logging.INFO + 5)

	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	# cf https://docs.python.org/3/library/logging.html#logrecord-attributes
	# '%(asctime)s %(levelname)s | %(module)s %(funcName)s - %(message)s', "%H:%M:%S"
	# formatter = logging.Formatter('%(levelname)s | %(message)s')
	formatter = ShorteningFormatter('%(levelname)s | %(message)s')
	# Colored logging for all platforms but Windows 7/8
	colored_formatter = AnsiFormatter('%(levelname)s | %(message)s')

	handlers: list[StreamHandler] = []
	stdout_handler: StreamHandler | None = None
	if log_to_stdout:
		stdout_handler = StreamHandler(sys.stdout)
		stdout_handler.setLevel(logging.INFO)
		stdout_handler.setFormatter(colored_formatter)
		stdout_handler.set_name(log_name)
		handlers.append(stdout_handler)

	file_handler: LogBackupFileHandler | None = None
	if log_to_file:
		log_path = f'{os.path.join(root_dir, log_name)}.log'
		file_handler = LogBackupFileHandler(log_path, mode="w", backupCount=backup_count, delay=True, encoding="utf-8")
		file_handler.setLevel(logging.DEBUG) # always write all levels to file log
		file_handler.setFormatter(formatter)
		file_handler.set_name(log_name)
		file_handler.doRollover()
		handlers.append(file_handler)

	# Setup the async queue
	log_queue = Queue(-1)  # -1 == inf
	# Only QueueHandler on root logger
	queue_handler = QueueHandler(log_queue)

	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	# Remove any existing handlers and add only the queue handler
	logger.handlers.clear()
	logger.addHandler(queue_handler)

	# Distribute the logs to the real handlers
	global _global_listener
	_global_listener = QueueListener(log_queue, *handlers, respect_handler_level=True)
	_global_listener.start()

	logger.info(f"Running python {sys.version}")
	logger.info(f"Running cobra-tools {get_version_str()}, {get_commit_str()}")
	return stdout_handler


def get_stdout_handler(name: str) -> StreamHandler | None:
	"""
	Finds the named stdout handler by searching the global QueueListener.
	"""
	listener = get_global_listener()
	if listener:
		# Search its list of handlers
		for handler in listener.handlers:
			if isinstance(handler, StreamHandler) and handler.stream == sys.stdout and handler.name == name:
				return handler
	return None


def get_version_str():
	return VERSION


def get_commit_str():
	return f"{COMMIT_HASH} - {COMMIT_TIME}"
