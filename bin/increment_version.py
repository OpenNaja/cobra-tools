#!/usr/bin/env python
import subprocess
import sys


def main():
    version = subprocess.check_output(["git", "log", r"--pretty=format:%h - %cd", "-1"], text=True)
    with open("version.txt", "w") as file:
        file.write(version)
    return subprocess.run(["git", "add", "version.txt"]).returncode


if __name__ == '__main__':
    exit(main())
