"""Tests for the binary registry / resolver / decorator in utils.shared.

Covers:
  * resolve_binary lookup order (PATH → vendored fallback → None).
  * argv_for_binary: raises BinaryNotAvailableError when unreachable; prefixes ``wine``
	when running a Windows .exe from a non-Windows or Wine-Python interpreter.
  * run_binary delegates to subprocess.run with the resolved argv.
  * @requires_binary fails fast at the function-entry boundary.
"""

from unittest.mock import MagicMock, patch

import pytest

from utils import shared
from utils.shared import (
	BinaryNotAvailableError,
	argv_for_binary,
	invocation_for_binary,
	register_binary,
	requires_binary,
	resolve_binary,
	run_binary,
	winepath,
)


@pytest.fixture(autouse=True)
def isolate_registry(monkeypatch):
	"""Each test gets a fresh _VENDORED_BINARIES dict so registrations don't leak."""
	monkeypatch.setattr(shared, "_VENDORED_BINARIES", {})
	yield


def test_resolve_binary_returns_path_when_on_path():
	"""shutil.which hit must short-circuit before consulting the vendored registry."""
	with patch("utils.shared.shutil.which", return_value="/usr/local/bin/texconv"):
		assert resolve_binary("texconv") == "/usr/local/bin/texconv"


def test_resolve_binary_returns_none_when_unregistered_and_not_on_path():
	"""No PATH entry, no registered fallback → None (caller decides what to do)."""
	with patch("utils.shared.shutil.which", return_value=None):
		assert resolve_binary("nonexistent_xyz") is None


def test_resolve_binary_falls_back_to_vendored_on_windows(tmp_path):
	"""On Windows, the vendored fallback is returned regardless of WINE_AVAILABLE."""
	fake_exe = tmp_path / "texconv.exe"
	fake_exe.write_bytes(b"")
	register_binary("texconv", str(fake_exe))
	with patch("utils.shared.shutil.which", return_value=None), \
		patch.object(shared, "IS_WINDOWS", True):
		assert resolve_binary("texconv") == str(fake_exe)


def test_resolve_binary_falls_back_to_vendored_on_unix_with_wine(tmp_path):
	"""On non-Windows with wine, the vendored .exe is reachable through wine."""
	fake_exe = tmp_path / "texconv.exe"
	fake_exe.write_bytes(b"")
	register_binary("texconv", str(fake_exe))
	with patch("utils.shared.shutil.which", return_value=None), \
		patch.object(shared, "IS_WINDOWS", False), \
		patch.object(shared, "WINE_AVAILABLE", True):
		assert resolve_binary("texconv") == str(fake_exe)


def test_resolve_binary_no_fallback_on_unix_without_wine(tmp_path):
	"""On non-Windows without wine, the vendored .exe is unreachable; resolver returns None."""
	fake_exe = tmp_path / "texconv.exe"
	fake_exe.write_bytes(b"")
	register_binary("texconv", str(fake_exe))
	with patch("utils.shared.shutil.which", return_value=None), \
		patch.object(shared, "IS_WINDOWS", False), \
		patch.object(shared, "WINE_AVAILABLE", False):
		assert resolve_binary("texconv") is None


def test_argv_for_binary_raises_when_unreachable():
	with patch("utils.shared.shutil.which", return_value=None), \
		patch.object(shared, "IS_WINDOWS", False), \
		patch.object(shared, "WINE_AVAILABLE", False):
		with pytest.raises(BinaryNotAvailableError) as exc_info:
			argv_for_binary("texconv")
	assert exc_info.value.name == "texconv"


def test_argv_for_binary_native_returns_single_path():
	"""Native PATH binary returns ``[resolved]`` with no wine prefix."""
	with patch("utils.shared.shutil.which", return_value="/usr/local/bin/texconv"):
		assert argv_for_binary("texconv") == ["/usr/local/bin/texconv"]


