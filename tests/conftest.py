
pytest_plugins = [
	"tests.fixtures.missing_modules",
	"tests.fixtures.missing_packages",
]

def pytest_addoption(parser):
	"""Adds a --tracemalloc command line flag to pytest."""
	parser.addoption(
		"--tracemalloc", action="store_true", default=False, help="Enable tracemalloc"
	)
