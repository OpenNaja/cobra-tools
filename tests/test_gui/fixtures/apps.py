from __future__ import annotations
import re
import logging
from typing import TYPE_CHECKING, Any, Generator, Callable, cast

import pytest
from pytest import LogCaptureFixture, FixtureRequest, MonkeyPatch
from pytestqt.plugin import QtBot

if TYPE_CHECKING:
	from PyQt5.QtWidgets import QApplication
	from gui.widgets.window import MainWindow as MW
	QtAppFixture = tuple[QApplication, 'MW', QtBot]
	QtAppFixtureGenerator = Generator[tuple[QApplication, 'MW', QtBot], Any, None]
	WindowHook = Callable[['MW'], None]


def _create_gui_fixture_generator(
	main_window_class: type[MW],
	log_name: str,
	qapp: QApplication,
	qtbot: QtBot,
	monkeypatch: MonkeyPatch,
	pre_show_hook: WindowHook | None = None,
	post_show_hook: WindowHook | None = None,
	setup_hook: WindowHook | None = None,
	teardown_hook: WindowHook | None = None,
) -> QtAppFixtureGenerator:
	"""
	A generic factory for creating and managing GUI application fixtures.

	This function handles repetitive setup and teardown logic (window creation,
	monkeypatching, cleanup) and provides hooks for injecting custom logic at
	key points in the fixture's lifecycle.

	Lifecycle Hooks:
	----------------
	- setup_hook: Runs after window creation, before qtbot captures exceptions.
	  - Use: Abstracting complex or reusable setup logic into standalone functions.
	  - NO Use: Setup must instead be done in the fixture body to share variables
	    with other hooks via closures.

	- pre_show_hook: Runs inside qtbot's exception capture before the window is shown.
	  - Use: Catching setup errors and configuring the UI's initial state before it is rendered.

	- post_show_hook: Runs after the window is visible and ready for interaction.
	  - Use: The primary hook for simulating and waiting for user actions, 
	    and asserting on the resulting state.

	- teardown_hook: Runs after the window has been closed and torn down.
	  - Use: Guaranteed resource cleanup and final assertions
	"""
	from gui import create_window, GuiOptions

	# --- Common Setup ---
	opts = GuiOptions(log_name=log_name, qapp=qapp)
	monkeypatch.setattr("gui.widgets.window.MainWindow.showdialog", lambda *args, **kwargs: True)
	window, _ = create_window(main_window_class, opts)

	# Pre-run
	if setup_hook:
		setup_hook(window)

	with qtbot.capture_exceptions() as exceptions:
		qtbot.addWidget(window)

		# Before window.show()
		if pre_show_hook:
			pre_show_hook(window)

		print(f"\nWaiting for {log_name} Window...")
		with qtbot.waitExposed(window, timeout=5000):
			window.show()
		print("\nWindow Exposed...")

		# After window.show()
		if post_show_hook:
			post_show_hook(window)

		print("\nYielding...")
		yield qapp, window, qtbot

		# --- Common Teardown ---
		print("\nTeardown...")
		window.close()
		qtbot.waitUntil(lambda: not window.isVisible(), timeout=5000)
		window.deleteLater()

	# Post-run teardown
	if teardown_hook:
		teardown_hook(window)

	assert not exceptions, f"Uncaught Qt exceptions found during test: {exceptions}"


@pytest.fixture(scope="function", params=["Planet Zoo", "Planet Coaster",
					"Jurassic World Evolution", "Jurassic World Evolution 2"])
def OVLTool(
	qapp: QApplication,
	qtbot: QtBot,
	caplog: LogCaptureFixture,
	request: FixtureRequest,
	monkeypatch: MonkeyPatch,
	trace_qtimer: None,  # Optional trace
	trace_signal: None,  # Optional trace
) -> QtAppFixtureGenerator:
	"""Fixture for OVLTool"""
	from ovl_tool_gui import MainWindow

	# Define custom logic in a nested function that has access to the fixture's scope
	def _post_show_logic(window: MainWindow):
		game = str(request.param)
		window.ovl_manager.game_choice.game_chosen(game)
		print("\nWaiting for Logs ...")
		qtbot.waitUntil(lambda: "Loading constants took" in caplog.text, timeout=5000)
		qtbot.waitUntil(lambda: f"Setting OVL version to {game}" in caplog.text, timeout=5000)

	# Use yield from to delegate generator control to the factory
	yield from _create_gui_fixture_generator(
		main_window_class=MainWindow,
		log_name="ovl_tool_gui",
		qapp=qapp,
		qtbot=qtbot,
		monkeypatch=monkeypatch,
		post_show_hook=_post_show_logic,
	)


@pytest.fixture(scope="function")
def FGMEditor(qapp: QApplication, qtbot: QtBot, monkeypatch: MonkeyPatch) -> QtAppFixtureGenerator:
	"""Fixture for FGMEditor"""
	from fgm_editor_gui import MainWindow
	yield from _create_gui_fixture_generator(
		main_window_class=MainWindow,
		log_name="fgm_editor_gui",
		qapp=qapp,
		qtbot=qtbot,
		monkeypatch=monkeypatch
	)


@pytest.fixture(scope="function")
def MS2Tool(qapp: QApplication, qtbot: QtBot, monkeypatch: MonkeyPatch) -> QtAppFixtureGenerator:
	"""Fixture for MS2Tool"""
	from ms2_tool_gui import MainWindow
	yield from _create_gui_fixture_generator(
		main_window_class=MainWindow,
		log_name="ms2_tool_gui",
		qapp=qapp,
		qtbot=qtbot,
		monkeypatch=monkeypatch
	)


@pytest.fixture(scope="function")
def MatcolEditor(qapp: QApplication, qtbot: QtBot, monkeypatch: MonkeyPatch) -> QtAppFixtureGenerator:
	"""Fixture for MatcolEditor"""
	from matcol_editor_gui import MainWindow
	yield from _create_gui_fixture_generator(
		main_window_class=MainWindow,
		log_name="matcol_editor_gui",
		qapp=qapp,
		qtbot=qtbot,
		monkeypatch=monkeypatch
	)


@pytest.fixture(scope="function")
def BNKGui(qapp: QApplication, qtbot: QtBot, monkeypatch: MonkeyPatch) -> QtAppFixtureGenerator:
	"""Fixture for BNKGui"""
	from bnk_gui import MainWindow
	yield from _create_gui_fixture_generator(
		main_window_class=MainWindow,
		log_name="bnk_gui",
		qapp=qapp,
		qtbot=qtbot,
		monkeypatch=monkeypatch
	)
