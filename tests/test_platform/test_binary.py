"""Smoke tests for the .exe-aware subprocess helpers in utils.shared.

Verifies that on non-Windows Python without `wine`, attempting to run a Windows .exe
fails with a clear BinaryNotAvailableError instead of a confusing FileNotFoundError.
"""

from unittest.mock import patch

import pytest

from utils.shared import (
	BinaryNotAvailableError,
	IS_WINDOWS,
	check_call_smart,
	prep_arg,
)


@pytest.mark.skipif(IS_WINDOWS, reason="Behavior under test is the non-Windows fallback path.")
def test_check_call_smart_raises_when_wine_missing():
	"""On non-Windows Python with no `wine` on PATH, invoking an .exe must raise
	BinaryNotAvailableError immediately, not attempt subprocess.check_call."""
	with patch("utils.shared.WINE_AVAILABLE", False):
		with pytest.raises(BinaryNotAvailableError) as exc_info:
			check_call_smart(["/nonexistent/path/texconv.exe", "--help"])
	assert exc_info.value.name.endswith("texconv.exe")


@pytest.mark.skipif(IS_WINDOWS, reason="Behavior under test is the non-Windows fallback path.")
def test_prep_arg_raises_when_wine_missing_for_exe():
	"""prep_arg must raise BinaryNotAvailableError when handed an .exe command on
	non-Windows Python without `wine` available."""
	with patch("utils.shared.WINE_AVAILABLE", False):
		with pytest.raises(BinaryNotAvailableError):
			prep_arg('"/nonexistent/path/luadec.exe" "input.bin"')


@pytest.mark.skipif(IS_WINDOWS, reason="Behavior under test is the non-Windows fallback path.")
def test_prep_arg_passthrough_for_non_exe():
	"""Non-.exe commands must pass through unchanged on non-Windows."""
	cmd = "/usr/bin/echo hello"
	assert prep_arg(cmd) == cmd


@pytest.mark.skipif(IS_WINDOWS, reason="Behavior under test is the non-Windows fallback path.")
def test_prep_arg_prefixes_wine_when_available():
	"""When wine is on PATH, prep_arg must prefix the command with 'wine '."""
	with patch("utils.shared.WINE_AVAILABLE", True):
		assert prep_arg('"/path/to/texconv.exe" -h').startswith("wine ")


def test_binary_not_available_error_message():
	err = BinaryNotAvailableError("texconv", "no PATH entry")
	assert "texconv" in str(err)
	assert "no PATH entry" in str(err)
	assert err.name == "texconv"
	assert err.reason == "no PATH entry"
