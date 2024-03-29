---
title: dev/Lua
description: Guide for setting up the dev environment for the game
icon: fontawesome/brands/dev
---


!!! note
    The functionality explained here requires [ACSE](https://opennaja.github.io/ACSE/) installed in the game to work.

## Introduction

ACSE provides a few methods for quickly scripting and prototyping code for the game that does not require packing a complete content pack or mod. One of this methods it the local development init.lua file. This file only exists in your local copy of the game (JWE1, JWE2 or PZ) and can be used to speed up your modding capabilities.

!!! warning
    Do not add anything to this file that is required for other Content Packs or mods to work because this file is not distributed widely, as part of ACSE or any other mod.

## File location and default template code.

ACSE makes use of a special folder accesible for the game code located in ``{platform]\Dev\Lua`` where platform is the game folder. If this folder exist, ACSE will look for a special file called init.lua and execute it during the game database bootstrap (the initial ACSE injection point). You can have any Lua code included in this file, however due to the current boostrap step it is being injected in the game it is very likely that many of the game API or features/facilities were not available for your code to use.

The best use of this file is to structure it as if it is another mod or content pack script. The most basic template of the Init.lua file is provided below:

```Lua
-----------------------------------------------------------------------
--/  @file    dev/Lua/init.lua (Template file, valid for all Cobra Engine games)
--/  @author  inaki
--/  @version 1.0
--/
--/  @brief  Creates a development environment in the running game.
--/
--/  The purpose of this file is to allow rapid testing/debugging of
--/  different things without needing to create a custom mod for it.
--/
--/  This file is added by ACSE as a Database manager, exposing all
--/  it CallOnContent methods to the game.
-----------------------------------------------------------------------
local global = _G
local api = global.api
local pairs = pairs
local type = type
local ipairs = ipairs
local next = global.next
local string = global.string

-- Include additiona lua modules as required.
-- local table = require("Common.tableplus")
-- local Main = require("Database.Main")
-- local GameDatabase = require("Database.GameDatabase")

-- @brief main module definition
local Dev = module(...)

-- @brief Database after Init setup. This function is called after Dev:Init() and can
-- be used to alter the setup of your mod if needed.
Dev.Setup = function()
    global.api.debug.Trace("Dev:Setup()")
end

-- @brief Database soft restart. This function is called when the game is doing a restart
-- of the Lua module, meaning after :Shutdown() it will call :Init(). Use this function
-- to cache any data you dont want/need to reinitialize.
Dev.ShutdownForReInit = function()
    global.api.debug.Trace("Dev:ShutdownForReInit()")
end

-- @brief Database Shutdown. This function is called when the database system is being shutdown,
-- usually when the game is closing. You can add your own custom shutdown commands here.
Dev.Shutdown = function()
    global.api.debug.Trace("Dev:Shutdown()")

    -- Remove custom commands. Note: tShellCommand is
    -- created during Init.
    for i, oCommand in ipairs(Dev.tShellCommands) do
        global.api.debug.UnregisterShellCommand(oCommand)
    end

    Dev.tShellCommands = nil
    global.api.debug.Trace("Dev:Shutdown() Finished")

    -- Add your custom shutdown code after this line.
end

-- @brief Database init
Dev.Init = function()
    global.api.debug.Trace("Dev:Init()")

    -- Register our own custom shell commands in this section. Custom shell commands can be
    -- executed through Lua scripting or using the ACSEDebug console window. To run a shell
    -- command from Lua you can call the debug API:
    -- local _, sResult = global.api.debug.RunShellCommand("Echo " .. sStringToEcho)
    --
    Dev.tShellCommands = {
        --
        -- Custom command to echo a string back. The input string will be displayed in the
        -- UI console or added to the game log. Note, this command include a example of how
        -- to add and process arguments to a command.
        global.api.debug.RegisterShellCommand(
            -- Function to run
            function(tEnv, tArgs)
                if #tArgs < 1 then
                    return false, "Needs at least one argument."
                end
                return true, global.tostring(tArgs[1])
            end,
            "Echo {string}",
            "Writes the input string back to the console.\n"
        ),
        --
        -- Crash to desktop. Simple command that will cause Lua to fail forcing a game crash.
        global.api.debug.RegisterShellCommand(
            function(tEnv, tArgs)
                local t = require(tArgs[3]:value())
            end,
            "&Crash&To&Desktop",
            "Crash the game.\n"
        ),

        -- Add more commands after this line.

    }

    -- Add any custom additional Init() code after this line.
end

--
-- Game database section
--
-- Here you can add your custom game database functions. The game database is a facility 
-- provided by the game engine to store and use different data. Since the database is 
-- accessible globaly through the game, any content pack can have access to any information 
-- created or updated by other content packs. This data however is not persistent: it needs to
-- be initialised everytime the game is run, and will get lost when the game is closed.
--

-- Definition of our own database methods
Dev.tDatabaseMethods = {
    --
    -- Example of custom database method, can be called using:
    -- local nResult = GameDatabase.DevTest()
    DevTest = function()
        return 42
    end
    -- ...
}

-- @brief adds our custom database methods to the main game database
Dev.AddDatabaseFunctions = function(_tDatabaseFunctions)
    for sName, fnFunction in pairs(Dev.tDatabaseMethods) do
        _tDatabaseFunctions[sName] = fnFunction
    end
end

--
-- Player table additions. Player table additions allows adding custom code and data
-- to the player table, being used during the entire game. The player table controls
-- everything related to the current game owner, including achievements or other
-- global stats and information through the entire game, not specific to a certain
-- park/zoo/island (this information will be stored in the save file instead).
--

-- Definition of our own player methods
Dev.tPlayerMethods = {
    --
    -- Example new player method, can be called using:
    -- tPlayer:DevPlayerTest(true)
    DevPlayerTest = function(_tPlayer, bTest)
        _tPlayer.bTestingBooleanValue = bTest
    end
    -- ...
}

-- @brief adds our custom methods to the player table
Dev.AddPlayerMethods = function(_tPlayerMethods)
    for sMethod, fnMethod in pairs(Dev.tPlayerMethods) do
        _tPlayerMethods[sMethod] = fnMethod
    end
end

--
-- Game player hooks. The game provides a few hooks when a player data is being
-- processed. This hooks can be used to access data persistently between game runs.
-- Being able to save and load data whenever it is needed can be used to load and
-- save custom setting changes through different game executions, meaning the data
-- will not get lost when you close the game.
--

-- @brief Allows adding attributes to a new player, called when a new player save
-- file is being created. Add your own attributes here.
Dev.AddPlayer = function(_tPlayer)
    global.api.debug.Trace("Dev:AddPlayer()")
    --_tPlayer.bBooleanValue = false
end

-- @brief Allows saving information to file in this player profile. Called when the
-- player data is being saved to disk, allows to store your own data for this player
-- persistently.
Dev.SavePlayer = function(_tPlayer, _saver)
    global.api.debug.Trace("Dev:SavePlayer()")
    -- _saver is the table being saved with our data.
    --_saver.bBooleanValue = _tPlayer.bBooleanValue
end

-- @brief Allows loading information from file of this player profile. Called when a
-- a player save is being loaded, allows you to read data saved previsouly.
Dev.LoadPlayer = function(_tPlayer, _loader)
    global.api.debug.Trace("Dev:LoadPlayer()")
    -- _loader is the table loaded from the file with our data
    --_tPlayer.bBooleanValue = _loader.bBooleanValue
end

-- @brief Notifies a player is removed. Called when a player save is being deleted (
-- usually on a player reset) allows you to read data before it will get destroyed.
Dev.RemovePlayer = function(_tPlayer)
    global.api.debug.Trace("Dev:RemovePlayer()")
    --_tPlayer.bBooleanValue = _loader.bBooleanValue
end

--
-- Custom ACSE managers section.
--
-- Managers are like Monobehaviors for Unity, they are specific class type scripts that
-- will run depending on the game stage. If you need a specific piece of code executed
-- each frame, or when the selected map/park/zoo is loading, you'd probably need to add
-- a custom manager.
--
-- Managers need to be injected in the right environment. ACSE provides functions to
-- inject managers in the main menu screen (globe menu in PZ or main menu in JWE) and the
-- main park game (Zoo in PZ or island in JWE). You can add the same manager to both
-- environments if you want, juts need to be aware what environment are your running your
-- script in. Depending on the environment, other managers might be available and your
-- code can interact with them (e.g. the Weather manager will not be available in the
-- main menu screen).

-- List of custom managers to force injection on the starting screen. It requires the
-- manager lua files to be available in the following location:
-- Dev\Lua\Managers\MyCustomStartManager.lua
Dev.tStartScreenManagers = {
    --['Managers.MyCustomStartManager'] = {},
}

-- @brief Add our custom Manager to the starting screen. If required, the lua modules
-- will be imported from the file system.
Dev.AddStartScreenManagers = function(_fnAdd)
    local tData = Dev.tStartScreenManagers
    for sManagerName, tParams in pairs(tData) do
        global.api.debug.RunShellCommand("ImportModule " .. sManagerName)
        _fnAdd(sManagerName, tParams)
    end
end

-- List of custom managers to force injection on a park. It requires the
-- manager lua files to be available in the following location:
-- Dev\Lua\Managers\MyCustomParkManager.lua
Dev.tParkManagers = {
    --['Managers.MyCustomParkManager'] = {},
}

-- @brief Add our custom Manager to the park/zoo/island game. If required, the lua
-- modules will be imported from the file system.
Dev.AddParkManagers = function(_fnAdd)
    local tData = Dev.tParkManagers
    for sManagerName, tParams in pairs(tData) do
        global.api.debug.RunShellCommand("ImportModule " .. sManagerName)
        _fnAdd(sManagerName, tParams)
    end
end

--
-- List of custom managers to force injection on different game environments
-- separated by environment. To be used when the game has additional game
-- environments (or game modes) other than the start screen and park managers.
-- (e.g. in JWE2 the Species Viewer is a custom environment/game mode.)
-- Note, you will need to know the exact name of the environment script. The lua
-- manager module file has to be available at:
-- Dev\Lua\Managers\CustomEnvironmentManager.lua
Dev.tManagers = {
    -- ["Environments.WhateverEnvironment"] = {
    --    ["Managers.CustomEnvironmentManager"] = {},
    --},    
}

-- @brief Add our custom Manager to the starting screen
Dev.AddManagers = function(_fnAdd)
    local tData = Dev.tManagers
    for sEnvironmentName, tParams in pairs(tData) do
        _fnAdd(sEnvironmentName, tParams)
    end
end

--
-- Custom ACSE Prefabs section.
--
-- This section of the init.lua file allows you to define custom prefabs that will be
-- injected to the game. Note: at this moment it is not possible to load models or
-- other files from the file system so all your game assets need to be added to the
-- game by a custom content pack. You can use this prefabs injection to modify in-game
-- existing prefabs or create custom ones without models too.
--
-- This prefabs are considered ACSE prefabs and can be listed with the custom prefab
-- commands added by the mod.

-- List of custom prefabs
Dev.tPrefabs = {}

-- @brief add custom prefabs to the game
Dev.AddLuaPrefabs = function(_fnAdd)
    local tData = Dev.tPrefabs
    for k, tInfo in global.ipairs(tData) do
        for sPrefabName, tParams in pairs(tInfo) do
            _fnAdd(sPrefabName, tParams)
        end
    end
end

--
-- ACSE Custom components section
--
-- This section allows you to inject custom componetns to the game for testing.
-- Note that components are definitions required by some prefabs and if you are
-- distributing a content pack with these prefabs you need to make sure to include
-- any required component in the Content Pack. Usually the components included
-- in this init.lua file are only used for testing on custom prefabs that don't
-- need to be distributed, like debug assets etc.

-- List of custom components to inject into the game. It requires the
-- manager lua files to be available in the following location:
-- Dev\Lua\Components\MyCustomComponent.lua
Dev.tComponents = {}

-- @brief add custom components to the game
Dev.AddLuaComponents = function(_fnAdd)
    local tData = Dev.tComponents
    for sComponentName, tParams in pairs(tData) do
        global.api.debug.RunShellCommand("ImportModule " .. sComponentName)
        _fnAdd(sComponentName, tParams)
    end
end
-- EOF
```

## Init file usage

The init.lua file was conceived to allow modders to create a custom development environment, with any additional tweakables, commands, managers and files as needed for their daily modding work. This file is not intended to be distributed although it is encouraged to share as much information and resusable code as possible.

Ideally, if a modder is working on a specific project, the init file will include helper function and commands or other relevant information required for the development of this or other modules. Examples of custom commands can include: a method to list if a prop item has all the information defined (to validate the prop mod being worked on), a method to list all spawned props, a method to change or spawn props automatically, etc.

You are free to share your init.lua file with other modders too if you want, althought it is understandable that some of the contents of the init file can be very specific to a modder development workflow that can hardly be of interest for other modders. 

Just apply common sense when creating your own development environment. If you come out with a list of interesting managers and commands that can help a specific modding workflow (e.g. adding new animals or props), you might want to consider creating a 'modding' content pack (or mod) with those specific files and commands to assist others developing their mods. The purpose of this init.lua is to assist you creating a rapid development local setup only.
