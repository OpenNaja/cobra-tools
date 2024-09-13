---
title: Download
description: Download and installation information including prerequisites
icon: material/download
---

# Download

## Installation

!!! warning

    1. Read the instructions steps carefully before downloading anything or you will miss important steps.
    2. If updating the tools, please also refer to [Updating](Updating.md).

### Installing Prerequisites

You need to have installed:  

- [Python 3.11 64-bit](https://www.python.org/downloads/windows/){:target="_blank"} 

    !!! danger "IMPORTANT" 
        - **Make sure you select the option "Add Python to PATH" during installation**
        - 32-bit versions of Python are not recommended.

<div class="annotate" markdown>
- [Microsoft Visual C++ Redistributable 2017 x64](https://aka.ms/vs/15/release/vc_redist.x64.exe){:target="_blank"} (1)
- [Microsoft Visual C++ Redistributable 2013 x86](https://aka.ms/highdpimfc2013x86enu){:target="_blank"} (2)
</div>
1. Required for texture conversion
2. Required for Lua decompilation

### Download

??? download interactive "Download & Terms of Conduct"

    --8<-- "terms-of-conduct.md"

### Installing Python Dependencies

Opening any of the GUI tools after installing Python 3.11 and the redistributables should auto-install the Python dependencies for you. You may also be prompted to update outdated packages via this same prompt. If you have issues please see [Installing Dependencies Manually](#installing-dependencies-manually).

![Auto Updater](./assets/images/auto_updater.png)

Simply follow the instructions, typing `y` and hitting `Enter`.

---

### Installing Dependencies Manually

If you would like to install the dependencies manually:

1. Open the Cobra Tools folder in Windows File Explorer.
2. In the File Explorer address bar, type `cmd` and hit `Enter`. This will open a command prompt in your Cobra Tools folder.
3. In the command prompt type the following line and hit `Enter`

    ```
    python.exe -m pip install --upgrade pip && pip install .[gui]
    ```
    !!! tip "IMPORTANT"
        There is a dot `.` at the end of the command `.[gui]`.
        If you do not open `cmd` in your Cobra Tools folder, you will need to replace `.` with the full path to the folder.

## Troubleshooting Errors

If you still encounter errors after following these instructions, please visit our [Tools FAQ](Tools-FAQ/index.md).
