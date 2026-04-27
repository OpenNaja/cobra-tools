import os
import platform
import subprocess


def check_any(iterable, string):
	"""Returns true if any of the entries of the iterable occur in string"""
	return any([i in string for i in iterable])


def check_call_smart(args: list[str]):
	if WINDOWS_WINE:
		args = ["wine", ] + args
	subprocess.check_call(args)


def prep_arg(arg: str):
	if WINDOWS_WINE:
		return "wine " + arg
	return arg


WINDOWS_NATIVE = platform.system() == "Windows" and 'WINEPREFIX' not in os.environ
WINDOWS_WINE = platform.system() == "Windows" and 'WINEPREFIX' in os.environ
