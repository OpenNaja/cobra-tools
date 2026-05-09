"""Path-handling tests covering separators that historically assumed Windows."""

import os
import posixpath

from codegen.path_utils import module_path_to_import_path, to_import_path
from utils.logs import shorten_str, shorten_paths


def test_shorten_str_normalises_backslash_paths():
	"""shorten_str must replace registered prefixes whether the input uses / or \\."""
	# Pick a registered prefix to verify against (root_dir is always present).
	prefix, replacement = next(iter(shorten_paths.items()))
	posix_input = f"{prefix.replace(os.sep, '/')}/foo/bar.py"
	win_input = f"{prefix.replace(os.sep, chr(92))}{chr(92)}foo{chr(92)}bar.py"

	assert replacement in shorten_str(posix_input)
	assert replacement in shorten_str(win_input)


def test_shorten_str_passthrough_for_unmatched_input():
	msg = "/some/path/that/is/not/registered.txt"
	assert shorten_str(msg) == msg


def test_to_import_path_returns_basename():
	"""to_import_path returns the basename of the supplied folder."""
	assert to_import_path(os.path.join("foo", "bar", "baz")) == "baz"


def test_module_path_to_import_path_dotted():
	"""Module paths must be converted to dotted Python imports regardless of OS separator."""
	module_path = os.path.join("foo", "bar", "baz")
	assert module_path_to_import_path(module_path, "generated") == "generated.foo.bar.baz"


def test_archive_relpath_uses_forward_slash():
	"""OVL archives store internal paths with forward slashes regardless of host OS;
	the current normalisation pattern (.replace('\\\\', '/')) is a no-op on POSIX
	and a separator-flip on Windows. Both must produce a forward-slash path."""
	common_root = os.path.normpath("/tmp/root") if os.name != "nt" else r"C:\tmp\root"
	file_path = os.path.join(common_root, "sub", "file.bin")
	rel = os.path.relpath(file_path, common_root).replace("\\", "/")
	assert rel == posixpath.join("sub", "file.bin")
	assert "\\" not in rel
