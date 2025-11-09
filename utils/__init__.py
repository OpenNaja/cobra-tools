from pathlib import Path


root_dir = Path(__file__).resolve().parent.parent


def is_dev_environment():
	"""
	Checks if running in a development environment
	"""
	try:
		from importlib.util import find_spec
		has_git = (root_dir / ".git").is_dir()
		has_pytest = find_spec("pytest")
		return has_git and has_pytest
	except Exception as e:
		return False
