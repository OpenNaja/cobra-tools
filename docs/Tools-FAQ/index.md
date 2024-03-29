---
title: Tools FAQ
description: FAQ for common issues and questions regarding the GUI tools and Blender Plugin
icon: material/frequently-asked-questions
---

# Tools FAQ

!!! construction
    This page is currently under construction!

For game-specific issues, please see [Modding FAQ](../Modding-FAQ/index.md)

!!! faq "Where is the latest release?"
    [Download :material-download:](../Download.md){ .md-button .md-button--download }

!!! faq "I do not know where the log file is."
    - For Blender, the file is located in

        --8<-- "blender-log.md"

    - For OVL Tool, FGM Editor, MS2 Tool, Mod Tool, the log file is located next to the .py you open the tool with, with the same name.

!!! faq "The tools immediately close after opening."
    1. Ensure you have at least Python 3.11
    2. Ensure you have all Python dependencies.
    3. Do not run the tools from the ZIP file. Extract the folder instead.
    4. If you have multiple version of Python installed, consider removing the other ones (if possible), or associate the cobra-tools .py files with the correct version of Python.

!!! faq "Q: I receive an error on injecting a file.<br />Q: When I import an MS2 into Blender, there is an error and the scene is blank.<br />Q: My Blender plugin will not open the files I extract, or my tools will not inject the MS2 I export."

    1. Ensure your Blender plugin version is the same as your tools version.
    2. Ensure your file is not an older, outdated extraction. Re-extract the file with the latest tools.
    3. If the file is freshly extracted and the plugin/tool versions do not mismatch, report the error with the full log file in #cobra-tools-help
