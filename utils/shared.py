import os
import platform
import shutil
import subprocess


_SYSTEM = platform.system()

IS_WINDOWS = _SYSTEM == "Windows"
IS_LINUX = _SYSTEM == "Linux"
IS_MACOS = _SYSTEM == "Darwin"

# A Wine-Python interpreter (Python installed inside a Wine prefix) reports
# platform.system() == "Windows" but interacts with a Wine-managed filesystem.
WINDOWS_WINE = IS_WINDOWS and "WINEPREFIX" in os.environ
WINDOWS_NATIVE = IS_WINDOWS and not WINDOWS_WINE

# True when the current shell can invoke `wine` to run Windows .exe targets.
# Always False on Windows-Python (native or Wine-Python).
WINE_AVAILABLE = (not IS_WINDOWS) and shutil.which("wine") is not None


class BinaryNotAvailableError(RuntimeError):
	"""Raised when a vendored or system binary cannot be located on the current platform."""

	def __init__(self, name: str, reason: str = ""):
		self.name = name
		self.reason = reason
		msg = f"Required binary {name!r} is not available on this platform"
		if reason:
			msg += f": {reason}"
		super().__init__(msg)


def check_any(iterable, string):
	"""Returns true if any of the entries of the iterable occur in string"""
	return any(i in string for i in iterable)


def _is_windows_exe(path: str) -> bool:
	return isinstance(path, str) and path.lower().endswith(".exe")


def _first_token(arg: str) -> str:
	"""Return the first whitespace-separated token of ``arg``, with surrounding quotes stripped."""
	stripped = arg.strip()
	if not stripped:
		return ""
	if stripped[0] in ('"', "'"):
		quote = stripped[0]
		end = stripped.find(quote, 1)
		return stripped[1:end] if end != -1 else stripped[1:]
	return stripped.split(None, 1)[0]


def check_call_smart(args: list[str]):
	"""subprocess.check_call wrapper that prefixes ``wine`` when invoking a Windows .exe
	from a Wine-Python or non-Windows Python. Raises BinaryNotAvailableError on non-Windows
	when the .exe target can't be reached (no wine on PATH)."""
	if not args:
		raise ValueError("check_call_smart requires at least one argument")
	if WINDOWS_WINE:
		args = ["wine", *args]
	elif (not IS_WINDOWS) and _is_windows_exe(args[0]):
		if not WINE_AVAILABLE:
			raise BinaryNotAvailableError(
				args[0],
				"Windows .exe targets need either a Windows host or `wine` on PATH",
			)
		args = ["wine", *args]
	subprocess.check_call(args)


def prep_arg(arg: str):
	"""Prefix ``arg`` (a single shell-style command string) with ``wine `` when invoking a
	Windows .exe from a Wine-Python or non-Windows Python. Mirrors check_call_smart for
	callers that pass commands to subprocess.Popen as a single string."""
	if WINDOWS_WINE:
		return "wine " + arg
	if not IS_WINDOWS and _is_windows_exe(_first_token(arg)):
		if not WINE_AVAILABLE:
			raise BinaryNotAvailableError(
				_first_token(arg),
				"Windows .exe targets need either a Windows host or `wine` on PATH",
			)
		return "wine " + arg
	return arg
