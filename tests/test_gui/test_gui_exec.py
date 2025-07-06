import logging
from typing import Any, Generator

import pytest
from pytest import LogCaptureFixture, MonkeyPatch, FixtureRequest
from pytestqt.plugin import QtBot

from PyQt5.QtWidgets import QApplication

from gui import widgets, init, GuiOptions


QtAppFixture = tuple[QApplication, widgets.MainWindow, QtBot]
QtAppFixtureGenerator = Generator[tuple[QApplication, widgets.MainWindow, QtBot], Any, None]


@pytest.fixture(autouse=True)
def no_logs_gte_error(caplog: LogCaptureFixture):
	"""Fail test if logging.ERROR or higher"""
	yield
	errors = [record for record in caplog.get_records("call") if record.levelno >= logging.ERROR]
	assert not errors


@pytest.fixture(autouse=True)
def no_prompts(caplog: LogCaptureFixture):
	"""Fail test if logging.ERROR or higher"""
	yield caplog
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


@pytest.fixture(scope="function", params=["Planet Zoo", "Planet Coaster",
					"Jurassic World Evolution", "Jurassic World Evolution 2"])
def OVLTool(qapp: QApplication, qtbot: QtBot, caplog: LogCaptureFixture, request: FixtureRequest) -> QtAppFixtureGenerator:
	from ovl_tool_gui import MainWindow
	opts = GuiOptions(
		log_name = "ovl_tool_gui",
		qapp=qapp
	)
	
	game = str(request.param)
	window, _ = init(MainWindow, opts)
	window.set_ovl_game_choice_game(game)
	qtbot.addWidget(window)
	qtbot.waitUntil(lambda: "loading constants took" in caplog.text.lower(), timeout=25000)
	yield qapp, window, qtbot
	qapp.quit()


@pytest.fixture(scope="function")
def FGMEditor(qapp: QApplication, qtbot: QtBot) -> QtAppFixtureGenerator:
	from fgm_editor_gui import MainWindow
	opts = GuiOptions(
		log_name = "fgm_editor_gui",
		qapp=qapp
	)
	window, _ = init(MainWindow, opts)
	qtbot.addWidget(window)
	yield qapp, window, qtbot
	qapp.quit()


@pytest.fixture(scope="function")
def MS2Tool(qapp: QApplication, qtbot: QtBot) -> QtAppFixtureGenerator:
	from ms2_tool_gui import MainWindow
	opts = GuiOptions(
		log_name = "ms2_tool_gui",
		qapp=qapp
	)
	window, _ = init(MainWindow, opts)
	qtbot.addWidget(window)
	yield qapp, window, qtbot
	qapp.quit()


@pytest.fixture(scope="function")
def MatcolEditor(qapp: QApplication, qtbot: QtBot) -> QtAppFixtureGenerator:
	from matcol_editor_gui import MainWindow
	opts = GuiOptions(
		log_name = "matcol_editor_gui",
		qapp=qapp
	)
	window, _ = init(MainWindow, opts)
	qtbot.addWidget(window)
	yield qapp, window, qtbot
	qapp.quit()


@pytest.fixture(scope="function")
def BNKGui(qapp: QApplication, qtbot: QtBot) -> QtAppFixtureGenerator:
	from bnk_gui import MainWindow
	opts = GuiOptions(
		log_name = "bnk_gui",
		qapp=qapp
	)
	window, _ = init(MainWindow, opts)
	qtbot.addWidget(window)
	yield qapp, window, qtbot
	qapp.quit()


def test_run_ovl_tool(OVLTool: QtAppFixture):
	app, window, _ = OVLTool
	assert "OVL" in window.windowTitle()
	window.close()


def test_run_fgm_editor(FGMEditor: QtAppFixture):
	app, window, _ = FGMEditor
	assert "FGM" in window.windowTitle()
	window.close()


def test_run_ms2_tool(MS2Tool: QtAppFixture):
	app, window, _ = MS2Tool
	assert "MS2" in window.windowTitle()
	window.close()


def test_run_matcol_editor(MatcolEditor: QtAppFixture):
	app, window, _ = MatcolEditor
	assert "Matcol" in window.windowTitle()
	window.close()


def test_run_bnk_gui(BNKGui: QtAppFixture):
	app, window, _ = BNKGui
	assert "BNK" in window.windowTitle()
	window.close()


def test_ovl_tool_new(OVLTool: QtAppFixture, log_succeeds: LogCaptureFixture, monkeypatch: MonkeyPatch):
	app, window, qtbot = OVLTool
	window.file_widget.set_file_path("tests/Files/Files.ovl")
	window.file_widget.dir_opened.emit("tests/Files/")
	qtbot.waitUntil(lambda: "adding succeeded" in window.status_bar.currentMessage().lower(), timeout=10000)

	assert window.file_widget.filepath == "tests/Files/Files.ovl"
	assert "Files.ovl" in window.windowTitle()
	assert "adding succeeded" in log_succeeds.text.lower()
	# Confirm Close
	with monkeypatch.context() as m:
		m.setattr("gui.widgets.MainWindow.showconfirmation", lambda *args, **kwargs: True)
		window.close()
