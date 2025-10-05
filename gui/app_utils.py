import logging
import subprocess
import os
import re
import html
import glob
import platform
import webbrowser
import shutil
from functools import cache
from pathlib import Path
from typing import NamedTuple
from PyQt5.QtCore import QDir, QFileInfo, QSize
from PyQt5.QtGui import QColor, QFont, QIcon, QPainter
from PyQt5.QtWidgets import QFileIconProvider

from ovl_util.config import Config

import vdf

# Windows modules
try:
    import winreg
    WINDOWS = True
except:
    logging.warning("Required Windows modules missing; some features may not work.")
    WINDOWS = False

ROOT_DIR = Path(__file__).resolve().parent.parent
ICON_CACHE = {"no_icon": QIcon()}
USERPROFILE = os.environ.get("USERPROFILE", "")


# -------------------------------------------------------------------------- #
#                                ICON UTILS                                  #
# region ------------------------------------------------------------------- #

class CacheInfo(NamedTuple):
    filename: str
    resource_path: str
    abs_filepath: str


def color_icon(icon: QIcon, color: str = "#FFF", size: QSize = QSize(16, 16)) -> QIcon:
    img = icon.pixmap(size)
    qp = QPainter(img)
    qp.setCompositionMode(QPainter.CompositionMode_SourceIn)
    qp.fillRect(img.rect(), QColor(color))
    qp.end()
    return QIcon(img)


def get_icon(name: str, color: str = "", size: QSize = QSize(16, 16)) -> QIcon:
    icon = name + color
    if icon in ICON_CACHE:
        return ICON_CACHE[icon]
    for ext in (".svg", ".png"):
        fp = ROOT_DIR / f'icons/{name}{ext}'
        if fp.is_file():
            ICON_CACHE[icon] = QIcon(str(fp)) if not color else color_icon(QIcon(str(fp)), color=color, size=size)
            return ICON_CACHE[icon]
    return ICON_CACHE["no_icon"]


def get_exe_from_ovldata(ovldata_path: str) -> str:
    game_dir = Path(ovldata_path).parent.parent
    if os.path.isdir(game_dir):
        exes = [exe for exe in os.listdir(game_dir) if
                exe.lower().endswith(".exe") and exe.lower() not in ("crash_reporter.exe",)]
        if exes:
            return os.path.join(game_dir, exes[0])
        logging.debug("EXE not found in manually added game folder")
    else:
        logging.debug(f"Game folder {game_dir} does not exist")
    return ""


def get_icon_cache_info(filename: str, icon_size: int) -> CacheInfo:
    safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_')).rstrip()
    resource_path = f"cache/{safe_filename}_{icon_size}"
    abs_filepath = ROOT_DIR / f"icons/{resource_path}.png"
    return CacheInfo(safe_filename, resource_path, str(abs_filepath))


def cache_icon(icon: QIcon, filename: str, icon_size: int):
    """Saves a given QIcon to the cache directory as a PNG."""
    QDir().mkpath(f"{ROOT_DIR}/icons/cache")
    try:
        cache_info = get_icon_cache_info(filename, icon_size)
        pixmap = icon.pixmap(icon_size, icon_size)
        if not pixmap.isNull():
            # Save the pixmap to the absolute path.
            pixmap.save(cache_info.abs_filepath)
    except Exception:
        # Caching failed, but we can still use the icon for this session.
        # Add logging here if desired.
        pass


def get_exe_icon(filename: str, exe_path: str, icon_size: int) -> QIcon:
    """
    Gets an EXE's icon, first checking the cache, then falling back to the exe.
    Caches the icon if it's retrieved from the exe.
    """
    if not filename or not exe_path:
        return get_icon("dir")

    cache_info = get_icon_cache_info(filename, icon_size)
    # Check if the cached file already exists.
    if Path(cache_info.abs_filepath).exists():
        try:
            # If it exists, load it directly and skip the rest of the logic
            icon = get_icon(cache_info.resource_path, size=QSize(icon_size, icon_size))
            if not icon.isNull():
                return icon
        except Exception:
            # Fall through to the original exe lookup logic
            pass

    # If cache doesn't exist (or failed), perform the original exe lookup.
    try:
        provider = QFileIconProvider()
        info = QFileInfo(exe_path)
        icon = QIcon(provider.icon(info))

        # Cache the newly found icon for next time.
        if not icon.isNull():
            cache_icon(icon, filename, icon_size)

        return icon
    except Exception:
        # If all else fails, return a null icon.
        return QIcon()

# endregion

# -------------------------------------------------------------------------- #
#                                FONT UTILS                                  #
# region ------------------------------------------------------------------- #

