# cobra-tools
A simple GUI for extracting OVL and OVS archives and modifying their contents.

![Imgur](https://i.imgur.com/ow8rKVd.png)

# Installation
Simply download and unzip to a folder of your choice. You need to have installed:
- Python 3.6
- pyffi 2.2.4.dev3 (run: `pip install PyFFI==2.2.4.dev3`)
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

# Basic Tutorials
### Jurassic World Evolution

The most advanced form of mod possible at this time will be a species replacement mod. To accomplish this task one can follow the steps outlined below:
1) Double click `ovl_tool.bat` to start the main tool.
2) Open the OVL file for the chosen dinosaur species to be replaced.
3) Unpack the OVL file to a folder.
4) import the MDL2 of the dinosaur into blender, if it crashes then close and restart the OVL tool and uncheck the reverse sets box and unpack once again.
5) once the model imports into the blender, edit the model or rig the new one to the nodes following the same conventions used
6) export the MDL2 by selecting the old one. 
7) If you have modified MDL2 models that used a shared MS2 buffer in blender, use the MS2 Merger to merge back the MDL2's.
7a) an example of step 7 is editing the dinosaur model and not the airlift straps, select the blender exported mdl2 for the dinosaur and the stock airlift straps mdl2 as the models to be merged. 
8) edit the PNG files as needed
9) inject any edited files back into the OVL tool and save the new dinosaur OVL
10) replace the stock OVL with the new one, back up the old one
11) Double click `ovl_tool.bat` to start the main tool.
12) Open the Loc.OVL file for the language your game uses from the content folder containing the dinosaur species you want to replace
13) Unpack the OVL file to a folder.
14) Edit the Txt files relevant to replacing the species.
15) inject the Txt files and save the new Loc.OVL.
16) replace the stock Loc.OVL and back it up.

### Planet Zoo

The most advanced form of mod possible at this time will be full model replacement. To accomplish this one can follow the following steps:
1) Double click `ovl_tool.bat` to start the main tool.
2) Open the OVL file for the chosen dinosaur species to be replaced.
3) Unpack the OVL file to a folder.
4) import the MDL2 of the dinosaur into blender, if it crashes then close and restart the OVL tool and uncheck the reverse sets box and unpack once again.
5) once the model imports into the blender, edit the model or rig the new one to the nodes following the same conventions used
6) export the MDL2 by selecting the old one. 
7) If you have modified MDL2 models that used a shared MS2 buffer in blender, use the MS2 Merger to merge back the MDL2's.
7a) an example of step 7 is editing the dinosaur model and not the airlift straps, select the blender exported MDL2 for the dinosaur and the stock airlift straps MDL2 as the models to be merged. 
8) edit the PNG files as needed
9) inject any edited files back into the ovl tool and save the new dinosaur ovl
10) replace the stock ovl with the new one, back up the old one

Note that one cannot currently change the ingame text in the Loc.OVL yet and that only the shell fur shader is active on moddable animals at this point in time. later releases will activate the ability to use fin fur shader as well and edit the Planet Zoo ingame text.

### Disclaimer
Remember to backup all mod files and stock files. any patches will reset or break the mods and will need to be redone and re-released. 

### Legal Notice
- This tool is developed under 'fair use' by enthusiasts and is not affiliated with Universal© or Frontier® in any form.
- Use at your own risk. This tool may cause damage to you, your equipment or your data.
- Do not use or modify these tools to circumvent copy protections; especially, do not try to unlock downloadable content for free or share official artwork or intellectual property or engage in so-called data mining to announce game content before an official announcement.
- Do not charge money or ask for donations for mods created with these tools.


### Credits
- Planet Zoo, Cobra, Frontier and the Frontier Developments logo are trademarks or registered trademarks of Frontier Developments, plc.
- Jurassic World, Jurassic World Fallen Kingdom, Jurassic World Evolution and their respective logos are trademarks of Universal Studios and Amblin Entertainment, Inc.
- Daemon1, DennisNedry1993 and Inaki for initial modding attempts and documentation.