def test_argv_for_binary_wraps_exe_with_wine_on_unix(tmp_path):
	"""Vendored .exe on non-Windows is wrapped with ``wine``."""
	fake_exe = tmp_path / "texconv.exe"
	fake_exe.write_bytes(b"")
	register_binary("texconv", str(fake_exe))
	with patch("utils.shared.shutil.which", return_value=None), \
		patch.object(shared, "IS_WINDOWS", False), \
		patch.object(shared, "WINE_AVAILABLE", True):
		assert argv_for_binary("texconv") == ["wine", str(fake_exe)]


def test_argv_for_binary_wraps_with_wine_on_windows_wine(tmp_path):
	"""On Wine-Python (WINDOWS_WINE), even a Windows-resolved binary is invoked through wine."""
	fake_exe = tmp_path / "texconv.exe"
	fake_exe.write_bytes(b"")
	register_binary("texconv", str(fake_exe))
	with patch("utils.shared.shutil.which", return_value=None), \
		patch.object(shared, "IS_WINDOWS", True), \
		patch.object(shared, "WINDOWS_WINE", True):
		assert argv_for_binary("texconv") == ["wine", str(fake_exe)]


def test_run_binary_delegates_to_subprocess_run():
	"""run_binary invokes subprocess.run with the argv prefix + supplied args, defaulting to check=True."""
	completed = MagicMock()
	with patch("utils.shared.shutil.which", return_value="/usr/bin/echo"), \
		patch("utils.shared.subprocess.run", return_value=completed) as mock_run:
		result = run_binary("echo", ["hello", "world"])
	mock_run.assert_called_once_with(["/usr/bin/echo", "hello", "world"], check=True)
	assert result is completed


def test_run_binary_caller_can_override_check():
	"""Passing check=False suppresses the default."""
	with patch("utils.shared.shutil.which", return_value="/usr/bin/echo"), \
		patch("utils.shared.subprocess.run") as mock_run:
		run_binary("echo", [], check=False)
	mock_run.assert_called_once_with(["/usr/bin/echo"], check=False)


def test_run_binary_propagates_binary_not_available():
	with patch("utils.shared.shutil.which", return_value=None), \
		patch.object(shared, "IS_WINDOWS", False), \
		patch.object(shared, "WINE_AVAILABLE", False), \
		patch("utils.shared.subprocess.run") as mock_run:
		with pytest.raises(BinaryNotAvailableError):
			run_binary("nonexistent", [])
	mock_run.assert_not_called()


def test_requires_binary_decorator_blocks_when_unreachable():
	"""When the binary is missing, the decorator raises before the function body runs."""
	body_ran = []

	@requires_binary("nonexistent_xyz")
	def fn():
		body_ran.append(True)
		return "should not reach"

	with patch("utils.shared.shutil.which", return_value=None), \
		patch.object(shared, "IS_WINDOWS", False), \
		patch.object(shared, "WINE_AVAILABLE", False):
		with pytest.raises(BinaryNotAvailableError):
			fn()
	assert body_ran == []


def test_requires_binary_decorator_passes_when_available():
	"""When the binary is available, the wrapped function is invoked normally."""
	@requires_binary("texconv")
	def fn(x):
		return x * 2

	with patch("utils.shared.shutil.which", return_value="/usr/local/bin/texconv"):
		assert fn(7) == 14


def test_requires_binary_preserves_function_metadata():
	"""functools.wraps must propagate __name__ and __doc__."""
	@requires_binary("texconv")
	def my_function():
		"""docstring"""

	assert my_function.__name__ == "my_function"
	assert my_function.__doc__ == "docstring"


def test_binary_not_available_error_message():
	err = BinaryNotAvailableError("texconv", "no PATH entry")
	assert "texconv" in str(err)
	assert "no PATH entry" in str(err)
	assert err.name == "texconv"
	assert err.reason == "no PATH entry"


# --- wine path translation -------------------------------------------------- #


