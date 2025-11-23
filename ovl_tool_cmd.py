#!/usr/bin/env python
"""
ovl_tool_cmd.py

Command-line OVL tool using the same OvlFile API as ovl_tool_gui.

Subcommands:

  new      - create a new OVL from a folder
  extract  - extract files from an OVL
  inject   - inject/replace files into an OVL

Examples:

  ovl_tool_cmd.py extract -i path/to/main.ovl 
  ovl_tool_cmd.py new -i this/folder/ -g "Planet Zoo" -o Main.ovl
  ovl_tool_cmd.py inject -f test/test.lua  -g "Jurassic World Evolution 3" --in-place path/to/main.ovl


"""

from __future__ import annotations

from utils.logs import logging_setup # type: ignore
import logging
logging_setup("ovl_tool_cmd")

import argparse
import os
import sys
from typing import Iterable, List, Optional

# -----------------------------------------------------------------------------
# Bootstrapping: repo root, shared formats, logging shim
# -----------------------------------------------------------------------------

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import contextlib
from modules.formats.shared import DummyReporter 

class BuildReporter(DummyReporter):
    def __init__(self):
        self.warnings = []
        self.errors = []
        self.error_files = []

    def show_warning(self, msg: str):
        self.warnings.append(msg)

    def show_error(self, exception: Exception):
        self.errors.append(exception)

    def iter_progress(self, iterable, message, cond=True):
        for item in iterable:
            yield item

    @contextlib.contextmanager
    def report_error_files(self, operation):
        yield self.error_files
  

from generated.formats.ovl import games, OvlFile
from generated.formats.ovl_base.enums.Compression import Compression
from utils.config import Config

# In the GUI, logging.success is provided by their logging wrapper; here we alias
if not hasattr(logging, "success"):
    def success(msg, *args, **kwargs):
        logging.getLogger("cobra-tools").info(msg, *args, **kwargs)
    logging.success = success  # type: ignore[attr-defined]

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s",
)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def ensure_exists(path: str, kind: str = "file") -> None:
    if kind == "file" and not os.path.isfile(path):
        die(f"{kind.capitalize()} does not exist: {path}")
    if kind == "dir" and not os.path.isdir(path):
        die(f"{kind.capitalize()} does not exist: {path}")


def find_common_root(files: Iterable[str]) -> str:
    paths = [os.path.abspath(p) for p in files]
    if not paths:
        return ""
    if len(paths) == 1:
        return os.path.dirname(paths[0])
    return os.path.commonpath(paths)


def resolve_game_label(label: Optional[str]) -> Optional[str]:
    """
    Convert a user-facing game label to the same value the GUI uses.

    The combo box in the GUI is built from [g.value for g in games], and
    game_changed() sets ovl_data.game to that value, so we mirror that.
    """
    if not label:
        return None
    for g in games:
        if label == getattr(g, "value", None) or label == getattr(g, "name", None):
            return g.value
    return label


def game_choices() -> List[str]:
    try:
        return [g.value for g in games]
    except Exception:
        return []


def compression_choices() -> List[str]:
    return [c.name for c in Compression]


# -----------------------------------------------------------------------------
# Core operations using OvlFile (no custom reporter, just like your working extract)
# -----------------------------------------------------------------------------

def cmd_new(args: argparse.Namespace) -> None:
    """
    File > New (from folder): create an OVL from a directory and save it.

    Mirrors MainWindow.create_ovl + save in ovl_tool_gui:
        self.ovl_data.clear()
        self.game_changed()
        self.ovl_data.create(ovl_dir)
        self.ovl_data.save(filepath, commands={"update_aux": cfg["update_aux"]})
    """
    in_dir = os.path.abspath(args.input)
    out_ovl = os.path.abspath(args.output)

    ensure_exists(in_dir, "dir")
    if os.path.exists(out_ovl) and not args.force:
        die(f"Output file already exists: {out_ovl} (use --force to overwrite)")

    game = resolve_game_label(args.game)
    if not game:
        die("You must specify --game for 'new'.")

    ovl = OvlFile()
    ovl.game = game  # same as game_changed() ultimately does
    ovl.load_hash_table()

    if args.compression:
        try:
            ovl.user_version.compression = Compression[args.compression]
        except KeyError:
            die(f"Unknown compression '{args.compression}'. Valid: {', '.join(compression_choices())}")

    logging.info("Creating OVL from %s", in_dir)
    logging.info("Game: %s", ovl.game)

    try:
        ovl.clear()    
        ovl.create(in_dir)
    except Exception as e:
        die(f"OvlFile.create failed: {e!r}")

    commands = {"update_aux": args.update_aux}
    try:
        ovl.save(out_ovl, commands=commands)
    except Exception as e:
        die(f"OvlFile.save failed: {e!r}")

    logging.success("Created OVL: %s", out_ovl)


