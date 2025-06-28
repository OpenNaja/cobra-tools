"""
    Deals with missing packages and tries to install them from the tool itself.
"""

import os.path
import re
import sys
import time
import logging
import subprocess

from ovl_util.logs import ANSI

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# temporarily set to make sure it shows up, even though it is not written to the log file
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug(f"Checking for automatic module updates")


def install_prompt(question) -> bool:
    """ask question and return True if user confirms"""
    print(f"{ANSI.LIGHT_WHITE}{question}{ANSI.END} (y/N)")
    print(f"{ANSI.LIGHT_YELLOW}[Type y and hit Enter]{ANSI.END}{ANSI.LIGHT_GREEN}")
    if input().lower() in {'yes', 'y', 'ye'}:
        return True
    else:
        return False


def pip_install(package_name) -> int:
    """use pip to install a package"""
    logging.info(f"Installing {package_name}")
    return subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def pip_upgrade(package_name) -> int:
    """use pip to install --update a package"""
    logging.info(f"Updating {package_name}")
    return subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])


if (sys.version_info.major, sys.version_info.minor) < (3, 11):
    logging.critical(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}. Install Python 3.11+ and try again.")
    time.sleep(60)
try:
    # pkg_resources is available on py <= 3.11
    from pkg_resources import packaging  # type: ignore
except:
    logging.warning(f"pkg_resources is not available, can't upgrade dependencies")
    packaging = None
try:
    from importlib import import_module
    # importlib.metadata is available on py >= 3.8
    from importlib.metadata import distribution, PackageNotFoundError, packages_distributions
    import tomllib

    MISSING: dict[str, str] = {}
    OUTDATED: dict[str, str] = {}
    INSTALLED: list[str] = []
    UPDATED: list[str] = []
    MODULES: list[str] = []

    pyproject_path = os.path.join(root_dir, "pyproject.toml")
    with open(pyproject_path, 'rb') as fproj:
        pyproject = tomllib.load(fproj)
        project = pyproject.get('project', {})
        deps = project.get('dependencies', {})
        deps_gui = project.get('optional-dependencies', {}).get('gui', [])
        pkg_dist = packages_distributions()
        for line in deps + deps_gui:
            lib, op, version = re.split("(~=|==|>=|<=|>|<)", line)
            # Get import name from package name to verify it can be imported
            for module, pkgs in pkg_dist.items():
                if lib in pkgs:
                    MODULES.append(module)
            # check if module is installed
            try:
                lib_dist = distribution(lib)
            except PackageNotFoundError:
                logging.warning(f"{lib} is not installed.")
                MISSING[lib] = line  # Need full line including ~= for pip install command
                continue
            # compare installed version to required version
            if packaging is not None:
                if packaging.version.parse(lib_dist.metadata['Version']) < packaging.version.parse(version):
                    logging.warning(f"{lib} is out of date.")
                    OUTDATED[lib] = line  # Need full line including ~= for pip install command

    if MISSING and install_prompt("Install the missing dependencies?"):
        # upgrade pip then try installing the rest of packages
        pip_upgrade('pip')
        for key, package in MISSING.items():
            if pip_install(package) == 0:
                INSTALLED.append(key)

    if OUTDATED and install_prompt("Update the outdated dependencies?"):
        # upgrade pip then try updating the outdated packages
        pip_upgrade('pip')
        for key, package in OUTDATED.items():
            if pip_upgrade(package) == 0:
                UPDATED.append(key)

    if hasattr(logging, "success"):
        if INSTALLED:
            logging.success(f"Installed: {INSTALLED}")

        if UPDATED:
            logging.success(f"Updated: {UPDATED}")

    # verify that all found modules can be imported
    try:
        for module in MODULES:
            import_module(module)
    except:
        logging.exception("Some modules could not be imported; install the required dependencies with pip!")
        time.sleep(15)
except:
    logging.exception("auto_updater didn't work")
    time.sleep(15)
