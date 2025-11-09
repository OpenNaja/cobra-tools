import sys
import logging
from pathlib import Path

from .migrator import Migrator

root_dir = Path(__file__).resolve().parent.parent

@Migrator.register("1.0.1")
def remove_old_widgets_module(config):
	gui_dir = root_dir / "gui"
	old_widgets_file = gui_dir / "widgets.py"
	new_widgets_package = gui_dir / "widgets"
	pycache_path = gui_dir / "__pycache__"

	if old_widgets_file.is_file() and new_widgets_package.is_dir():
		try:
			logging.warning(f"Old '{old_widgets_file}' found. Attempting to remove it.")
			old_widgets_file.unlink()
			if pycache_path.is_dir():
				for old_pyc in pycache_path.glob("widgets.*.pyc"):
					logging.warning(f"Removing orphaned bytecode file: {old_pyc.name}")
					old_pyc.unlink()
		except (OSError, PermissionError) as e:
			logging.critical(f"CRITICAL ERROR: Could not remove conflicting file {old_widgets_file}. Please check permissions.", file=sys.stderr)
			sys.exit(1)

@Migrator.register("1.0.1")
def restructure_game_config(config):
	"""
	Converts the 'games' config from a simple "name: path" map
	to a "name: {path: ..., recent: []}" structure.
	
	Also deletes old top-level 'recent_...' keys.
	"""
	print("   - Running 'restructure_game_config' migration...")
	
	# Restructure the 'games' dictionary
	if "games" not in config:
		print("   - 'games' key not found. Skipping games restructure.")
	else:
		migrated_count = 0
		game_dict = config["games"]
		for game_name, game_data in game_dict.items():
			if isinstance(game_data, str):
				game_dict[game_name] = {
					"path": game_data,
					"recent": []
				}
				migrated_count += 1

		if migrated_count > 0:
			print(f"   - Migrated {migrated_count} game entries to new structure.")
		else:
			print("   - All game entries already in new structure.")

	# Delete old 'recent_' keys from the root
	keys_to_delete = []
	for key in config.keys():
		if isinstance(key, str) and key.startswith("recent_"):
			keys_to_delete.append(key)
	if keys_to_delete:
		print(f"   - Found {len(keys_to_delete)} old 'recent_' keys to delete.")
		for key in keys_to_delete:
			del config[key]
			print(f"     - Deleted '{key}'")
	else:
		print("   - No old 'recent_' keys found.")

@Migrator.register("1.0.2")
def remove_old_files_1_0_2(config):
	Migrator.delete_paths(["ovl_util"])