@cache
def get_font(family: str, point_size: int = -1, pixel_size: int = -1,
        italic: bool = False, bold: bool = False,
        weight: QFont.Weight = QFont.Weight.Normal
    ) -> QFont:
    """
    Creates a QFont instance, ensuring antialiasing and kerning.
    """
    font = QFont()
    font.setFamily(family)  # Set your desired family
    if point_size != -1:
        font.setPointSize(point_size)
    if pixel_size != -1:
        font.setPixelSize(pixel_size)
    if bold:
        font.setBold(True)
    else:
        font.setWeight(weight)
    font.setItalic(italic)
    font.setKerning(True)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
    font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    #font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 100.0)  # Default is 100%
    #font.setWordSpacing(QFont.SpacingType.PercentageSpacing, 100.0)    # Default is 100%

    # Sanity check if Qt actually found and is using your desired font family
    if font.family().lower() != family.lower() and family.lower() not in font.family().lower().split(","):
        logging.warning(
            f"Requested font family '{family}' was not fully resolved by QFont. "
            f"QFont is actually using '{font.family()}'. "
            "Ensure the custom font was loaded correctly via QFontDatabase.addApplicationFont()."
        )

    return font

# endregion

# -------------------------------------------------------------------------- #
#                                TEXT UTILS                                  #
# region ------------------------------------------------------------------- #

def truncate_tooltip(text: str, character_index: int=5000, line_count: int=100) -> str:
    """
    Truncates a string based on character index or line count, whichever comes first
    """

    def find_nth_occurrence(text_block: str, substring: str, n: int) -> int:
        """Finds the starting index of the nth occurrence of a substring"""
        start = text_block.find(substring)
        while start >= 0 and n > 1:
            start = text_block.find(substring, start + 1)
            n -= 1
        return start

    truncation_indices = []
    # Find the nth newline
    line_limit_index = find_nth_occurrence(text, '\n', line_count)
    if line_limit_index != -1:
        truncation_indices.append(line_limit_index)
    # Find the first newline after character_index
    char_limit_index = text.find('\n', character_index)
    if char_limit_index != -1:
        truncation_indices.append(char_limit_index)

    if not truncation_indices:
        return text

    final_trunc_index = min(truncation_indices)
    return text[:final_trunc_index] + "\n..."


def url_to_html(raw_line: str) -> str:
    """
    Escapes a line of text and wraps any http/https links in HTML <a> tags.
    """
    # A regex pattern to find URLs.
    url_pattern = re.compile(r'(https?://[^\s<>"]+)')

    # Split the line by the URL pattern. This gives a list of alternating
    # text and URL strings. e.g., ['text1', 'url1', 'text2', 'url2', ...]
    parts = url_pattern.split(raw_line)
    processed_parts = []
    for i, part in enumerate(parts):
        if not part:
            continue
        # The URLs will be at the odd-numbered indices in the 'parts' list.
        if i % 2 == 1:
            # This part is a URL
            escaped_url = html.escape(part)
            processed_parts.append(f'<a href="{escaped_url}">{escaped_url}</a>')
        else:
            # This part is plain text
            processed_parts.append(html.escape(part))

    return "".join(processed_parts)

#endregion

# -------------------------------------------------------------------------- #
#                                  STEAM                                     #
# region ------------------------------------------------------------------- #

def get_steam_games(games_list: list[str]) -> dict[str, str]:
    if WINDOWS:
        # get steam folder from windows registry
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Valve\\Steam")
        steam_query = winreg.QueryValueEx(hkey, "InstallPath")
        # get path to steam games folder
        # C:\\Program Files (x86)\\Steam
        steam_path = steam_query[0]
        library_folders = {steam_path}
        vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
        # check if there are other steam library folders (e.g. on external drives)
        try:
            with open(vdf_path) as vdf_reader:
                v = vdf.load(vdf_reader)
                for folder in v["libraryfolders"].values():
                    library_folders.add(folder["path"])
        except:
            logging.warning(
                f"vdf not installed, can not detect steam games on external drives - run `pip install vdf`")

        # map all installed fdev game names to their ovldata folder
        fdev_games = {}
        # list all games for each library folder
        for steam_path in library_folders:
            apps_path = os.path.join(steam_path, "steamapps", "common")
            if os.path.isdir(apps_path):
                # filter with supported fdev games
                fdev_in_lib = [game for game in os.listdir(apps_path) if game in games_list]
                # generate the whole path for each game, add to dict
                # C:\Program Files (x86)\Steam\steamapps\common\Planet Zoo\win64\ovldata
                fdev_games.update({game: os.path.join(apps_path, game, "win64", "ovldata") for game in fdev_in_lib})

        logging.info(f"Found {len(fdev_games)} Cobra games from Steam")
        return fdev_games

    logging.warning(f"Can only get games from Steam on Windows")
    return {}

# endregion

# -------------------------------------------------------------------------- #
#                               LAUNCH GAME                                  #
# region ------------------------------------------------------------------- #

