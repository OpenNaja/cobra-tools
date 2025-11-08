from __future__ import annotations
import logging
from unittest.mock import MagicMock
from typing import TYPE_CHECKING, Any, Generator, Protocol, Callable

import pytest

from tests.test_gui.fixtures.apps import *
if TYPE_CHECKING:
	from pytest import MonkeyPatch
	from pytestqt.plugin import QtBot
	from PyQt5.QtWidgets import QApplication
	from gui.widgets.window import MainWindow
	from tests.fixtures.missing_packages import MissingPackages


MOCK_PYPROJECT_DATA = {
	"project": {
		"dependencies": [
			"imageio~=2.26.0",
			"numpy~=1.22",
			"pillow>=10.0.1",
		],
		"optional-dependencies": {
			"gui": [
				"PyQt5-Frameless-Window~=0.2.8",
				"PyQt5~=5.15.4",
				"vdf~=3.4",
			],
			"manis_tool_gui": [
				"matplotlib~=3.10.3",
			],
			"fgm_editor_gui": [
				"pillow<=10.0",  # TODO: Contradictory version testing
			]
		}
	}
}

MOCK_MISSING = {
	"PyQt5-Frameless-Window": "PyQt5-Frameless-Window~=0.2.8",
	"numpy": "numpy~=1.22",
	"imageio": "imageio~=2.26.0"
}

MOCK_OUTDATED = {
	"vdf": "vdf~=3.4"
}


class UpdateHarness(Protocol):
	"""
	A Protocol for the callable factory returned by the harness fixture
	"""
	def __call__(
		self,
		user_response_to_prompt: bool,
		*,
		missing_deps: dict[str, str] | None = None,
		outdated_deps: dict[str, str] | None = None
	) -> tuple['MainWindow', list[str], list[str], list[str]]:
		...


@pytest.fixture(scope="function")
def update_harness(
	qapp,
	qtbot,
	monkeypatch
) -> Generator[Callable[..., tuple['MainWindow', list, list, list]], Any, None]:
	"""
	A configurable harness fixture using FGM Editor for integration tests.

	This fixture returns a factory function that takes the user's response
	to the install prompt as an argument. It sets up the mocked
	application environment and yields the results.
	"""

	created_windows: list[MainWindow] = []
	def _create_harness(
		user_response: bool,
		missing_deps: dict[str, str] = MOCK_MISSING,
		outdated_deps: dict[str, str] = MOCK_OUTDATED
	):
		"""
		Creates an FGM Editor with patched `run_update_check` for integration testing.

		This fixture:
		1. Launches the application via setup_app()
		2. Allows the patched `run_update_check` to execute
		3. Mocks all external boundaries (pip, user input, files)
		4. Provides spies to capture the results of the updater execution

		Returns:
			- window: The launched MainWindow instance
			- called_tools: List of tool names passed to run_update_check
			- called_install_packages: List of packages passed to pip_install
			- called_upgrade_packages: List of packages passed to pip_upgrade
		"""
		# Spies to capture side-effects
		called_tools = []
		called_install_packages = []
		called_upgrade_packages = []
		# Spy wrapper for update_check
		from ovl_util import auto_updater
		original_run_update_check = auto_updater.run_update_check
		def spy_wrapper_run_update_check(tool_name: str):
			called_tools.append(tool_name)
			return original_run_update_check(tool_name)
		monkeypatch.setattr(auto_updater, "run_update_check", spy_wrapper_run_update_check)

		# Mock dependency data
		monkeypatch.setattr(
			"ovl_util.auto_updater.check_dependencies",
			lambda *args, **kwargs: (missing_deps, outdated_deps)
		)

		# Mock user choice
		monkeypatch.setattr("ovl_util.auto_updater.install_prompt", lambda *args: user_response)
		# Patch out the restart logic so the test doesn't exit.
		monkeypatch.setattr("ovl_util.auto_updater._relaunch_application", lambda: None)

		# Spies for pip actions
		def spy_pip_install(packages: list[str]):
			called_install_packages.extend(packages)
			return 0
		monkeypatch.setattr("ovl_util.auto_updater.pip_install", spy_pip_install)

		def spy_pip_upgrade(packages: list[str]):
			called_upgrade_packages.extend(packages)
			return 0
		monkeypatch.setattr("ovl_util.auto_updater.pip_upgrade", spy_pip_upgrade)
		# Mock all other external dependencies
		monkeypatch.setattr("tomllib.load", lambda *args: MOCK_PYPROJECT_DATA)
		monkeypatch.setattr("ovl_util.auto_updater.get_modules_for_package", lambda *args: ["mock_module"])
		monkeypatch.setattr("importlib.import_module", lambda *args: MagicMock())

		# Setup app, calling patched auto_updater
		from fgm_editor_gui import MainWindow
		from gui import setup_app, GuiOptions
		opts = GuiOptions(log_name="fgm_editor_gui", qapp=qapp, check_update=True)
		window, _ = setup_app(MainWindow, opts)
		qtbot.addWidget(window)
		# Track the created window for explicit cleanup
		created_windows.append(window)
		
		return window, called_tools, called_install_packages, called_upgrade_packages

	# Yields the factory function
	yield _create_harness

	# Explicitly delete Qt objects before VSCode's reporter can race the GC.
	try:
		logging.debug(f"\nFixture teardown: Deleting {len(created_windows)} windows.")
		for window in created_windows:
			window.deleteLater()
		
		# Force Qt to process the deleteLater() events
		if qapp:
			qapp.processEvents()
	except Exception as e:
		# Don't crash the test run if teardown fails
		logging.error(f"Error during fixture teardown: {e}")

