---
title: Content Pack Setup
icon: material/numeric-1-box
---

# Content Pack Setup

These instructions are applicable to the following titles:

- Jurassic World Evolution
- Jurassic World Evolution 2
- Planet Coaster
- Planet Zoo

## Content Packs

<div class="annotate" markdown>
Cobra Engine supports additional content modules called **Content Packs**. Whenever Cobra Engine finds a Content Pack, it will perform a set of actions to initialize and include it once the game runs. The game will find new Content Packs looking for a `Manifest.xml` file within the subfolders of the game, usually starting from `{platform}(1)\ovldata`
</div>

1. platform can be win64, win32, etc. 

!!! note "Loading Content Packs"
    The Cobra Engine will find all the modules initially through a folder search, but will load them sorted alphabetically. Consider this if you need your Content Pack to load before or after another Content Pack.


When the game finds the Manifest file, it will first validate that this Content Pack has not been loaded yet. If the Content Pack is new, it will try loading the **Init**ialization resources, and then the **Main** data. There could be different types of content included in a single pack (maps, animals, building elements, etc.), but they all will have the same structure:

- Manifest file
- Init OVL
- Main OVL
- Other OVL files

!!! note
    A Content Pack does not need both Init and Main OVL files, but at least one of them needs to be present.


## Creating the Basic Mod/Content Pack Structure

The following instructions will show you how to create your first Content Pack.

### Content Pack Location and Folder

Navigate into the game ovldata folder and create a custom folder named after your mod. If we were to use 'ExampleContentPack' as our mod name, we would create the `ovldata\ExampleContentPack` folder.

### Adding a Manifest File

The Manifest file defines the Content Pack; it gives the module a name used later by the engine to bootstrap the content initialization and a unique ID used to check if the module has been loaded before. It is important that these two (Name and ID) are unique for the module to load properly.

Content of `ovldata\ExampleContentPack\Manifest.xml`
```xml
<ContentPack version="1">
  <Name>ExampleContentPack</Name> <!-- This must match your folder name -->
  <ID>9a1fce40-4dce-11ec-81d3-0242ac130003</ID> <!-- You must replace this UUID -->
  <Version>1</Version>
  <Type>Game</Type>
</ContentPack>
```
!!! tip "UUID"
    **You need your own UUID**, you can visit this [UUID Generator](https://www.uuidgenerator.net/) to create one. Replace the value inside ```<ID></ID>```

!!! tip "Name"
    It is **vital** to name the Content Pack after the folder it is contained in for various reasons such as ACSE naming requirements.


## Creating the Content Package(s)

Inside your Content Pack folder, add a subfolder called Main. If you also need some initialization (will explain later) Create an Init folder too. The content of your module folder Will look like this:

```
ovldata\ExampleContentPack\Init
ovldata\ExampleContentPack\Main
ovldata\ExampleContentPack\Manifest.xml
```

## Other required or optional folders.

While you have total freedom on how to name any extra OVL files included by your package, the game engine will also look for specific files/folders inside your module, like Localisation files. If your module has strings that need translation, you will need to provide the data through a localisation folder tree for the different languages.

## Content Pack Resources

Anything inside the module OVL files will be considered a resource for the game, regardless of its mime type; however, some resources will be treated differently by the game engine precisely depending on their mime type. It is important to understand that OVL files are loaded on-demand, and therefore your resources in 'Init' will not be able to access your resources in the 'Main' OVL files, or any other OVL file your Content Package has that has not been loaded yet.


To begin with, we will add a harmless file without any purpose to the Main.ovl file. Create the ```ExampleContentPack.txt``` inside the ```ExampleContentPack\Main``` folder and type the following in it:

```
Version: 1.0
```

## Packing Your Content

Now it is time to create the OVL files for your Content Pack. Run the `cobra-tools\ovl_tool_gui.py` script and perform the following actions:

- Select the right title from the game dropdown list.
- Click File > New (++ctrl+n++) and select the ```ExampleContentPack\Main``` folder. The tool will try loading all the known files and show the list of OVL contents.
- Click File > Save (++ctrl+s++). This saves the OVL to ```ExampleContentPack\Main.ovl```.


At this point, the tool has created the ```ExampleContentPack\Main.ovl``` file from the contents of the ```ExampleContentPack\Main``` folder. Your module folder should look like this now:


```
ovldata\ExampleContentPack\Init
ovldata\ExampleContentPack\Main
ovldata\ExampleContentPack\Main.ovl
ovldata\ExampleContentPack\Manifest.xml
```

Because the tool only allows the creation of an OVL file at a time, you will need to repeat this process for every folder with content in your module, and you don't need to pack folders that don't have any files on them. The tool will try to guess the name of the file based on the last folder it loaded the content from, but don't forget to double check that you are using the right folder and name for your output OVL file.


## Distributing the Content Pack

If you want to share your Content Pack, you only need to distribute the Content Pack folder containing your Manifest.xml and OVL files. Inside ovldata, create a ZIP file from your Content Pack folder and save it. Open your ZIP file and remove any directory and file not required from it. Any folder such as `Init` or `Main` used for `File > New` in OVL tool does not need to be included in the package. 

In this example, the ZIP content will look like this:

```
ExampleContentPack\
    Main.ovl
    Manifest.xml
```
You can share this ZIP file now. To use it, all a person has to do is unzip the Content Pack folder inside the ZIP to the ovldata folder.


## Final Notes

Not all file types can be imported at this time. There is a [list of supported mime types](../../Supported-Formats.md) you can check.

The game does not load loose files from the file system; all the resources need to be imported into an OVL file. Therefore, you will need to repeat the packing process every time you modify a file in your content; however, you will only need to repack the specific folder where the modified file is.