def test_winepath_translates_posix_absolute_on_unix():
	"""POSIX-absolute paths get the Z: drive prefix and backslash separators on non-Windows."""
	with patch.object(shared, "IS_WINDOWS", False):
		assert winepath("/home/user/foo.dds") == r"Z:\home\user\foo.dds"
		assert winepath("/tmp/out") == r"Z:\tmp\out"


def test_winepath_no_op_on_windows():
	"""On Windows-Python (native or Wine), winepath returns its input unchanged so we don't
	clobber drive-letter paths that Wine-Python sees natively."""
	with patch.object(shared, "IS_WINDOWS", True):
		assert winepath("/home/user/foo.dds") == "/home/user/foo.dds"
		assert winepath(r"C:\Users\foo") == r"C:\Users\foo"


def test_winepath_no_op_for_relative_paths_and_flags():
	"""Non-POSIX-absolute strings (relative paths, flags, plain values) pass through verbatim."""
	with patch.object(shared, "IS_WINDOWS", False):
		assert winepath("-y") == "-y"
		assert winepath("relative/path") == "relative/path"
		assert winepath("png") == "png"
		assert winepath("") == ""


# --- invocation_for_binary -------------------------------------------------- #


def test_invocation_for_binary_native_returns_identity_translator():
	"""Native PATH binary: translator is identity; argv has no wine prefix."""
	with patch("utils.shared.shutil.which", return_value="/usr/local/bin/luadec"):
		argv, translator = invocation_for_binary("luadec")
	assert argv == ["/usr/local/bin/luadec"]
	assert translator("/some/path") == "/some/path"


def test_invocation_for_binary_wine_returns_winepath_translator(tmp_path):
	"""Wine invocation: translator is winepath; argv is wine-prefixed."""
	fake_exe = tmp_path / "luadec.exe"
	fake_exe.write_bytes(b"")
	register_binary("luadec", str(fake_exe))
	# Translator must be invoked while IS_WINDOWS is mocked False; otherwise on a Windows
	# host winepath sees the real IS_WINDOWS=True and returns the input unchanged.
	with patch("utils.shared.shutil.which", return_value=None), \
		patch.object(shared, "IS_WINDOWS", False), \
		patch.object(shared, "WINE_AVAILABLE", True):
		argv, translator = invocation_for_binary("luadec")
		assert argv == ["wine", str(fake_exe)]
		assert translator("/home/user/foo.bin") == r"Z:\home\user\foo.bin"


# --- run_binary auto-translation -------------------------------------------- #


def test_run_binary_translates_posix_path_args_under_wine(tmp_path):
	"""When invoking via wine, POSIX-absolute path args are converted to Z: drive form."""
	fake_exe = tmp_path / "texconv.exe"
	fake_exe.write_bytes(b"")
	register_binary("texconv", str(fake_exe))
	with patch("utils.shared.shutil.which", return_value=None), \
		patch.object(shared, "IS_WINDOWS", False), \
		patch.object(shared, "WINE_AVAILABLE", True), \
		patch("utils.shared.subprocess.run") as mock_run:
		run_binary("texconv", ["-y", "-o", "/tmp/out", "/home/user/in.dds"])
	mock_run.assert_called_once_with(
		["wine", str(fake_exe), "-y", "-o", r"Z:\tmp\out", r"Z:\home\user\in.dds"],
		check=True,
	)


def test_run_binary_does_not_translate_native_invocation():
	"""Native PATH binary: POSIX paths passed through unchanged (native binary speaks POSIX)."""
	with patch("utils.shared.shutil.which", return_value="/usr/local/bin/texconv"), \
		patch("utils.shared.subprocess.run") as mock_run:
		run_binary("texconv", ["-o", "/tmp/out", "/home/user/in.dds"])
	mock_run.assert_called_once_with(
		["/usr/local/bin/texconv", "-o", "/tmp/out", "/home/user/in.dds"],
		check=True,
	)
