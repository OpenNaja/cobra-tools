# Download

## Installation

**Read the instructions steps carefully and do not jump ahead and start downloading everything or you will miss important steps**.

[Download :material-download:](https://github.com/OpenNaja/cobra-tools/archive/master.zip){ .md-button .md-button--download }

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


### Installing Python Dependencies

Opening any of the GUI tools after installing Python 3.11 and the redistributables will auto-install the Python dependencies for you. You may also be prompted to update outdated packages.

![Auto Updater](assets/images/auto_updater.png)

Simply follow the instructions, typing `y` and hitting `Enter`.

---

### Installing Dependencies Manually

If you would like to install the dependencies manually:

1. Open the Cobra Tools folder in Windows File Explorer.
2. In the File Explorer address bar, type `cmd` and hit `Enter`. This will open a command prompt in your Cobra Tools folder.
3. In the command prompt type the following line and hit `Enter`

    ```
    python.exe -m pip install --upgrade pip && pip install -r requirements.txt
    ```
    !!! tip "IMPORTANT"
        If you do not open `cmd` in your Cobra Tools folder, you will need to provide the full path to `requirements.txt`

## Troubleshooting Errors

If you still encounter errors after following these instructions, please visit our [Tools FAQ](Tools-FAQ/index.md).
