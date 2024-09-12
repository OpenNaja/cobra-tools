#!/usr/bin/env python
import subprocess
from __version__ import VERSION


def should_increment():
    TRACKED_FOLDERS = [
        "codegen",
        "constants",
        "generated",
        "source",
        "modules",
        "ovl_util",
        "dumps",
        "sql_commands",
        "gui",
        "plugin",
    ]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", "--cached"], text=True
    )
    for path in changed.splitlines():
        path = path.split("/")
        if path[0] in TRACKED_FOLDERS:
            return True
        elif len(path) == 1 and path[0].endswith(".py"):
            return True


def main():
    if should_increment():
        last_commit = subprocess.check_output(
            ["git", "log", r"--pretty=format:%h - %cd", "-1"], text=True
        )
        commit_hash, commit_time = last_commit.split(" - ")
        version_file = "__version__.py"
        with open(version_file, "w") as file:
            file.writelines(
                [
                    f'VERSION = "{VERSION}"\n',
                    f'COMMIT_HASH = "{commit_hash}"\n',
                    f'COMMIT_TIME = "{commit_time}"\n',
                ]
            )
        return subprocess.run(["git", "add", version_file]).returncode


if __name__ == "__main__":
    SystemExit(main())