def cmd_extract(args: argparse.Namespace) -> None:
    """
    Extract from an OVL.

    GUI equivalents:
      - MainWindow._extract_all -> ovl.extract(out_dir, only_types=only_types)
      - drag_files -> ovl.extract(temp_dir, only_names=file_names)
    """
    ovl_path = os.path.abspath(args.ovl)
    ensure_exists(ovl_path, "file")

    if args.output:
        out_dir = os.path.abspath(args.output)
    else:
        # Default: <same_dir>/<ovl_basename_without_ext>
        ovl_dir = os.path.dirname(ovl_path)
        ovl_name = os.path.splitext(os.path.basename(ovl_path))[0]
        out_dir = os.path.join(ovl_dir, ovl_name)

    os.makedirs(out_dir, exist_ok=True)

    ovl = OvlFile()

    # Optional override: if user passes -g, we force that game
    game = resolve_game_label(args.game)
    commands = {}
    if game:
        commands["game"] = game
        logging.info("Using game preset: %s", game)
    else:
        logging.info("No game preset supplied; OvlFile will auto-detect.")
    logging.info("Loading archive %s", ovl_path)

    try:
        ovl.load(ovl_path, commands)
        logging.info("Detected game from archive: %s", getattr(ovl, "game", "<unknown>"))
    except Exception as e:
        die(f"OvlFile.load failed: {e!r}")

    only_types = args.type or None
    only_names = args.name or None

    logging.info("Extracting to %s", out_dir)
    if only_types:
        logging.info("Only types: %s", ", ".join(only_types))
    if only_names:
        logging.info("Only names: %s", ", ".join(only_names))

    kwargs = {}
    if only_types:
        kwargs["only_types"] = only_types
    if only_names:
        kwargs["only_names"] = only_names

    try:
        ovl.extract(out_dir, **kwargs)
    except Exception as e:
        die(f"OvlFile.extract failed: {e!r}")

    logging.success("Extracted OVL to %s", out_dir)


def cmd_inject(args: argparse.Namespace) -> None:
    """
    Inject files into an OVL, using OvlFile.add_files(files, common_root_dir)
    (same pattern as MainWindow.inject_files in the GUI).
    """
    ovl_src = os.path.abspath(args.ovl)
    ensure_exists(ovl_src, "file")


    game = resolve_game_label(args.game)
    commands = {}
    if game:
        commands["game"] = game
        logging.info("Using game preset: %s", game)
    else:
        logging.info("No game preset supplied; OvlFile will auto-detect.")

    ovl = OvlFile()
    ovl.game = game
    ovl.load_hash_table()

    logging.info("Loading archive %s", ovl_src)

    try:
        ovl.clear()
        ovl.load(ovl_src, commands)
    except Exception as e:
        die(f"OvlFile.load failed: {e!r}")

    try:
        logging.info("Detected game from archive: %s", getattr(ovl, "game", "<unknown>"))
    except Exception:
        pass


    # Collect files to inject
    files_to_inject: List[str] = []

    if args.input:
        in_dir = os.path.abspath(args.input)
        ensure_exists(in_dir, "dir")
        for root, _, files in os.walk(in_dir):
            for name in files:
                files_to_inject.append(os.path.join(root, name))

    if args.file:
        for p in args.file:
            files_to_inject.append(os.path.abspath(p))

    if not files_to_inject:
        die("No files to inject (use --input folder and/or --file path).")

    files_to_inject = sorted(set(files_to_inject))

    # Choose a common root like the GUI does for relative names
    if args.input:
        common_root = os.path.abspath(args.input)
    else:
        common_root = find_common_root(files_to_inject)
        if not common_root:
            die("Could not determine common root directory for injected files.")

    logging.info("Injecting %d files (root: %s)", len(files_to_inject), common_root)

    try:
        ovl.add_files(files_to_inject, common_root)
    except Exception as e:
        die(f"OvlFile.add_files failed: {e!r}")

    # Decide output path
    if args.in_place:
        out_ovl = ovl_src
    else:
        if not args.output:
            die("You must specify --output when not using --in-place.")
        out_ovl = os.path.abspath(args.output)

    commands_save = {"update_aux": args.update_aux}

    logging.info("Saving archive to %s", out_ovl)
    try:
        ovl.save(out_ovl, commands=commands_save)
    except Exception as e:
        die(f"OvlFile.save failed: {e!r}")

    logging.success("Injected files into %s", out_ovl)


