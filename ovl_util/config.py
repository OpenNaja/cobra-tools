import json
import logging
import sys
import os
import platform

from root_path import root_dir


def save_config(cfg_dict):
	logging.info(f"Saving config")
	with open(os.path.join(root_dir, "config.json"), "w") as json_writer:
		json.dump(cfg_dict, json_writer, indent="\t", sort_keys=True)


def load_config():
	try:
		with open(os.path.join(root_dir, "config.json"), "r") as json_reader:
			return json.load(json_reader)
	except FileNotFoundError:
		logging.exception(f"Config file missing")
		return {}
	except json.decoder.JSONDecodeError:
		logging.exception(f"Config file broken")
		return {}


def read_str_dict(cfg_path):
	config_dict = {}
	try:
		with open(cfg_path, 'r', encoding='utf-8') as cfg_file:
			for line in cfg_file:
				if not line.startswith("#") and "=" in line:
					(key, val) = line.strip().split("=")
					key = key.strip()
					val = val.strip()
					if val.startswith("["):
						# strip list format [' ... ']
						val = val[2:-2]
						config_dict[key] = [v.strip() for v in val.split("', '")]
					else:
						config_dict[key] = val
	except:
		print(f"{cfg_path} is missing or broken!")
	return config_dict


def write_str_dict(cfg_path, config_dict):
	stream = "\n".join([key+"="+str(val) for key, val in config_dict.items()])
	with open(cfg_path, 'w', encoding='utf8') as cfg_file:
		cfg_file.write(stream)


def read_list(cfg_path):
	try:
		with open(cfg_path, 'r', encoding='utf-8') as cfg_file:
			return [line.strip() for line in cfg_file if line.strip() and not line.startswith("#")]
	except:
		print(f"{cfg_path} is missing or broken!")
		return []


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

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.FORMATS = {
			logging.DEBUG: f"{ANSI.DARK_GRAY}{self._fmt}{ANSI.END}",
			logging.INFO: f"{ANSI.LIGHT_WHITE}{self._fmt}{ANSI.END}",
			logging.INFO + 5: f"{ANSI.LIGHT_GREEN}{self._fmt}{ANSI.END}", # SUCCESS
			logging.WARNING: f"{ANSI.YELLOW}{self._fmt}{ANSI.END}",
			logging.ERROR: f"{ANSI.RED}{self._fmt}{ANSI.END}",
			logging.CRITICAL: f"{ANSI.LIGHT_RED}{self._fmt}{ANSI.END}"
		}
		self.FORMATTERS = {key: logging.Formatter(fmt) for key, fmt in self.FORMATS.items()}

	def format(self, record):
		formatter = self.FORMATTERS.get(record.levelno)
		return formatter.format(record)


def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present 

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
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def logging_setup(log_name):
	log_path = f'{os.path.join(root_dir, log_name)}.log'
	addLoggingLevel('SUCCESS', logging.INFO + 5)
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	# formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
	formatter = logging.Formatter('%(levelname)s | %(message)s')
	# Colored logging for all platforms but Windows 7/8
	colored_formatter = ColoredFormatter('%(levelname)s | %(message)s')

	stdout_handler = logging.StreamHandler(sys.stdout)
	stdout_handler.setLevel(logging.INFO)
	stdout_handler.setFormatter(colored_formatter)
	# always write all levels to debug log
	file_handler = logging.FileHandler(log_path, mode="w")
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	logger.addHandler(stdout_handler)
	return stdout_handler


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


if __name__ == '__main__':
	cfg = read_str_dict("config.ini")
	print(cfg)
