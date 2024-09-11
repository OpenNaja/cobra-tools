#!/usr/bin/env python
import subprocess
from __version__ import VERSION


def main():
    last_commit = subprocess.check_output(["git", "log", r"--pretty=format:%h - %cd", "-1"], text=True)
    commit_hash, commit_time = last_commit.split(" - ")
    version_file = "__version__.py"
    with open(version_file, "w") as file:
        file.writelines([
            f'VERSION = "{VERSION}"\n',
            f'COMMIT_HASH = "{commit_hash}"\n',
            f'COMMIT_TIME = "{commit_time}"\n',
        ])
    return subprocess.run(["git", "add", version_file]).returncode


if __name__ == "__main__":
    SystemExit(main())
