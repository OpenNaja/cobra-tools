### Before Installing Mods

!!! warning 
    Removing, installing, or updating mods comes with the risk of having issues with loading old parks. If there is a park you are working on and you do not want to deal with the associated risks, **do not modify your game**.

1. Save a backup of your current ovldata folder so that you can always go back to the version of the game that can load your existing parks.
2. Make a [copy of your save files](#).

### When Installing Mods

Mods interact with the game and other mods in different ways. Mods may:

1. Require other mods to work (e.g. it requires ACSE).
2. Require specific DLCs to be owned before they can work, because it requires features from this DLC.
3. Manipulate game data used by other mods, or even manipulate other mod data (e.g. PZPlus).

Thus, it is important to read the Nexus Mods page description of the mod you are downloading to understand what you need to do for the mod to work correctly.

!!! failure "MODPOCALYPSE"

    It is **NOT RECOMMENDED** to install several mods at once, especially new mods you have never used before. If one of them crashes the game, you'll have no idea which one of them is the culprit. 
    
!!! success "INSTEAD..." 

    Install new mods one by one, and always make sure you download the latest version of the mod.


### Installing the Mod

The ovldata folder is where the game reads its ContentPacks. Every mod nowadays is a ContentPack and has to be installed the same way as the game installs its DLCs in this folder. Do not make folders and subfolders and put mods in them, this will break the game. Every mod needs to be installed in the same folder. 
Mod folder names don't usually have sequences of numbers or other characters, just letters (and maybe a number or two). If you see a folder that has a long sequence of numbers on it you need to install the mod correctly.

Every mod needs a 'manifest' file. You will find this file Inside every folder in OvlData. If you go to the mod folder and you can't find a file named 'Manifest' chances are this mod is installed wrong.

### Crashes After Installation

If you install a mod and it crashes your game, check the installation instructions and requirements. 
When things don't work, the best course of action is to remove the last mod you installed and try running the game again. If this mod keeps crashing your game you might want to open a bug report in Nexus Mods commenting on the problem.

### if all mods are crashing or mods don't work for you

Usually this is a misconception and more like a rare case. Most likely you have reached a point where your game is completely unstable and will be like that even without mods. Here is a little troubleshooting guide to get you through this case:

1. Make sure you make a copy of your saved games, you might want to come back to them (TODO: maybe add the point)
2. Remove all mods and try running the game. if the game doesn't run, then Validate the game files (TODO: maybe add how to). If this is still not working, reinstall the game. It might be a problem somewhere else in the computer that has nothing to do with the game.
3. You need to make sure that the game runs without mods, and confirm that by going to the globe screen (main menu).
4. Install ACSE (and only ACSE). Don't rush installing mods again. ACSE will show its version in the main menu screen (globe screen), confirm ACSE is running before installing other mods.
5. Install PZP (and only PZP). Again, PZP will show its version in the globe screen, you can confirm it is working when you go to the main menu.
6. Start installing mods again, but remember that to get different results you need to do something different this time. Redownload all the mods you are going to install. This process might look daunting but the current mods you had downloaded broke your game, and installing them might just have the same ending results. This also ensures you always have the latest versions and not old ones. Do not install all the mods at once, install them in packs of 5 or 10 (or less), so you know which ones you have to remove if the game stops working.
7. From this point, if you encounter a problem with a mod, it will most likely be a mod issue that you'd need to report in the corresponding Nexus Mods page.

### Other tips

When you want to preserve a park, it is important to know that you will most likely need the same mods installed the next time you want to open it. Either take notes or make a copy of your game files just in case so you will always have a list of the mods you used, or even the mod versions that worked when you were making the park.

*[ovldata]: The folder located at {Game}\win64\ovldata
