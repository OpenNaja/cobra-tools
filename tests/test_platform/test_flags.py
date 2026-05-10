"""Cross-platform sanity checks on the IS_WINDOWS / IS_LINUX / IS_MACOS / WINE_AVAILABLE flags."""

import platform
import shutil

from utils.shared import (
	IS_LINUX,
	IS_MACOS,
	IS_WINDOWS,
	WINDOWS_NATIVE,
	WINDOWS_WINE,
	WINE_AVAILABLE,
)


def test_one_os_flag_is_set():
	"""Exactly one of IS_WINDOWS / IS_LINUX / IS_MACOS must be True on a supported platform."""
	assert sum([IS_WINDOWS, IS_LINUX, IS_MACOS]) == 1


def test_os_flag_matches_platform_system():
	system = platform.system()
	if system == "Windows":
		assert IS_WINDOWS
	elif system == "Linux":
		assert IS_LINUX
	elif system == "Darwin":
		assert IS_MACOS


def test_windows_native_and_wine_are_mutually_exclusive():
	"""WINDOWS_NATIVE and WINDOWS_WINE partition the IS_WINDOWS=True case; both False otherwise."""
	assert not (WINDOWS_NATIVE and WINDOWS_WINE)
	if not IS_WINDOWS:
		assert not WINDOWS_NATIVE
		assert not WINDOWS_WINE


def test_wine_available_is_non_windows_only():
	"""WINE_AVAILABLE is meaningful only off Windows-Python; it must be False on Windows."""
	if IS_WINDOWS:
		assert WINE_AVAILABLE is False
	else:
		assert WINE_AVAILABLE == (shutil.which("wine") is not None)
