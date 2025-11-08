import sys
import pytest
from unittest.mock import MagicMock, patch
from importlib.metadata import PackageNotFoundError

# Functions we want to test
from ovl_util.auto_updater import check_dependencies, extract_package_name, get_modules_for_package


# Mock distribution class to simulate installed packages
class MockDistribution:
	def __init__(self, version):
		self.version = version


MOCK_PYPROJECT_DATA = {
	"project": {
		"dependencies": [
			"imageio~=2.26.0",
			"numpy~=1.22",
			"pillow>=10.0.1",
		],
		"optional-dependencies": {
			"gui": [
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

def test_check_dependencies_all_ok():
	"""Tests the scenario where all packages are correctly installed."""
	deps = ["imageio==2.28.0", "packaging>=21.0"]
	
	MOCK_INSTALLED = {
		"imageio": MockDistribution("2.28.0"),
		"packaging": MockDistribution("22.0")
	}
	
	def mock_dist_finder(name):
		if name in MOCK_INSTALLED:
			return MOCK_INSTALLED[name]
		raise PackageNotFoundError(f"No distribution found for {name}")

	missing, outdated = check_dependencies(deps, mock_dist_finder)

	# Must be empty
	assert not missing
	assert not outdated


def test_check_dependencies_one_missing():
	"""Tests when one package is not installed."""
	deps = ["imageio==2.28.0", "numpy>=1.20"]  # Don't "install" numpy
	
	MOCK_INSTALLED = {
		"imageio": MockDistribution("2.28.0")
	}
	
	def mock_dist_finder(name):
		if name in MOCK_INSTALLED:
			return MOCK_INSTALLED[name]
		raise PackageNotFoundError(f"No distribution found for {name}")

	missing, outdated = check_dependencies(deps, mock_dist_finder)

	assert "numpy" in missing
	assert missing["numpy"] == "numpy>=1.20"
	assert "imageio" not in missing
	assert not outdated


def test_check_dependencies_one_outdated():
	"""Tests when a package is installed but the version is too old."""
	deps = ["imageio>=2.28.0", "packaging~=22.0"]
	
	MOCK_INSTALLED = {
		"imageio": MockDistribution("2.27.0"),  # This version is too old
		"packaging": MockDistribution("22.0")
	}
	
	def mock_dist_finder(name):
		if name in MOCK_INSTALLED:
			return MOCK_INSTALLED[name]
		raise PackageNotFoundError(f"No distribution found for {name}")

	missing, outdated = check_dependencies(deps, mock_dist_finder)

	assert not missing
	assert "imageio" in outdated
	assert outdated["imageio"] == "imageio>=2.28.0"
	assert "packaging" not in outdated


def test_check_dependencies_mixed_issues():
	"""Tests a combination of missing and outdated packages."""
	deps = ["imageio>=2.28.0", "numpy>=1.20", "packaging==22.0"]
	
	MOCK_INSTALLED = {
		"imageio": MockDistribution("2.27.0"),  # Outdated
		# numpy is missing
		"packaging": MockDistribution("22.0")   # OK
	}
	
	def mock_dist_finder(name):
		if name in MOCK_INSTALLED:
			return MOCK_INSTALLED[name]
		raise PackageNotFoundError(f"No distribution found for {name}")

	missing, outdated = check_dependencies(deps, mock_dist_finder)

	assert "numpy" in missing
	assert "imageio" in outdated
	assert "packaging" not in missing and "packaging" not in outdated


@pytest.mark.parametrize("dependency_string, expected_name", [
	("imageio==2.28.0", "imageio"),
	("  numpy ~= 1.20", "numpy"),
	("packaging", "packaging"),
	("my-cool.package>=1.0.0", "my-cool.package"),
	("another_package<=3.4", "another_package"),
	("    ", None),
	("", None),
	(">=1.2.3", None),
])
def test_extract_package_name(dependency_string, expected_name):
	"""
	Tests that the regex helper correctly extracts package names from various
	dependency string formats.
	"""
	assert extract_package_name(dependency_string) == expected_name


class MockReturns:
	RAISE_PACKAGE_NOT_FOUND = "RAISE_PACKAGE_NOT_FOUND"
	RAISE_FILE_NOT_FOUND = "RAISE_FILE_NOT_FOUND"

@pytest.mark.parametrize("package_name, mock_behavior, expected_modules", [
	(  # The ideal case
		"scikit-learn", 
		"sklearn\n_another_module",
		["sklearn", "_another_module"]
	),
	(  # Missing top_level.txt
		"missing-txt", 
		MockReturns.RAISE_FILE_NOT_FOUND,
		["missing_txt"]
	),
	(  # The package is not installed at all
		"non-existent-package", 
		MockReturns.RAISE_PACKAGE_NOT_FOUND,
		[]
	),
	(  # A standard package where install and import names match
		"imageio",
		"imageio",
		["imageio"]
	),
	(  # Package with a top_level.txt that contains only whitespace
		"whitespace-package",
		" \n\t ", # Simulate whitespace-only file content
		["whitespace_package"]
	),
	(  # Prove it returns [] immediately for data packages
		"lxml-stubs",
		"lxml", # Mock valid metadata to prove priority
		[]
	),
	(  # Prove it returns [] immediately for data packages
		"types-pandas",
		"pandas", # Mock valid metadata to prove priority
		[]
	),
])
def test_get_modules_for_package_mocked(package_name, mock_behavior, expected_modules, monkeypatch):
	"""
	Tests the get_modules_for_package function by mocking the call to
	importlib.metadata.distribution to simulate various scenarios.
	"""
	def mock_distribution(pkg_name):
		if mock_behavior == MockReturns.RAISE_PACKAGE_NOT_FOUND:
			raise PackageNotFoundError(f"Mock says {pkg_name} is not found.")
			
		# If the package is "found", we create a mock object to represent it.
		mock_dist_object = MagicMock()

		if mock_behavior == MockReturns.RAISE_FILE_NOT_FOUND:
			# Configure the mock object to raise an error when .read_text() is called
			mock_dist_object.read_text.side_effect = FileNotFoundError
		else:
			# Configure the mock object to return the simulated file content
			mock_dist_object.read_text.return_value = mock_behavior
			
		return mock_dist_object

	monkeypatch.setattr("importlib.metadata.distribution", mock_distribution)

	result = get_modules_for_package(package_name)

	assert set(result) == set(expected_modules)


def test_pip_install_builds_correct_command(monkeypatch):
	"""
	Tests that pip_install constructs the correct `install` list
	"""
	# Use a realistic list of packages from the mock data
	packages_to_install = MOCK_PYPROJECT_DATA["project"]["optional-dependencies"]["gui"]
	
	# Spy on subprocess.check_call
	called_command = None
	def spy_check_call(command_list):
		nonlocal called_command
		called_command = command_list
		return 0
	monkeypatch.setattr("subprocess.check_call", spy_check_call)

	# Import and run the function to be tested
	from ovl_util.auto_updater import pip_install
	pip_install(packages_to_install)

	expected_command = [sys.executable, "-m", "pip", "install"] + packages_to_install
	assert called_command == expected_command


def test_pip_upgrade_builds_correct_command(monkeypatch):
	"""
	Tests that pip_upgrade constructs the correct `install --upgrade` list
	"""
	# Use a realistic list of packages from the mock data
	packages_to_upgrade = MOCK_PYPROJECT_DATA["project"]["dependencies"]
	
	# Spy on subprocess.check_call
	called_command = None
	def spy_check_call(command_list):
		nonlocal called_command
		called_command = command_list
		return 0
	monkeypatch.setattr("subprocess.check_call", spy_check_call)

	# Import and run the function to be tested
	from ovl_util.auto_updater import pip_upgrade
	pip_upgrade(packages_to_upgrade)

	expected_command = [sys.executable, "-m", "pip", "install", "--upgrade"] + packages_to_upgrade
	assert called_command == expected_command


def test_run_update_check_orchestration(monkeypatch):
	"""
	Tests the main orchestration logic
	"""
	# Mock the pure logic functions to return a known state
	missing_deps = {"numpy": "numpy~=1.22"}
	outdated_deps = {"PyQt5": "PyQt5~=5.15.4"}
	monkeypatch.setattr("ovl_util.auto_updater.check_dependencies", lambda *args: (missing_deps, outdated_deps))
	monkeypatch.setattr("ovl_util.auto_updater.get_modules_for_package", lambda *args: [])
	monkeypatch.setattr("tomllib.load", lambda *args: MOCK_PYPROJECT_DATA)

	# Mock user input
	monkeypatch.setattr("ovl_util.auto_updater.install_prompt", lambda *args: True)

	# Create spies for the pip_* helper functions
	installed_packages = []
	upgraded_packages = []
	def spy_pip_install(packages: list[str]):
		installed_packages.append(packages)
		return 0
	def spy_pip_upgrade(packages: list[str]):
		upgraded_packages.append(packages)
		return 0
	monkeypatch.setattr("ovl_util.auto_updater.pip_install", spy_pip_install)
	monkeypatch.setattr("ovl_util.auto_updater.pip_upgrade", spy_pip_upgrade)
	# Patch out the restart logic so the test doesn't exit.
	monkeypatch.setattr("ovl_util.auto_updater._relaunch_application", lambda: None)
	# Patch file I/O and run the main function
	with patch("ovl_util.auto_updater.open", MagicMock()):
		from ovl_util.auto_updater import run_update_check
		run_update_check("manis_tool_gui")

	# Assert the orchestration was correct
	assert installed_packages == [["numpy~=1.22"]]

	all_upgraded_packages = [
		pkg for call_list in upgraded_packages for pkg in call_list
	]
	assert "pip" in all_upgraded_packages
	assert "PyQt5~=5.15.4" in all_upgraded_packages


@pytest.mark.parametrize("tool_name, expected_tool_specific_deps", [
	(
		"manis_tool_gui",
		["matplotlib~=3.10.3"]
	),
	(
		"fgm_editor_gui",
		["pillow<=10.0"]
	),
	(
		"some_other_tool",
		[]
	)
])
def test_get_all_deps(tool_name, expected_tool_specific_deps):
	"""
	Tests that the dependency aggregation logic correctly combines the base,
	gui, and tool-specific dependency lists.
	"""
	from ovl_util.auto_updater import get_all_deps

	result = get_all_deps(MOCK_PYPROJECT_DATA, tool_name)
	expected_deps = (
		MOCK_PYPROJECT_DATA["project"]["dependencies"] +
		MOCK_PYPROJECT_DATA["project"]["optional-dependencies"]["gui"] +
		expected_tool_specific_deps
	)
	assert set(result) == set(expected_deps)
