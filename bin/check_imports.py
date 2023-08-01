#!/usr/bin/env python
import argparse
from typing import Sequence

from utils.imports import get_imports


def check_imports(filenames) -> int:
	"""Ensures GUI files have GUI setup and auto_updater imports before certain imports"""
	retv = 0
	filenames = set(filenames)
	for file in filenames:
		retv_file = 0
		setup_passed = False
		updater_passed = False
		widgets_passed = False
		imports = list(get_imports(file))
		# widgets.py
		has_auto_updater = any(i for i in imports if i.name == "auto_updater")
		# GUI Files
		has_gui_setup = any(i for i in imports if i.modules == ["gui", "setup"])
		has_widgets = any(i for i in imports if i.module == "gui" and i.name == "widgets")
		if not has_gui_setup and not has_widgets and not has_auto_updater:
			print(f"Skipping {file}")
			continue

		setup_error = False
		widgets_error = False
		updater_error = False

		print(f"Checking {file}")
		for i in imports:
			# Python built-in imports are OK
			if i.module_source == "BUILTIN":
				continue
			# Typing is fine except before the Python version check (from imports)
			if i.module_source == "TYPING" and not has_gui_setup and not has_auto_updater and not has_widgets:
				continue

			# Track imports
			is_updater = i.name == "auto_updater"
			is_setup = i.modules == ["gui", "setup"]
			is_widget = i.module == "gui" and i.name == "widgets"
			if is_updater:
				updater_passed = True
			if is_setup:
				setup_passed = True
			if is_widget:
				widgets_passed = True

			# Errors above setup import
			if has_gui_setup and not setup_passed and not is_setup:
				if not setup_error:
					print(f"  Error: The following imports must come after `from gui.setup import ...`")
					setup_error = True
				print(f"    {i.module_source.title()}: `{i}`")
				retv_file = 1
				continue
			# Errors above widgets import
			if has_widgets and not widgets_passed and not is_widget and not is_setup:
				if not widgets_error:
					print(f"  Error: The following imports must come after `from gui import widgets`")
					widgets_error = True
				print(f"    {i.module_source.title()}: `{i}`")
				retv_file = 1
				continue
			# Errors above updater import
			if has_auto_updater and not updater_passed and not is_updater:
				if not updater_error:
					print(f"  Error: The following imports must come after `auto_updater` import")
					updater_error = True
				print(f"    {i.module_source.title()}: `{i}`")
				retv_file = 1
				continue
			if retv_file:
				retv = 1
		if not retv_file:
			print("  OK")
	return retv


def main(argv: Sequence[str] | None = None) -> int:
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'filenames', nargs='*', help='Filenames pre-commit believes are changed.',
	)
	args = parser.parse_args(argv)
	return check_imports(args.filenames)


if __name__ == '__main__':
	exit(main())