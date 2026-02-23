import os
import subprocess

from gui.app_utils import WINDOWS_WINE

util_dir = os.path.dirname(__file__)


def check_call_smart(args: list[str]):
	if WINDOWS_WINE:
		args = ["wine", ] + args
	subprocess.check_call(args)


def prep_arg(arg: str):
	if WINDOWS_WINE:
		return "wine " + arg
	return arg
