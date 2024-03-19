# Crash Troubleshooting

!!! warning "Construction"
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

#### On Animal Place

=== "Planet Zoo"

    1. Check that you have a visuals prefab for the animal and gender in your ACSEData Lua
    2. Check that the visuals prefab for the animal and gender is correctly spelled and capitalized in the AnimalDefinitions table of the Animals FDB
    3. Check that the modded AssetPackages referenced in your visuals prefabs exist as .assetpkg in Init.OVL
    4. Check that the .assetpkg reference your Animal OVLs correctly

=== "Jurassic World Evolution 2"

    1. Check that you have a visuals prefab for the animal and gender in your ACSEData Lua
    2. Check that the visuals prefab for the animal and gender is correctly spelled and capitalized in the AnimalDefinitions table of the Animals FDB
    3. Check that the modded AssetPackages referenced in your visuals prefabs exist as .assetpkg in Init.OVL
    4. Check that the .assetpkg reference your Animal OVLs correctly

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