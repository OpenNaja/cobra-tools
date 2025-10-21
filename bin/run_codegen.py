#!/usr/bin/env python
import os
import subprocess


def get_env():
    # Attempt to get the venv python
    venv = os.path.normpath(os.environ.get("VIRTUAL_ENV", ""))
    if venv != ".":
        for py in [rf"{venv}\Scripts\python.exe", rf"{venv}/bin/python", rf"{venv}/Bin/python"]:
            if os.path.exists(py):
                return py
    return "python"


def generated_files(changed: str):
    """Returns strings for use with `git add` based on source files being committed"""
    files = changed.splitlines()
    generated = set()
    for file in files:
        if file.startswith("source/formats"):
            # `git add` each formats dir for source in changed
            dirs = ['generated'] + file.split("/")[1:3]
            generated.add("/".join(dirs))
        elif file.startswith("source/"):
            # `git add` root files if source in changed
            generated.add(file.replace("source/", "generated/"))
    return generated


def main():
    return 0  # Temporary
    # The files in the current commit
    changed = subprocess.check_output(["git", "diff", "--name-only", "--cached", "--ignore-cr-at-eol"], text=True)
    if len(changed) == 0:
        return 0
    # Run codegen
    result = subprocess.run([get_env(), "-m", "codegen", "--silent"]).returncode
    if result == 0:
        # Run `git add` for generated paths corresponding to source paths in commit
        for file in generated_files(changed):
            result = subprocess.run(f"git add {file}").returncode
            if result:
                return result
    return result


if __name__ == '__main__':
    SystemExit(main())
