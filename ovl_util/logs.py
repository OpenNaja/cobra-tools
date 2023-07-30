import logging
import os
import platform
import sys
from functools import partialmethod, partial

from root_path import root_dir


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
	if not sys.stdout.isatty() or (platform.system() == "Windows" and int(platform.release()) < 10):
		for _ in dir():
			if isinstance(_, str) and _[0] != "_":
				locals()[_] = ""
	else:
		# Set Windows console
		if platform.system() == "Windows":
			os.system("color")


class ColoredFormatter(logging.Formatter):

	def format(self, record):
		formatter = self.FORMATTERS.get(record.levelno)
		return formatter.format(record)


class HtmlFormatter(ColoredFormatter):

	def __init__(self, fmt: str, datefmt: str = None, *args, **kwargs):
		super().__init__(fmt, datefmt, *args, **kwargs)
		self.FORMATS = {
			logging.DEBUG: f"<div style='color:gray;'>{self._fmt}</div>",
			logging.INFO: f"<div style='color:white;'>{self._fmt}</div>",
			logging.INFO + 5: f"<div style='color:lime;'>{self._fmt}</div>", # SUCCESS
			logging.WARNING: f"<div style='color:yellow;'>{self._fmt}</div>",
			logging.ERROR: f"<div style='color:red;'>{self._fmt}</div>",
			logging.CRITICAL: f"<div style='color:red;'>{self._fmt}</div>",
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


def logging_setup(log_name):
	addLoggingLevel('SUCCESS', logging.INFO + 5)
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	# cf https://docs.python.org/3/library/logging.html#logrecord-attributes
	# '%(asctime)s %(levelname)s | %(module)s %(funcName)s - %(message)s', "%H:%M:%S"
	formatter = logging.Formatter('%(levelname)s | %(message)s')
	# Colored logging for all platforms but Windows 7/8
	colored_formatter = AnsiFormatter('%(levelname)s | %(message)s')

	stdout_handler = logging.StreamHandler(sys.stdout)
	stdout_handler.setLevel(logging.INFO)
	stdout_handler.setFormatter(colored_formatter)
	# always write all levels to debug log
	log_path = f'{os.path.join(root_dir, log_name)}.log'
	file_handler = logging.FileHandler(log_path, mode="w")
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	logger.addHandler(stdout_handler)

	logging.info(f"Running python {sys.version}")
	logging.info(f"Running cobra-tools {get_version_str()}, {get_commit_str()}")
	return stdout_handler


def get_stdout_handler():
	return next(h for h in logging.getLogger().handlers if type(h) is logging.StreamHandler)


def get_version():
	init_path = f'{os.path.join(root_dir, "__init__")}.py'
	with open(init_path, "r") as f:
		line = ""
		while '"version"' not in line:
			line = f.readline()
		# 	"version": (2, 3, 1),
		_, r = line.split("(", 1)
		version_raw, _ = r.split(")", 1)
		version = [int(x.strip()) for x in version_raw.split(",")]
	return version


def get_version_str():
	version_tuple = get_version()
	return '.'.join([str(x) for x in version_tuple])


def get_commit_str():
	with open(os.path.join(root_dir, "version.txt"), "r") as f:
		return f.read()