import sys
import pytest
import contextlib
import importlib.machinery
from threading import Lock
from importlib.abc import Loader, MetaPathFinder
from types import ModuleType
from typing import Protocol, Iterable, Sequence, Generator, Any, ContextManager

class MissingModules(Protocol):
	"""A protocol describing the callable to simulate missing modules."""
	def __call__(self, *modules_to_block: str) -> ContextManager[None]:
		...

# Core Mechanism

class _ModuleBlockerLoader(Loader):
	"""A custom loader that always raises ModuleNotFoundError"""
	def __init__(self, fullname: str) -> None:
		self.fullname = fullname

	def exec_module(self, _module: ModuleType) -> None:
		raise ModuleNotFoundError(
			f"Mocked import error: '{self.fullname}' is blocked by 'missing_modules'.",
			name=self.fullname
		)

class _ModuleBlockerFinder(MetaPathFinder):
	"""A custom finder that intercepts import attempts for specific modules"""
	def __init__(self, modules_to_block: Iterable[str]) -> None:
		self.modules_to_block: set[str] = set(modules_to_block)

	def find_spec(self, fullname: str, _path: Sequence[str] | None = None, _target: ModuleType | None = None
	) -> importlib.machinery.ModuleSpec | None:
		if any(fullname == mod or fullname.startswith(f"{mod}.") for mod in self.modules_to_block):
			return importlib.machinery.ModuleSpec(fullname, _ModuleBlockerLoader(fullname))
		return None

# Plugin Structure

_LOCK = Lock()  # pytest-xdist thread safety

class MissingModulesContext:
	"""Provides a context manager to simulate missing modules"""
	
	def __init__(self, monkeypatch: pytest.MonkeyPatch) -> None:
		self.monkeypatch = monkeypatch

	@contextlib.contextmanager
	def __call__(self, *modules_to_block: str) -> Generator[None, Any, None]:
		with _LOCK:
			# Safely clean up sys.modules
			for name in list(sys.modules):
				if any(name == mod or name.startswith(f"{mod}.") for mod in modules_to_block):
					self.monkeypatch.delitem(sys.modules, name, raising=False)

			# Use MetaPathFinder
			blocker = _ModuleBlockerFinder(modules_to_block)
			sys.meta_path.insert(0, blocker)
		try:
			yield
		finally:
			# Teardown
			with _LOCK:
				if sys.meta_path and sys.meta_path[0] is blocker:
					sys.meta_path.pop(0)


@pytest.fixture
def missing_modules(monkeypatch: pytest.MonkeyPatch) -> MissingModules:
	"""
	Pytest fixture to simulate missing modules for testing optional dependencies
	"""
	return MissingModulesContext(monkeypatch)
