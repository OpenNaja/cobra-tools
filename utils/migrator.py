import logging
import shutil
from pathlib import Path
from packaging.version import parse, Version
from typing import TYPE_CHECKING, Callable, TypeAlias

from ovl_util.auto_updater import install_prompt, pip_install, pip_upgrade
from ovl_util.config import load_config, save_config


MigrationFunc: TypeAlias = Callable[[dict], None]

class MigrationSkippedError(Exception):
    """Raised when a migration is intentionally skipped by the user."""
    pass


root_dir = Path(__file__).parent.parent.resolve()


class Migrator:
	_REGISTRY: list[tuple[str, MigrationFunc]] = []

	@classmethod
	def register(cls, version_str) -> Callable[[MigrationFunc], MigrationFunc]:
		"""A class-method decorator to register a migration function."""
		def decorator(func: MigrationFunc) -> MigrationFunc:
			cls._REGISTRY.append((version_str, func))
			logging.debug(f"Registered migration '{func.__name__}' for version {version_str}")
			return func
		return decorator

	@staticmethod
	def _run_pip_install(packages: list[str]) -> None:
		"""Internal helper to run pip install. Raises CalledProcessError on failure."""
		if not packages:
			return
		pip_install(packages)

	@staticmethod
	def _run_pip_upgrade(packages: list[str]) -> None:
		"""Internal helper to run pip upgrade. Raises CalledProcessError on failure."""
		if not packages:
			return
		pip_upgrade(packages)

	@staticmethod
	def install_packages(packages: list[str]) -> None:
		"""
		Utility for migrations to install packages without a prompt.
		Raises CalledProcessError on failure.
		"""
		logging.debug(f"Attempting silent install of: {packages}")
		Migrator._run_pip_install(packages)

	@staticmethod
	def install_packages_prompt(packages: list[str], question: str | None = None) -> None:
		"""
		Utility for migrations to prompt user before installing packages.
		Raises CalledProcessError on failure.
		Raises MigrationSkippedError if user cancels.
		"""
		if not packages:
			return
		
		if question is None:
			question = f"This update needs to install the following packages: {', '.join(packages)}. Proceed?"
		
		if install_prompt(question):
			Migrator._run_pip_install(packages)
		else:
			logging.warning(f"User skipped installation of: {packages}")
			raise MigrationSkippedError(f"User skipped installation of {packages}")

	@staticmethod
	def upgrade_packages(packages: list[str]) -> None:
		"""
		Utility for migrations to upgrade packages without a prompt.
		Raises CalledProcessError on failure.
		"""
		logging.debug(f"Attempting silent upgrade of: {packages}")
		Migrator._run_pip_upgrade(packages)

	@staticmethod
	def upgrade_packages_prompt(packages: list[str], question: str | None = None) -> None:
		"""
		Utility for migrations to prompt user before upgrading packages.
		Raises CalledProcessError on failure.
		Raises MigrationSkippedError if user cancels.
		"""
		if not packages:
			return
		
		if question is None:
			question = f"This update needs to upgrade the following packages: {', '.join(packages)}. Proceed?"
			
		if install_prompt(question):
			Migrator._run_pip_upgrade(packages)
		else:
			logging.warning(f"User skipped upgrade of: {packages}")
			raise MigrationSkippedError(f"User skipped upgrade of {packages}")

	@staticmethod
	def delete_paths(relative_paths: list[str]) -> None:
		"""
		Utility for migrations to delete a list of files or directories
		relative to the root dir.
		"""
		logging.debug(f"Attempting to delete {len(relative_paths)} relative paths...")
		for rel_path in relative_paths:
			try:
				# Resolve the path.
				abs_path = (root_dir / rel_path).resolve()
				# Check if the final path is a child of root_dir
				if not abs_path.is_relative_to(root_dir):
					logging.warning(f"Skipping unsafe path (resolved outside root): {rel_path}")
					continue

				if not abs_path.exists():
					logging.debug(f"  -> Path not found, skipping: {rel_path}")
					continue

				if abs_path.is_file() or abs_path.is_symlink():
					abs_path.unlink()
					logging.debug(f"  -> Deleted file/link: {rel_path}")
				elif abs_path.is_dir():
					shutil.rmtree(abs_path)
					logging.debug(f"  -> Recursively deleted directory: {rel_path}")
			except Exception as e:
				# This catches file operation errors (e.g., permissions)
				logging.error(f"Failed to delete path '{rel_path}': {e}", exc_info=True)

	def __init__(self, config_path: Path | str, current_app_version: str) -> None:
		"""
		Args:
			config_path (str or Path): The file path to the config.json.
			current_app_version (str): The application's current version.
		"""
		self.config_path = config_path
		self.current_version = parse(current_app_version)
		self._migrations: dict[Version, list[MigrationFunc]] = {}
		self._fresh_install = not Path(self.config_path).exists()
		
		# Load the config dictionary on initialization
		self.config = load_config(self.config_path)

	def _collect_migrations(self) -> None:
		"""Processes the class-level _REGISTRY into an instance-level dict."""
		for version_str, func in self._REGISTRY:
			version = parse(version_str)
			if version not in self._migrations:
				self._migrations[version] = []
			self._migrations[version].append(func)

	def run(self) -> None:
		"""
		Runs all pending migrations.
		
		This method is now fully self-contained. It imports migrations,
		collects them, runs them, and saves the config as needed.
		"""
		# Import and collect migrations
		import utils.migrations  
		self._collect_migrations()

		if self._fresh_install:
			self.config['version'] = str(self.current_version)
			save_config(self.config_path, self.config)
			return

		config_version_str = self.config.get('version', '0.0.0')
		config_version = parse(config_version_str)

		logging.debug(f"Config version: {config_version}")
		logging.debug(f"Current app version: {self.current_version}")

		if config_version >= self.current_version:
			logging.debug("Configuration is up to date. No migration needed.")
			return

		logging.debug("Migration needed. Starting process...")
		
		pending_migrations = sorted([
			v for v in self._migrations.keys() 
			if config_version < v <= self.current_version
		])

		if not pending_migrations:
			logging.debug("No pending migration scripts found for the required range.")
			# Even if no scripts ran, we update the version
			self.config['version'] = str(self.current_version)
			save_config(self.config_path, self.config)
			return

		for version in pending_migrations:
			logging.debug(f"--- Applying migrations for version {version} ---")
			for command in self._migrations[version]:
				try:
					logging.debug(f"  -> Running '{command.__name__}'...")
					# Pass the config dictionary to the command
					command(self.config) 
					logging.debug(f"  -> Success.")
				except Exception as e:
					logging.error(f"  -> ERROR: Migration '{command.__name__}' failed: {e}")
					logging.error(f"Migration '{command.__name__}' failed", exc_info=True)
					return

			# Save after each successful version bump for resumability
			self.config['version'] = str(version)
			save_config(self.config_path, self.config)
			logging.debug(f"--- Successfully migrated to {version} ---")

		logging.info("All migrations applied successfully.")
