# cobra-tools
A simple GUI for extracting OVL and OVS archives and modifying their contents.

![Imgur](https://i.imgur.com/ow8rKVd.png)

# Installation
Simply download and unzip to a folder of your choice. You need to have installed:
- Python 3.6
- pyffi
- pyqt5

# How to use
1) Double click `ovl_tool.bat` to start the main tool.
2) Open an OVL file.
3) Unpack the OVL file to a folder.
4) Modify the extracted files.
5) If you have modified MDL2 models that used a shared MS2 buffer in blender, use the MS2 Merger on those.
6) Inject modified files into OVL.
7) Save OVL and test.

# Supported Filetypes
The following filetypes are currently fully supported for editing:
- Txt
- Png

The following filetypes are partially supported and may experience some issues when editing:
- Mdl2 & Ms2 

The following filetypes are currently being researched for future support:
- Bani & Banis
- Fdb
- Lua
- Xml
- Fgm
- Matcol
- Mani & Manis

