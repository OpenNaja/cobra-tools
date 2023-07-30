import logging

import pytest
from pytest import LogCaptureFixture
from pytestqt.plugin import QtBot

from PyQt5.QtWidgets import QApplication

from ovl_util import widgets


QtAppFixture = tuple[QApplication, widgets.MainWindow, QtBot]


@pytest.fixture(autouse=True)
def no_logs_gte_error(caplog: LogCaptureFixture):
	"""Fail test if logging.ERROR or higher"""
	yield
	errors = [record for record in caplog.get_records("call") if record.levelno >= logging.ERROR]
	assert not errors


@pytest.fixture()
def log_succeeds(caplog: LogCaptureFixture):
	yield caplog
	successes = [record for record in caplog.get_records("call") if record.levelno == logging.SUCCESS]
	assert successes


@pytest.fixture(scope="function")
def OVLTool(qapp: QApplication, qtbot: QtBot, caplog: LogCaptureFixture) -> QtAppFixture:
	from ovl_tool_gui import MainWindow
	window = MainWindow()
	qtbot.addWidget(window)
	qtbot.waitUntil(lambda: "loading constants took" in caplog.text.lower(), timeout=25000)
	return qapp, window, qtbot


@pytest.fixture(scope="function")
def FGMEditor(qapp: QApplication, qtbot: QtBot) -> QtAppFixture:
	from fgm_editor_gui import MainWindow
	window = MainWindow()
	qtbot.addWidget(window)
	return qapp, window, qtbot


@pytest.fixture(scope="function")
def MS2Tool(qapp: QApplication, qtbot: QtBot) -> QtAppFixture:
	from ms2_tool_gui import MainWindow
	window = MainWindow()
	qtbot.addWidget(window)
	return qapp, window, qtbot


@pytest.fixture(scope="function")
def MatcolEditor(qapp: QApplication, qtbot: QtBot) -> QtAppFixture:
	from matcol_editor_gui import MainWindow
	window = MainWindow()
	qtbot.addWidget(window)
	return qapp, window, qtbot


@pytest.fixture(scope="function")
def BNKGui(qapp: QApplication, qtbot: QtBot) -> QtAppFixture:
	from bnk_gui import MainWindow
	window = MainWindow()
	qtbot.addWidget(window)
	return qapp, window, qtbot


def test_run_ovl_tool(OVLTool: QtAppFixture):
	app, window, _ = OVLTool
	assert "OVL" in window.windowTitle()
	app.quit()


def test_run_fgm_editor(FGMEditor: QtAppFixture):
	app, window, _ = FGMEditor
	assert "FGM" in window.windowTitle()
	app.quit()


def test_run_ms2_tool(MS2Tool: QtAppFixture):
	app, window, _ = MS2Tool
	assert "MS2" in window.windowTitle()
	app.quit()


def test_run_matcol_editor(MatcolEditor: QtAppFixture):
	app, window, _ = MatcolEditor
	assert "Matcol" in window.windowTitle()
	app.quit()


def test_run_bnk_gui(BNKGui: QtAppFixture):
	app, window, _ = BNKGui
	assert "BNK" in window.windowTitle()
	app.quit()


def test_ovl_tool_new(OVLTool: QtAppFixture, log_succeeds: LogCaptureFixture):
	app, window, qtbot = OVLTool
	
	window.file_widget.set_file_path("tests/Files/Files.ovl")
	window.file_widget.dir_opened.emit("tests/Files/")
	qtbot.waitUntil(lambda: "finished adding" in window.statusBar.currentMessage().lower(), timeout=10000)

	assert window.file_widget.filepath == "tests/Files/Files.ovl"
	assert "Files.ovl" in window.windowTitle()
	assert "adding succeeded" in log_succeeds.text.lower()

	app.quit()
