import os
import subprocess

from gui.app_utils import WINDOWS_WINE

util_dir = os.path.dirname(__file__)


def check_call_smart(args):
	if WINDOWS_WINE:
		args = ["wine", ] + args
	subprocess.check_call(args)
