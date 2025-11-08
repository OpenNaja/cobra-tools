from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any, Generator

import pytest
from pytest import LogCaptureFixture, MonkeyPatch, FixtureRequest
from pytestqt.plugin import QtBot

from tests.test_gui.fixtures.apps import *

if TYPE_CHECKING:
	from PyQt5.QtWidgets import QApplication
	from gui.widgets.window import MainWindow
	QtAppFixture = tuple[QApplication, 'MainWindow', QtBot]
	QtAppFixtureGenerator = Generator[tuple[QApplication, 'MainWindow', QtBot], Any, None]


@pytest.fixture(autouse=True)
def no_call_logs_gte_error(caplog: LogCaptureFixture):
	"""Fail test if logging.ERROR or higher during call phase"""
	yield
	errors = [record for record in caplog.get_records("call") if record.levelno >= logging.ERROR]
	assert not errors


@pytest.fixture
def no_prompts(caplog: LogCaptureFixture):
	"""Fail test if User Prompt occurs"""
	yield
	prompts = [record for record in caplog.get_records('call') if "User Prompt:" in record.message]
	assert not prompts


# Disable for now
#@pytest.fixture(autouse=True)
#def logs_closed(caplog: LogCaptureFixture):
#	"""Fail test if logs are not reported as closed"""
#	yield
#	closed = [record for record in caplog.get_records('call') if "Closing Log:" in record.message]
#	assert closed


@pytest.fixture()
def log_succeeds(caplog: LogCaptureFixture):
	yield caplog
	successes = [record for record in caplog.get_records("call") if record.levelno == logging.SUCCESS]
	assert successes

def test_ovl_tool_new(
	OVLTool: QtAppFixture,
	log_succeeds: LogCaptureFixture
):
	app, window, qtbot = OVLTool
	
	window.file_widget.set_file_path("tests/Files/Files.ovl")
	window.file_widget.dir_opened.emit("tests/Files/")

	qtbot.waitUntil(lambda: "adding succeeded" in window.status_bar.currentMessage().lower(), timeout=10000)

	assert window.file_widget.filepath == "tests/Files/Files.ovl"
	assert "Files.ovl" in window.windowTitle()
	assert "adding succeeded" in log_succeeds.text.lower()

def test_run_ovl_tool(OVLTool: QtAppFixture, no_prompts):
	app, window, qtbot = OVLTool
	assert "OVL" in window.windowTitle()


def test_run_fgm_editor(FGMEditor: QtAppFixture, no_prompts):
	app, window, qtbot = FGMEditor
	assert "FGM" in window.windowTitle()


def test_run_ms2_tool(MS2Tool: QtAppFixture, no_prompts):
	app, window, qtbot = MS2Tool
	assert "MS2" in window.windowTitle()


def test_run_matcol_editor(MatcolEditor: QtAppFixture, no_prompts):
	app, window, qtbot = MatcolEditor
	assert "Matcol" in window.windowTitle()


def test_run_bnk_gui(BNKGui: QtAppFixture, no_prompts):
	app, window, qtbot = BNKGui
	assert "BNK" in window.windowTitle()

