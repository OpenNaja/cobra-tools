import pytest
from tests.fixtures.missing_modules import MissingModules


def test_app_import_recovers_if_optional_module_is_missing(
	missing_modules: MissingModules
):
	"""
	Tests that importing a GUI module succeeds if an optional
	module is not available.
	"""
	import importlib
	with missing_modules("qframelesswindow"):
		import fgm_editor_gui
		module = importlib.reload(fgm_editor_gui)
		assert module is not None


def test_app_import_fails_if_critical_module_is_missing(
	missing_modules: MissingModules
):
	"""
	Tests that importing a GUI module fails if PyQt5 is not available.
	"""
	import importlib
	with missing_modules("PyQt5"):
		with pytest.raises(ModuleNotFoundError):
			import fgm_editor_gui
			importlib.reload(fgm_editor_gui)

