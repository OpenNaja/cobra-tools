# Crash Troubleshooting

!!! construction
    This page is currently under construction!

This document will cover various scenarios in which your game may crash, and provide possible solutions.

This document assumes you are familiar with modding and are having trouble with your own mod.

!!! tip "NON-MOD AUTHORS"
    For end-user troubleshooting regarding your installed mods, instead refer to [Installed Mods Troubleshooting](Installed-Mods-Troubleshooting.md)

### On Game Start

#### Immediate (Before intro cinematic)

1. Check your Lua file syntax. Lua syntax errors will show as Errors in OVL Tool upon injection

    !!! note
        You can also avoid syntax errors by using [Visual Studio Code](https://code.visualstudio.com/) with a Lua extension.

2. Check that the OVLs included by your OVLs exist. Included OVLs are at the bottom of OVL Tool in the dropdown menu
3. Check that all modded AssetPackages named in your Lua prefabs have an .assetpkg in Init.OVL
4. Check that all used .assetpkg in Init.OVL reference an OVL that exists in ovldata/
5. Check that all FDB named in GetDatabaseConfig in your Databases Lua exist in Main.OVL

#### Just before globe menu

1. A functional error in your Lua code that is not caught with just syntax checking, i.e. missing functions, tables
2. ?

### On Map Load

=== "Planet Zoo"

    1. Check that your animal has an .animalresearchunlockssettings file
        - ...and that the number of VetLevel in this file matches the Research FDB
        - ...and the names of the research in this file match the names in the Research FDB
    2. ?

=== "Jurassic World Evolution 2"

    1. ?

### In-Game

#### On Animal Spawn

=== "Planet Zoo"

    1. Main.OVL Prefabs
        - [x] The Visuals Prefab for the animal/gender exists in your Data Lua, or is `required` in Data/LuaDatabases as its own .lua
            - [x] If using separate .lua per Visuals Prefab, ensure these exist in your OVL and are named the same as in your Data Lua
        - [x] The Visuals Prefab is correctly spelled and capitalized according to the AnimalDefinitions table of the Animals FDB
        - [x] The modded AssetPackages referenced by the Visuals Prefab exist as .assetpkg in your Init.OVL
        - [x] The `ModelName`, `MotionGraphName`, and `HitcheckModel` strings all match the names of the MDL2 and motiongraph files in your animal OVL
    2. Init.OVL Asset Packages
        - [x] The .assetpkg match in name with the modded AssetPackages in your Visuals Prefabs
        - [x] The .assetpkg contents reference your Animal OVLs correctly i.e. `ovldata\{MOD_NAME}\Animals\{ANIMAL_NAME}\{ANIMAL_NAME}`
    3. Main.OVL FDBs
        - [x] The Visuals Prefabs in the AnimalDefinitions table are spelled and capitalized the same as the Prefabs loaded by your Data Lua.

=== "Jurassic World Evolution 2"

    1. Main.OVL Prefabs
        - [x] The Prefab for the Dinosaur exists in your Data Lua, or is `required` in Data/LuaDatabases as its own .lua
            - [x] If using separate .lua per Prefab, ensure these exist in your OVL and are named the same as in your Data Lua
        - [x] The Prefab is correctly spelled and capitalized according to the Species table of the Dinosaurs FDB
        - [x] The modded AssetPackages referenced by the Prefab exist as .assetpkg in your Init.OVL
        - [x] The `ModelName` and `MotionGraphName` strings all match the names of the MDL2 and motiongraph files in your Dinosaur OVL
        - [x] The `DecalPrefabName`, if modded, matches the name and capitalization of the Decal Prefabs loaded by your Data Lua.
        - [x] Any modded Prefabs (e.g. Footprint) referenced by your Dinosaur Prefab are listed ***before*** the Dinosaur Prefab in your Data Lua.
    2. Init.OVL Asset Packages
        - [x] The .assetpkg match in name with the modded AssetPackages in your Prefabs
        - [x] The .assetpkg contents reference your Dinosaur OVLs correctly i.e. `ovldata\{MOD_NAME}\Dinosaurs\{DINO_NAME}\{DINO_NAME}`
    3. Main.OVL FDBs
        - [x] The Prefabs in the Species table are spelled and capitalized the same as the Prefabs loaded by your Data Lua.
        - [x] SpeciesID must be unique and not collide with any other Species

#### Miscellaneous

=== "Planet Zoo"

    ##### On Research Open

    1. Ensure the animal's Research FDB has been made with the tools/scripts. 
        - Tool-made Research FDB ResearchIDs are taken care of for you, thus minimizing chances of ID collision crashes
    2. ?

    ##### On Zoopedia Open or Zoopedia Filtering/Scrolling

    1. Check the references in your Zoopedia-related .userinterfaceicondata 
        - Check that the .assetpkg referenced exists
    2. ?

=== "Jurassic World Evolution 2"

    ##### Something JWE2

=== "Planet Coaster"

    ##### Something PC