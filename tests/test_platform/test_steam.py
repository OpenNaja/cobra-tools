"""Tests for gui.app_utils.get_steam_path covering each platform branch.

Imports gui.app_utils, which transitively imports PyQt5 — fine because the project's
dev install (`pip install .[gui,dev]`) provides it on every CI runner.
"""

import os
from unittest.mock import patch

import pytest

from utils.shared import IS_WINDOWS


@pytest.fixture(scope="module")
def app_utils():
	"""Import gui.app_utils once so each test patches the same module object."""
	from gui import app_utils as module
	return module


@pytest.mark.skipif(IS_WINDOWS, reason="Verifies the non-Windows native branch on the actual host.")
def test_get_steam_path_native_posix_is_well_formed(app_utils):
	"""On real Linux/macOS Python, the returned path must be POSIX-shaped (no backslashes,
	`~` expanded, ends with 'Steam')."""
	path = app_utils.get_steam_path()
	assert path is not None
	assert "\\" not in path, f"unexpected Windows backslashes: {path!r}"
	assert not path.startswith("~"), f"`~` must be expanded: {path!r}"
	assert path.rstrip(os.sep).endswith("Steam"), f"path should end with 'Steam': {path!r}"


@pytest.mark.skipif(IS_WINDOWS, reason="os.path.expanduser is platform-aware; this branch only produces POSIX-shaped output on a non-Windows host.")
def test_get_steam_path_linux_branch(app_utils):
	"""IS_LINUX=True returns a Steam path under the user's home, no Windows separators."""
	with patch.object(app_utils, "IS_WINDOWS", False), \
		patch.object(app_utils, "IS_LINUX", True), \
		patch.object(app_utils, "IS_MACOS", False):
		path = app_utils.get_steam_path()
	assert path is not None
	assert "\\" not in path
	assert "Steam" in path
	assert path.startswith(os.path.expanduser("~"))


@pytest.mark.skipif(IS_WINDOWS, reason="os.path.expanduser is platform-aware; this branch only produces POSIX-shaped output on a non-Windows host.")
def test_get_steam_path_macos_branch(app_utils):
	"""IS_MACOS=True returns the conventional macOS Application Support path."""
	with patch.object(app_utils, "IS_WINDOWS", False), \
		patch.object(app_utils, "IS_LINUX", False), \
		patch.object(app_utils, "IS_MACOS", True):
		path = app_utils.get_steam_path()
	assert path is not None
	assert "\\" not in path
	assert not path.startswith("~")
	assert "Library/Application Support/Steam" in path


def test_get_steam_path_unsupported_platform_returns_none(app_utils):
	"""When no platform flag is set (e.g. an unsupported OS), get_steam_path returns None."""
	with patch.object(app_utils, "IS_WINDOWS", False), \
		patch.object(app_utils, "IS_LINUX", False), \
		patch.object(app_utils, "IS_MACOS", False):
		assert app_utils.get_steam_path() is None
