import sys
try:
	import bpy
	# fake-bpy-module lacks the 'app' attribute
	if not hasattr(bpy, "app"):
		# Remove the loaded fake module
		del sys.modules["bpy"]
		# Force subsequent imports of 'bpy' to raise ModuleNotFoundError
		sys.modules["bpy"] = None
except ImportError:
	pass

pytest_plugins = [
	"tests.fixtures.missing_modules",
	"tests.fixtures.missing_packages",
]

def pytest_addoption(parser):
	"""Adds a --tracemalloc command line flag to pytest."""
	parser.addoption(
		"--tracemalloc", action="store_true", default=False, help="Enable tracemalloc"
	)