# -----------------------------------------------------------------------------
# Argument parsing
# -----------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Command-line OVL tool using cobra-tools' OvlFile."
    )

    sub = parser.add_subparsers(dest="command", required=True)

    game_vals = game_choices()
    comp_vals = compression_choices()

    # new
    p_new = sub.add_parser(
        "new",
        help="Create a new OVL from a folder (File > New from folder).",
    )
    p_new.add_argument(
        "-g", "--game",
        help="Game identifier (matches GUI 'Game' dropdown).",
        choices=game_vals if game_vals else None,
        required=True,
    )
    p_new.add_argument(
        "-i", "--input",
        help="Input folder containing files to pack into the OVL.",
        required=True,
    )
    p_new.add_argument(
        "-o", "--output",
        help="Output .ovl file path.",
        required=True,
    )
    p_new.add_argument(
        "-c", "--compression",
        help="Compression method (matches GUI 'Compression').",
        choices=comp_vals if comp_vals else None,
    )
    p_new.add_argument(
        "--update-aux",
        action="store_true",
        help="Set commands['update_aux']=True when saving.",
    )
    p_new.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )
    p_new.set_defaults(func=cmd_new)

    # extract
    p_ext = sub.add_parser(
        "extract",
        help="Extract files from an OVL.",
    )
    p_ext.add_argument(
        "ovl",
        help="Path to the .ovl file to extract.",
    )
    p_ext.add_argument(
        "-o", "--output",
        help=(
            "Output folder (created if missing). "
            "If omitted, a folder named after the OVL file will be created "
            "next to the OVL (e.g. Main.ovl -> Main/)."
        )
    ),
    p_ext.add_argument(
        "-g", "--game",
        help="Game identifier (optional; if omitted, OvlFile may auto-detect).",
        choices=game_vals if game_vals else None,
    )
    p_ext.add_argument(
        "--type",
        action="append",
        default=[],
        help="Restrict extraction to specific file types/extensions (can repeat).",
    )
    p_ext.add_argument(
        "--name",
        action="append",
        default=[],
        help="Restrict extraction to specific internal entry names (can repeat).",
    )
    p_ext.set_defaults(func=cmd_extract)

    # inject
    p_inj = sub.add_parser(
        "inject",
        help="Inject/replace files into an OVL.",
    )
    p_inj.add_argument(
        "ovl",
        help="Path to the .ovl file to modify.",
    )
    p_inj.add_argument(
        "-g", "--game",
        help="Game identifier (matches GUI 'Game' dropdown).",
        choices=game_vals if game_vals else None,
        required=True,
    )
    p_inj.add_argument(
        "-i", "--input",
        help="Folder whose contents will be injected (recursively).",
    )
    p_inj.add_argument(
        "-f", "--file",
        action="append",
        default=[],
        help="Individual file path(s) to inject. Can be repeated.",
    )
    p_inj.add_argument(
        "--in-place",
        action="store_true",
        help="Modify the OVL in place (overwrite the input file).",
    )
    p_inj.add_argument(
        "-o", "--output",
        help="Output .ovl file path (required unless --in-place).",
    )
    p_inj.add_argument(
        "--update-aux",
        action="store_true",
        help="Set commands['update_aux']=True when saving.",
    )
    p_inj.set_defaults(func=cmd_inject)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
