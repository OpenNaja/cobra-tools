from __future__ import annotations
from __version__ import VERSION, COMMIT_HASH, COMMIT_TIME
import logging
import os
import platform
import sys
import tempfile
import inspect
import pprint
import threading
from functools import partialmethod, partial
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
from queue import Queue
from contextlib import contextmanager, nullcontext
from typing import TextIO, Generator, Any

from ovl_util.config import load_config
# TODO: log_dir and config_path used in this file should be parameterized instead of hardcoded based on root_dir
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
cfg_path = os.path.join(root_dir, "config.json")

shorten_paths = {
	root_dir: os.path.basename(root_dir),
	tempfile.gettempdir(): "TEMP",
	os.path.expanduser('~'): "USER",
}
# TODO: This needs to stop executing on import
for game_name, game_info in load_config(cfg_path).get("games", {}).items():
	game_path = game_info["path"]
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


class LoggerFormatter(logging.Formatter):

	def __init__(self, fmt: str = "%(levelname)s | %(message)s\n%(details)s", datefmt: str = None, *args, **kwargs):
		super().__init__(fmt, datefmt, *args, **kwargs)


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


class DelegatingFormatter(logging.Formatter):
	def __init__(self, initial_formatter: logging.Formatter):
		self._delegate = initial_formatter
		self._lock = threading.Lock()

	def format(self, record: logging.LogRecord) -> str:
		# Check if a temporary formatter was attached to this specific record.
		if hasattr(record, "temporary_formatter"):
			# Use the record-specific formatter.
			return record.temporary_formatter.format(record)
		
		# Otherwise, use the handler's default delegate formatter.
		with self._lock:
			return self._delegate.format(record)

	def set_delegate(self, new_delegate: logging.Formatter):
		with self._lock:
			self._delegate = new_delegate

	@property
	def delegate(self) -> logging.Formatter:
		with self._lock:
			return self._delegate


# A simple filter that attaches a formatter to a record.
class TemporaryFormatFilter(logging.Filter):
	def __init__(self, formatter: logging.Formatter):
		super().__init__()
		self.formatter = formatter

	def filter(self, record: logging.LogRecord) -> bool:
		record.temporary_formatter = self.formatter
		return True


@contextmanager
def temporary_formatter(
	formatter: str | logging.Formatter
) -> Generator[None, Any, None]:
	"""
	Thread-safe, race-free context manager that uses a filter to attach a temporary
	formatter directly to LogRecords.
	"""
	if isinstance(formatter, str):
		new_formatter = logging.Formatter(formatter)
	else:
		new_formatter = formatter

	temp_filter = TemporaryFormatFilter(new_formatter)
	
	logger = logging.getLogger()
	try:
		logger.addFilter(temp_filter)
		yield
	finally:
		logger.removeFilter(temp_filter)


_trace_counter = 0

def tracepoint(log_locals: bool = True, fprint: bool = True, fmt: str = "%(message)s"):
	"""
	Logs a detailed trace point with the file, line number, function name,
	and optionally the local variables of the caller.

	Args:
		locals (bool): If True, logs the local variables of the caller.
		fprint (bool): If True, default `fmt` removes `DEBUG | ` from each line.
		fmt (str):  The default format for fprint.
	"""
	
	global _trace_counter
	_trace_counter += 1
	
	# --- Trace Info ---
	caller_frame = inspect.stack()[1]
	filename = caller_frame.filename
	line_number = caller_frame.lineno
	function_name = caller_frame.function
	try:
		rel_filename = os.path.relpath(filename, root_dir).replace("\\", "/")
	except ValueError:
		rel_filename = filename.replace("\\", "/")

	# --- Conditional Setup ---
	context = temporary_formatter(fmt) if fprint else nullcontext()

	# --- Execution ---
	with context:
		# The first line is always logged
		log_message = (
			f"[📍 TRACE {_trace_counter:03}] {rel_filename}:{line_number} "
			f"in {function_name}()"
		)
		logging.debug(log_message)

		if log_locals:
			local_vars = caller_frame.frame.f_locals
			formatted_locals = pprint.pformat(local_vars, indent=2, width=100)

			logging.debug("--- Local Variables ---")
			for line in formatted_locals.splitlines():
				logging.debug(line)
			logging.debug("-----------------------")


def toggle_timestamps(enable: bool, date_format: str = "%H:%M:%S") -> None:
	"""
	Adds or removes timestamps (including milliseconds) from all handlers 
	managed by the global listener.

	This function inspects the delegate formatter of each handler's 
	DelegatingFormatter. It preserves the original formatter class (e.g., 
	AnsiFormatter, ShorteningFormatter) and prepends the timestamp format.

	Args:
		enable (bool): If True, adds timestamps. If False, removes them.
		date_format (str): The date format for the asctime part of the timestamp.
	"""
	listener = get_global_listener()
	if not listener:
		logging.warning("Cannot toggle timestamps: Global QueueListener not found.")
		return

	for handler in listener.handlers:
		if not hasattr(handler, "formatter") or not isinstance(handler.formatter, DelegatingFormatter):
			continue

		delegating_formatter = handler.formatter
		current_delegate = delegating_formatter.delegate

		is_timestamped = hasattr(current_delegate, "_original_fmt")

		if enable and not is_timestamped:
			# --- ADD TIMESTAMPS ---
			original_fmt = current_delegate._style._fmt
			original_datefmt = current_delegate.datefmt
			
			new_fmt = f"%(asctime)s.%(msecs)03d | {original_fmt}"

			new_delegate = type(current_delegate)(fmt=new_fmt, datefmt=date_format)
			new_delegate._original_fmt = original_fmt
			new_delegate._original_datefmt = original_datefmt
			
			delegating_formatter.set_delegate(new_delegate)
		elif not enable and is_timestamped:
			# --- REMOVE TIMESTAMPS ---
			original_fmt = current_delegate._original_fmt
			original_datefmt = current_delegate._original_datefmt

			restored_delegate = type(current_delegate)(fmt=original_fmt, datefmt=original_datefmt)
			
			delegating_formatter.set_delegate(restored_delegate)


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
		stdout_handler.setFormatter(DelegatingFormatter(colored_formatter))
		stdout_handler.set_name(log_name)
		handlers.append(stdout_handler)

	file_handler: LogBackupFileHandler | None = None
	if log_to_file:
		log_path = f'{os.path.join(root_dir, log_name)}.log'
		file_handler = LogBackupFileHandler(log_path, mode="w", backupCount=backup_count, delay=True, encoding="utf-8")
		file_handler.setLevel(logging.DEBUG) # always write all levels to file log
		file_handler.setFormatter(DelegatingFormatter(formatter))
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
