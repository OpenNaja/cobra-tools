"""
Deals with missing packages and tries to install them from the tool itself.
"""

import re
import os
import sys
import time
import logging
import subprocess
from typing import Callable

from utils.logs import ANSI

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _relaunch_application():
    """
    Logs, waits, and then relaunches the application.
    """
    print("Restarting application...")
    time.sleep(2)
    if sys.platform == "win32":
        # Use subprocess.Popen to work around second process exit hanging console
        subprocess.Popen([sys.executable] + sys.argv, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    sys.exit(0)


def wait_for_user_exit(message: str | None) -> None:
    """Prints a message and waits for the user to press Enter."""
    if message:
        print(f"\n{ANSI.LIGHT_RED}{message}{ANSI.END}")
    print(f"{ANSI.LIGHT_WHITE}Press Enter to exit...{ANSI.END}")
    input()


def install_prompt(question: str) -> bool:
    """ask question and return True if user confirms"""
    print(f"{ANSI.LIGHT_WHITE}{question}{ANSI.END} (y/N)")
    print(f"{ANSI.LIGHT_YELLOW}[Type y and hit Enter]{ANSI.END}{ANSI.LIGHT_GREEN}")
    return input().lower() in {'yes', 'y', 'ye'}


def pip_install(packages: list[str]) -> int:
    """use pip to install a list of packages"""
    if not packages:
        return 0
    logging.info(f"Installing {packages}")
    command = [sys.executable, "-m", "pip", "install"] + packages
    return subprocess.check_call(command)


def pip_upgrade(packages: list[str]) -> int:
    """use pip to install --upgrade a list of packages"""
    if not packages:
        return 0
    logging.info(f"Updating {packages}")
    command = [sys.executable, "-m", "pip", "install", "--upgrade"] + packages
    return subprocess.check_call(command)


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


def extract_package_name(line: str) -> str | None:
    """Extracts the package name from a dependency string using regex."""
    lib_match = re.match(r"^\s*([a-zA-Z0-9_.-]+)", line)
    if not lib_match:
        return None
    return lib_match.group(1)


def check_dependencies(all_deps: list[str], dist_finder: Callable) -> tuple[dict[str, str], dict[str, str]]:
    """
    Checks dependencies against a provided distribution finder.
    """
    from importlib.metadata import PackageNotFoundError

    MISSING: dict[str, str] = {}
    OUTDATED: dict[str, str] = {}

    # Check for missing packages first
    for line in all_deps:
        lib = extract_package_name(line)
        if not lib:
            continue
        try:
            dist_finder(lib)
        except PackageNotFoundError:
            logging.warning(f"{lib} is not installed.")
            MISSING[lib] = line  # Need full line including ~= for pip install command

    # Now check for outdated packages
    try:
        from packaging.specifiers import SpecifierSet
        logging.debug("Checking for outdated packages...")
        for line in all_deps:
            lib = extract_package_name(line)
            if not lib or lib in MISSING:
                continue
            try:
                lib_dist = dist_finder(lib)
                # Create a specifier from the requirement line, e.g., ">=1.2.3"
                specifier_str = line.replace(lib, '').strip()
                if specifier_str and not SpecifierSet(specifier_str).contains(lib_dist.version):
                    logging.warning(f"{lib} is out of date. Found: {lib_dist.version}, require: {line}")
                    OUTDATED[lib] = line
            except PackageNotFoundError:
                # Should not happen in this loop
                continue
    except ImportError:
        logging.warning("The 'packaging' library is not installed. Skipping check for outdated packages.")

    return MISSING, OUTDATED


def get_all_deps(pyproject: dict, tool_name: str) -> list[str]:
    """Extracts and combines all relevant dependency lists from pyproject.toml"""
    project = pyproject.get('project', {})
    deps = project.get('dependencies', [])
    optional_deps = project.get('optional-dependencies', {})
    deps_gui = optional_deps.get('gui', [])
    deps_tool = optional_deps.get(tool_name, [])
    return deps + deps_gui + deps_tool


def run_update_check(tool_name: str) -> list[str] | None:
    """
    Checks for missing or outdated dependencies defined in pyproject.toml
    and prompts the user to install or update them.

    Returns:
        A list of module names that are required, if successful.
        None, if the process fails or is aborted.
    """
    logging.debug("Checking for automatic module updates")
    if (sys.version_info.major, sys.version_info.minor) < (3, 11):
        logging.critical(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}. Install Python 3.11+ and try again.")
        wait_for_user_exit()
    try:
        import tomllib
        from importlib import import_module
        from importlib.util import find_spec
        from importlib.metadata import distribution

        INSTALLED: list[str] = []
        UPDATED: list[str] = []
        MODULES: list[str] = []

        pyproject_path = os.path.join(root_dir, "pyproject.toml")
        with open(pyproject_path, 'rb') as fproj:
            pyproject = tomllib.load(fproj)
            all_deps = get_all_deps(pyproject, tool_name)

        # Install `packaging` if missing
        if not find_spec("packaging"):
            pip_install(["packaging"])
        # Call the distribution finder
        MISSING, OUTDATED = check_dependencies(all_deps, distribution)

        # Populate modules from packages that are already installed and relevant
        all_libs = {extract_package_name(line) for line in all_deps if extract_package_name(line)}
        for lib in all_libs:
            if lib not in MISSING:
                MODULES.extend(m for m in get_modules_for_package(lib) if m not in MODULES)

        # Update pip
        if MISSING or OUTDATED:
            pip_upgrade(['pip'])

        # Install MISSING packages
        if MISSING and install_prompt("Install the missing dependencies?"):
            # Batch all missing packages into a single pip command
            # This ensures correct dependency resolution via pip
            packages_to_install = list(MISSING.values())
            if pip_install(packages_to_install) == 0:
                for key in MISSING:
                    INSTALLED.append(key)
                    MODULES.extend(m for m in get_modules_for_package(key) if m not in MODULES)

        # Update OUTDATED packages
        if OUTDATED and install_prompt("Update the outdated dependencies?"):
            packages_to_update = list(OUTDATED.values())
            if pip_upgrade(packages_to_update) == 0:
                for key in OUTDATED:
                    UPDATED.append(key)

        if INSTALLED or UPDATED:
            from importlib import invalidate_caches
            invalidate_caches()
            
            if hasattr(logging, "success"):
                if INSTALLED:
                    logging.success(f"Installed: {INSTALLED}")
                if UPDATED:
                    logging.success(f"Updated: {UPDATED}")

            # Relaunch to avoid DLL issues (e.g. initial install of Qt)
            print("Packages were installed/updated.")
            _relaunch_application()

        logging.debug("Verifying all required modules can be imported...")
        for module in MODULES:
            try:
                import_module(module)
            except ImportError:
                logging.error(f"{module} could not be imported; install the required dependencies with pip!")
                time.sleep(15)
                return None

        logging.debug("All modules verified successfully")
        return MODULES
    except FileNotFoundError:
        logging.error("pyproject.toml not found in the expected location")
    except Exception as e:
        logging.exception(f"auto_updater encountered an unrecoverable error: {e}")
        wait_for_user_exit()
        return None
