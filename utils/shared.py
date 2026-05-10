from __future__ import annotations

import functools
import os
import platform
import shutil
import subprocess
from typing import Callable


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


# --- Vendored-binary registry & PATH-aware resolver ---

_VENDORED_BINARIES: dict[str, str] = {}


def register_binary(name: str, vendored_path: str) -> None:
	"""Register a vendored binary path used as a fallback when ``name`` is not on PATH.

	Each conversion module calls this at import time, e.g.:

		register_binary("texconv", os.path.join(util_dir, "texconv/texconv.exe"))
	"""
	_VENDORED_BINARIES[name] = vendored_path


def resolve_binary(name: str) -> str | None:
	"""Resolve ``name`` to a runnable absolute path, or None if unreachable.

	Lookup order:
	  1. ``shutil.which(name)`` — Linux/macOS native install or Windows-on-PATH.
	  2. ``shutil.which(name + ".exe")`` — defensive on Windows where PATHEXT usually handles it.
	  3. The vendored fallback registered via :func:`register_binary`. Only returned on
	     Windows or when ``WINE_AVAILABLE`` is True (so wine can run the .exe).
	"""
	on_path = shutil.which(name)
	if on_path:
		return on_path
	if IS_WINDOWS:
		on_path_exe = shutil.which(f"{name}.exe")
		if on_path_exe:
			return on_path_exe
	fallback = _VENDORED_BINARIES.get(name)
	if fallback and os.path.isfile(fallback):
		if IS_WINDOWS or WINE_AVAILABLE:
			return fallback
	return None


def _missing_reason(name: str) -> str:
	if IS_WINDOWS:
		return f"{name!r} not on PATH and no vendored fallback found"
	if WINE_AVAILABLE:
		return f"{name!r} not on PATH and no vendored fallback found"
	return f"{name!r} not on PATH and `wine` is unavailable to run the vendored .exe"


def winepath(path: str) -> str:
	"""Translate a POSIX absolute path to the wine ``Z:`` drive form.

	``/home/user/foo.dds`` becomes ``Z:\\home\\user\\foo.dds`` so that a Windows .exe
	invoked through wine can resolve the file. No-op on Windows-Python (native or Wine-
	Python) and for paths that aren't POSIX-absolute (relative paths, flags, drive-letter
	paths).

	Use this only when invoking a Windows binary through wine — native Linux/macOS
	binaries take POSIX paths unchanged. :func:`run_binary` and
	:func:`invocation_for_binary` apply it automatically when needed.
	"""
	if IS_WINDOWS or not path.startswith("/"):
		return path
	return "Z:" + path.replace("/", "\\")


def _identity_path(path: str) -> str:
	return path


def argv_for_binary(name: str) -> list[str]:
	"""Return the argv prefix for invoking ``name`` via subprocess.

	Use as: ``cmd = [*argv_for_binary("texconv"), "-y", "-ft", "png", ...]``.

	Raises :class:`BinaryNotAvailableError` if no source is reachable. When the resolved
	path is a Windows .exe and we're on a non-Windows or Wine-Python interpreter, the
	returned list is prefixed with ``"wine"``.
	"""
	resolved = resolve_binary(name)
	if resolved is None:
		raise BinaryNotAvailableError(name, _missing_reason(name))
	if WINDOWS_WINE or ((not IS_WINDOWS) and _is_windows_exe(resolved)):
		return ["wine", resolved]
	return [resolved]


def invocation_for_binary(name: str) -> tuple[list[str], Callable[[str], str]]:
	"""Return ``(argv_prefix, path_translator)`` for invoking ``name``.

	The path translator must be applied to every path-style argument before constructing
	the final command. When the invocation is going through wine, ``path_translator`` is
	:func:`winepath`; otherwise it's the identity function.

	Use this for callers that bypass :func:`run_binary` (e.g. ``subprocess.Popen`` for
	stdout streaming or output parsing) and need the same translation contract.
	"""
	argv = argv_for_binary(name)
	if argv[0] == "wine":
		return argv, winepath
	return argv, _identity_path


def run_binary(name: str, args: list[str], **kwargs) -> "subprocess.CompletedProcess":
	"""subprocess.run wrapper that resolves ``name`` and invokes it with ``args``.

	Defaults to ``check=True`` (raises CalledProcessError on non-zero exit). Pass
	``capture_output=True`` to capture stdout/stderr, ``timeout=N`` for a deadline, etc.
	Raises :class:`BinaryNotAvailableError` before invocation if ``name`` cannot be resolved.

	When invoking via wine, POSIX-absolute path arguments in ``args`` are auto-translated
	to wine ``Z:`` drive form (see :func:`winepath`); other arguments pass through verbatim.
	"""
	argv, to_argpath = invocation_for_binary(name)
	translated_args = [to_argpath(a) if isinstance(a, str) else a for a in args]
	cmd = [*argv, *translated_args]
	return subprocess.run(cmd, **{"check": True, **kwargs})


def requires_binary(name: str):
	"""Decorator: validates that ``name`` is reachable before invoking the wrapped function.

	Pairs with :func:`register_binary` at module load. On miss, fails at the function-entry
	boundary with :class:`BinaryNotAvailableError` so callers learn early which feature is
	missing instead of debugging a mid-subprocess error.
	"""
	def deco(fn):
		@functools.wraps(fn)
		def wrapper(*args, **kw):
			if resolve_binary(name) is None:
				raise BinaryNotAvailableError(name, _missing_reason(name))
			return fn(*args, **kw)
		return wrapper
	return deco
