# cobra-tools
A simple GUI for extracting OVL and OVS archives and modifying their contents.

![Imgur](https://i.imgur.com/ow8rKVd.png)

# Installation
Get the latest release [here](https://github.com/OpenNaja/cobra-tools/releases) and unzip to a folder of your choice. You need to have installed:
- Python 3.6 (make sure you add it to the system path during installation)
- pyffi 2.2.4.dev3 (run: `pip install PyFFI==2.2.4.dev3`)
- pyqt5 (run: `pip install pyqt5`)

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
4) import the MDL2 of the dinosaur into blender, if it crashes or fails to import correctly then uncheck or check reverse sets and unpack the ovl once again
5) once the model imports into the blender, edit the model or rig the new one to the nodes following the same conventions used
6) export the MDL2 by selecting the old one. 
7) If you have modified MDL2 models that used a shared MS2 buffer in blender, use the MS2 Merger to merge back the MDL2's. Ensure the MS2 filename is the same as stock before merging
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
2) Open the OVL file for the chosen species to be replaced.
3) Unpack the OVL file to a folder.
4) import the MDL2 of the animal into blender, if it crashes or fails to import correctly then close and restart the OVL tool and uncheck the reverse sets box and unpack once again.
5) once the model imports into the blender, edit the model or rig the new one to the nodes following the same conventions used
6) export the MDL2 by selecting the original stock one. 
7) If you have modified MDL2 models that used a shared MS2 buffer in blender, use the MS2 Merger to merge back the MDL2's.
8) edit the PNG files as needed
9) inject any edited files back into the ovl tool and save the new animal ovl
10) replace the stock ovl with the new one, back up the old one

Note that one cannot currently change the ingame text in the Loc.OVL yet and that only the shell fur shader is active on moddable animals at this point in time. later releases will activate the ability to use fin fur shader as well and edit the Planet Zoo ingame text.

### Editing Texture PNG Files
Many of the texture file types use the transparency layer not for transparancy but for other texture formats. If you are using photoshop please install the SuperPNG plugin so that you can load the transparency as a seperate channel. 

The link is available here: https://www.fnordware.com/superpng/

To use this plugin, hold shift when opening a png file in photoshop and choose the following settings.

![Imgur](https://i.imgur.com/9KPTx86.png)

Blendweights files work alongside the matcol files to generate scales on the mesh. if you are using a custom model feel free to blank out this file completely to not deal with the scale normal maps or can edit it to apply scale and wrinkle texture to the new UV

PackedTexture files contain blood splatter in the R channel, damage in the G Channel, Specular/Roughness in the B channel and AO in the alpha channel. 


#### Disclaimer
Remember to backup all mod files and stock files. any patches will reset or break the mods and will need to be redone and re-released. 

#### Legal Notice
- This tool is developed under 'fair use' by enthusiasts and is not affiliated with Universal© or Frontier® in any form.
- Use at your own risk. This tool may cause damage to you, your equipment or your data.
- Do not use or modify these tools to circumvent copy protections; especially, do not try to unlock downloadable content for free or share official artwork or intellectual property or engage in so-called data mining to announce game content before an official announcement.
- Do not charge money or ask for donations for mods created with these tools.


### Credits
- Planet Zoo, Cobra, Frontier and the Frontier Developments logo are trademarks or registered trademarks of Frontier Developments, plc.
- Jurassic World, Jurassic World Fallen Kingdom, Jurassic World Evolution and their respective logos are trademarks of Universal Studios and Amblin Entertainment, Inc.
- Daemon1, DennisNedry1993 and Inaki for initial modding attempts and documentation.


### Discord
Some Discords where modding progress is discussed can be found here.

- https://discord.gg/SmjHnB2 Planet Zoo Discord Community
- https://discord.gg/Wt48PYX Frontier Modding Club
