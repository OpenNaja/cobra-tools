import pytest
import contextlib
from importlib.metadata import Distribution, distribution, PackageNotFoundError
from pytest import MonkeyPatch
from typing import TYPE_CHECKING, Generator, Protocol, Callable, Any, ContextManager

from tests.fixtures.missing_modules import MissingModules

class MissingPackages(Protocol):
	def __call__(self, *packages_to_mock: str) -> ContextManager[None]:
		...


@pytest.fixture
def missing_packages(
	missing_modules: MissingModules,
	monkeypatch: MonkeyPatch
) -> MissingPackages:
	"""
	A fixture that simulates packages being un-installed.

	It mocks the metadata check used by the auto-updater and the import
	statement used by the application.
	"""

	def get_modules_for_package(pkg_name: str) -> list[str]:
		"""Finds the importable top-level module names for a given package."""
		from importlib.metadata import distribution, PackageNotFoundError
		if pkg_name.startswith('types-') or pkg_name.endswith('-stubs'):
			return []
		try:
			dist = distribution(pkg_name)
			try:
				top_level_content = dist.read_text('top_level.txt')
				if top_level_content and top_level_content.strip():
					return top_level_content.strip().splitlines()
			except (FileNotFoundError, AttributeError):
				pass
			# The file is missing or empty
			return [pkg_name.replace('-', '_')]
		except PackageNotFoundError:
			# If the package itself was never found, return an empty list
			return []
	
	@contextlib.contextmanager
	def _manager(*packages_to_mock: str) -> Generator[None, Any, None]:

		# BEFORE applying any mocks
		all_modules_to_block = []
		for pkg_name in packages_to_mock:
			modules = get_modules_for_package(pkg_name)
			all_modules_to_block.extend(modules)

		# Save the original distribution func
		original_distribution: Callable[..., Distribution] = distribution
		# Create a wrapper that fakes the error
		def mock_distribution_wrapper(package_name: str) -> Distribution:
			if package_name in packages_to_mock:
				raise PackageNotFoundError(f"Mocked: '{package_name}' is not installed.")
			# For any other package, call the real function
			return original_distribution(package_name)

		# Patch the metadata check and the import mechanism
		with missing_modules(*all_modules_to_block):
			monkeypatch.setattr("importlib.metadata.distribution", mock_distribution_wrapper)
			yield

	return _manager