def launch_game(game: str, cfg: Config):
    logging.info(f"Running {game}")
    args = ["-nointro", ]
    if game == "Jurassic World Evolution 2":
        args.extend(["-disableprint", "-level", "modelviewer"])  # only works on JWE2, crashes PC, PZ
    # try steam launch
    id_map = {
        "Jurassic World Evolution 2": 1244460,
        "Jurassic World Evolution": 648350,
        "Planet Coaster 2": 2688950,
        "Planet Coaster": 493340,
        "Planet Zoo": 703080,
        "Disneyland Adventures": 630610,
        "Zoo Tycoon": 613880,
        }
    steam_game_id = id_map.get(game)
    if steam_game_id:
        args_str = " ".join(args)
        steam_cmd = f"steam://rungameid/{steam_game_id}//{args_str}"
        logging.debug(f"Running game from {steam_cmd}")
        webbrowser.open(steam_cmd)
    else:
        ovldata = cfg["games"].get(game, None)
        exe_path = get_exe_from_ovldata(ovldata)
        if exe_path:
            subprocess.Popen([exe_path, ] + args)
        else:
            logging.warning(f"Couldn't find the game's executable")

# endregion

# -------------------------------------------------------------------------- #
#                              LAUNCH EDITOR                                 #
# region ------------------------------------------------------------------- #

# macOS & Linux
vscode_exes = ["code"]
pycharm_exes = ["pycharm.sh", "pycharm"]

if platform.system() == "Windows":
    vscode_exes = ["code.cmd", "code"]
    pycharm_exes = ["pycharm64.exe", "pycharm.exe", "pycharm"]

EDITOR_CONFIGS = {
    "VS Code": {
        "type": "vscode",
        "exe_names": vscode_exes,
        "install_paths": [
            # User Install
            os.path.join(USERPROFILE, R"AppData\Local\Programs\Microsoft VS Code\bin") if USERPROFILE else None,
            # System Install
            R"C:\Program Files\Microsoft VS Code\bin",
        ]
    },
    "PyCharm": {
        "type": "pycharm",
        "exe_names": pycharm_exes,
        "install_paths": [
            R"C:\Program Files\JetBrains\PyCharm *\bin",  # Unified e.g. 2025.1.1, 2025.2.1
            R"C:\Program Files\JetBrains\PyCharm\bin",    # Non-Unified
            R"C:\Program Files\JetBrains\PyCharm Community Edition\bin", 
            R"C:\Program Files\JetBrains\PyCharm Professional Edition\bin",
        ]
    }
}

def launch_editor(editor_config, file_location, target_line_number) -> bool:
    """Launch editor for a text file, with optional line number target"""
    exe_names_to_try = editor_config.get("exe_names", [])
    command_to_run = None
    # The primary method is to find the executable on the system's PATH.
    for exe_name in exe_names_to_try:
        resolved_path = shutil.which(str(exe_name))
        if resolved_path:
            command_to_run = resolved_path
            break

    # If not found on PATH and the OS is Windows, try the hardcoded paths.
    if not command_to_run and platform.system() == "Windows":
        install_paths = editor_config.get("install_paths", [])
        for exe_name in exe_names_to_try:
            # First check explicit install paths
            for path_pattern in install_paths:
                dirs_to_check = []
                if "*" in path_pattern:
                    matches = glob.glob(path_pattern)
                    if matches:
                        # Last item is probably the highest version
                        matches.sort()  
                        dirs_to_check.append(matches[-1])
                else:
                    dirs_to_check.append(path_pattern)  # Use the path as is

                for install_path_dir in dirs_to_check:
                    potential_path = os.path.join(install_path_dir, exe_name)
                    if os.path.exists(potential_path):
                        command_to_run = potential_path
                        break
            if command_to_run:
                break

    editor_name = editor_config["type"]
    if not command_to_run:
        logging.info(f"Could not find {editor_name}. Please ensure it's in your PATH.")
        return False

    # Normalize the filepath for the current OS
    system_specific_filepath = os.path.normpath(file_location)
    command = []
    if editor_config["type"] == "vscode":
        vscode_goto_arg = f"{system_specific_filepath}:{target_line_number}"
        command = [command_to_run, "--goto", vscode_goto_arg]
    elif editor_config["type"] == "pycharm":
        command = [command_to_run]
        if target_line_number and target_line_number.isdigit():
            command.extend(["--line", target_line_number])
        command.append(system_specific_filepath)

    #logging.debug(f"Attempting to execute for {editor_name}: {command}")
    try:
        subprocess.Popen(command)
        #logging.debug(f"{editor_name} launch command sent.")
        return True
    except Exception as e:
        logging.info(f"Error launching {editor_name} ('{command_to_run}'): {e}.")
    
    return False

# endregion