def test_updater_is_triggered_with_during_app_prep(update_harness: UpdateHarness):
	"""Tests that setup_app calls the updater with the correct tool_name."""
	_, called_tools, _, _ = update_harness(user_response=True)
	assert "fgm_editor_gui" in called_tools


def test_updater_installs_missing_packages(update_harness: UpdateHarness):
	"""Tests that the updater logic correctly identifies and installs missing packages."""
	_, _, called_install_packages, _ = update_harness(user_response=True)

	# Install the values from the dict ("package~=1.2.3")
	expected_installs = list(MOCK_MISSING.values())
	assert len(called_install_packages) == len(expected_installs)
	for package in expected_installs:
		assert package in called_install_packages


def test_updater_upgrades_outdated_packages(update_harness: UpdateHarness):
	"""Tests that the updater logic correctly identifies and upgrades outdated packages."""
	_, _, _, called_upgrade_packages = update_harness(user_response=True)

	# The upgrade logic calls pip_upgrade for 'pip' itself first
	assert "pip" in called_upgrade_packages
	
	expected_upgrades = list(MOCK_OUTDATED.values())
	assert len(called_upgrade_packages) == len(expected_upgrades) + 1  # +1 for pip
	for package in expected_upgrades:
		assert package in called_upgrade_packages


def test_app_window_is_valid_after_update_check(update_harness: UpdateHarness):
	"""Tests that the app is still in a valid state after the updater runs."""
	window, _, _, _ = update_harness(user_response=True)
	assert "FGM" in window.windowTitle()


def test_updater_app_if_user_declines_optional_install(
	update_harness: UpdateHarness,
	missing_packages: MissingPackages
):
	"""
	Tests that the app can still launch if an optional dependency is missing
	and the user answers "n" to the install prompt.
	"""
	NO_FRAMELESS = {
		"PyQt5-Frameless-Window": "PyQt5-Frameless-Window~=0.2.8"
	}
	with missing_packages("PyQt5-Frameless-Window"):
		window, _, installed, _ = update_harness(user_response=False, missing_deps=NO_FRAMELESS)
		assert "FGM" in window.windowTitle()
		assert len(installed) == 0
