import logging
from pathlib import Path
from packaging.version import parse, Version
from typing import TYPE_CHECKING, Callable, TypeAlias

from ovl_util.config import load_config, save_config


MigrationFunc: TypeAlias = Callable[[dict], None]


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
