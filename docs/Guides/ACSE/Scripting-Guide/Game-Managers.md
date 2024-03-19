---
title: Game Managers
icon: material/numeric-3-box
---

!!! note
    The functionality explained here requires [ACSE](https://opennaja.github.io/ACSE/) installed in the game to work.

## Introduction

Game managers are Lua files that when injected, can communicate and use existing game API, modify or add new functionality or even gameplay to a Cobra Engine game. A game manager is similar to a **singleton** Monobehaviour in Unity. It is a special class Lua file with different functions called by the Cobra Engine on different steps of the game including initialization, shutdown, or every time a frame is being rendered. If you need to execute your custom Lua code everytime a game is loaded, an action is performed or a frame is rendered you definitelly need a custom Manager.

Managers are not tied to entities, meaning there can be only one Manager instance running at any given time.

## Environments

Game managers run inside a game Environment. An Environment is a Lua context responsible for loading managers (could be in an specific order) and handles all the manager life cycle management. Environments are loaded by the running world script running the loaded world. In other words: there are multiple game environments, and managers need to opt-in to be loaded. Cobra Engine usually has two main Environments (or World scripts):
- Start screen Environment: used during the main menu screen (globe screen on PZ, game selection UI in JWE, etc).
- Park environment: used during the actual playable game (a Zoo in PZ or an Island in JWE).

There could be additional game Environments (e.g. the Species Viewer mode in JWE2 uses a custom Environment). Each Environment will include a different set of Managers (e.g. a Park environment will need animal control managers, but not the main menu UI). Regardless the environment the Manager is loaded into, it usually performs the same steps and requires a very specific set of functions to interact with the game. Because these two environments are so different, you usually would like to have a Park Manager And a Start screen Manager in case you need both, otherwise just include your Manager in the environment in which you will use it, you don't need to include your Managers in all the environments.

The environments are defined by the game and the game main script uses one environment or another depending on the world being loaded. It is strongly recommended to not modify the existing environments manually (any Environments.*.lua file) and use ACSE to inject your manager file and prevent breaking other mods.

## Cobra Game Manager Structure

A game manager for Cobra Engine can be templated as the following:

```Lua
-----------------------------------------------------------------------
--/  @file    Managers.CustomManager.lua
--/  @author  Inaki
--/  @version 1.0
--/
--/  @brief  Boilerplate template for a park manager script
--/  @see    https://github.com/OpenNaja/ACSE
-----------------------------------------------------------------------
local global = _G
local api = global.api
local pairs = global.pairs
local require = global.require
local module = global.module
local Object = require("Common.object")
local Mutators = require("Environment.ModuleMutators")

--/ Main class definition
local CustomManager = module(..., Mutators.Manager())

--
-- @Brief Init function for this manager
-- @param _tProperties  a table with initialization data for all the managers.
-- @param _tEnvironment a reference to the current Environment 
--
-- The Init function is the first function of the manager being called by the game.
-- This function is used to initialize all the custom data required, however at this
-- stage the rest of the managers might not be available.
--
CustomManager.Init = function(self, _tProperties, _tEnvironment)
    api.debug.Trace("CustomManager:Init()")
end

--
-- @Brief Activate function for this manager
--
-- Activate is called after all the Managers of this environment have been initialised,
-- and it is safe to assume that access to the rest of the game managers is guaranteed to
-- work.
--
CustomManager.Activate = function(self)
    api.debug.Trace("CustomManager:Activate()")
end

--
-- @Brief Update function for this manager
--
-- Advance is called on every frame tick.
--
CustomManager.Advance = function(self, _nDeltaTime, _nUnscaledDeltaTime)
    --api.debug.Trace("CustomManager:Advance()")
end

--
-- @Brief Deactivate function for this manager
--
-- Deactivate is called when the world is shutting down or closing. Use this function
-- to perform any deinitialization that still requires access to the current world data
-- or other Managers.
-- 
CustomManager.Deactivate = function(self)
    api.debug.Trace("CustomManager:Deactivate()")
end

--
-- @Brief Shutdown function for this manager
--
-- Shutdown is called when the current world is shutting down.
--
CustomManager.Shutdown = function(self)
    api.debug.Trace("CustomManager:Shutdown()")
end

--/ Validate class methods and interfaces, the game needs
--/ to validate the Manager conform to the module requirements.
Mutators.VerifyManagerModule(CustomManager)
```

Not all the Manager calls are required, in fact, none of them are required. You could have a Manager that only runs a piece of code on the Init() step of the world loading so you can just implement Init() and remove all the other functions. Regardless of how simple your Manager is, it still needs to be validated as a Manager at the end by the Mutators object or it will not load.

## Exporting Methods: Manager Interface

The basic Manager template showcased in the previous point is so simple, no other Manager in the game can interact with it, which is appropriate for many cases. However, it is common for a Manager to allow other game areas to interact with it. Imagine your Manager has the ability to open or close a park (allowing guests to come in or not), you might want this action to be exposed to other Managers so they can just use it without having to implement it. Another good example is the Weather storm manager: it includes code to start/stop storms based on certain conditions; however, it also allows other Managers to request a Storm starting or stopping at any given time. This functionality is achieved through Interfaces.

An interface is another script that defines what parts of a Manager will be exposed publicly to be used by other game Managers. An interface is only required if you want your Manager code to be exposed to other game elements. The use of interfaces is encouraged to prevent two different managers trying to control the same element of the game. Imagine the case of the door, where one manager has been instructed to Open the door and another one has been instructed to do the opposite.

Lets have a look at the CameraShake manager from JWE2. This manager adds the ability to shake the camera (this Manager exists in JWE2) for close dinosaur stomps, weather events, etc. This is preferred to having multiple scripts trying to shake the camera at the same time, if any other manager needs the effect, it can ask the CameraShake manager to do that instead. To allow this functionality, the CameraShake manager provides an Interface that looks like this:

```Lua
-----------------------------------------------------------------------
--/  @file    Interfaces.ICameraShakeManager.lua
--/  @author  Frontier
--/
--/  @brief  Interface file for the CameraShake Manager 
--
local Mutators    = require("Common.mutators")
local Interface   = module(..., Mutators.Interface)
Interface.Methods = {
    "ShakeCamera", 
    "SetPeriodicShakeParams"
}
Mutators.VerifyInterfaceModule(Interface)
```

This interface is exporting two methods, called: **ShakeCamera** (to start the shaking action) and **SetPeriodicShakeParams** (to configure how the shaking will perform).

Creating the interface file is not the only thing required for a Manager to export functions to the game. The interface also needs to be defined in the Manager file:

```Lua
-----------------------------------------------------------------------
--/  @file    Managers.CameraShakeManager.lua
--/  @author  Frontier
--/
--/  @brief  Interface file for the CameraShake Manager 
--
local global = _G
local api = global.api
local pairs = pairs
local math = global.math
local table = require("Common.tableplus")
local Vector3 = require("Vector3")
local Object = require("Common.object")
local mathUtils = require("Common.MathUtils")
local Mutators = require("Environment.ModuleMutators")

-- Define our Manager class using a specific interface file
local CameraShakeManager = module(..., Mutators.Manager("Interfaces.ICameraShakeManager"))

-- ... rest of the file follows
```

That is the difference between a Manager with and without and interfaces, the interface file needs to be specified on the module creation code. With this parameter, during the validation of the Manager, the game will check that the two exposed functions: "ShakeCamera" and "SetPeriodicShakeParams" exist in the Manager class. In that file (Managers.CameraShakeManager.lua) you will find the following code:

```Lua
CameraShakeManager.ShakeCamera = function(self, _tParams)
-- ...
end

CameraShakeManager.SetPeriodicShakeParams = function(self, _tParams)
-- ...
end
```

To finalize this point, if we want to expose functions to other part of the game, we will need to create an interface. So, the next question is then: how do we *use* an existing interface? 

## Using Manager Interfaces

If we want to use some other Manager interface, all we need to do is request the interface from the running Environment. The Environment class is responsible for the life cycle all the Managers present in the game mode we are in:

```Lua
  -- the _tEnvironment table is passed to the manager during the Init() call.
  local iCameraShakeManager = _tEnvironment:RequestInterface("Interfaces.ICameraShakeManager")

  -- Now we just need to call the exported method with the appropriate expected data. Note: the
  -- data to call each exported method is different and requires looking at the inputs of the function 
  -- we are calling.
  iCameraShakeManager:ShakeCamera( tCameraShakeData )
```

The current Game managers already export a lot of interesting functions you can use if you just request the corresponding interfaces. These functions include full control of the playing Cinematic video, communications, popups, full access to the Park rating, etcetera. Before going into coding any of this logic, first find out what Manager is responsible for what functionality, and then see what is exposed in the manager interface that you can use in your own scripts. 

## Complex Manager Initialization

Sometimes, especially when a Manager depends on other Managers it is better to instruct the game to load your Manager in an specific order. This is accomplished with the addition of some Manager initialization data that will ensure any required dependency is loaded before your own Manager. This order affects not only the loading but also the order in which every class function is executed. If you need to update some data in your Manager only After the park rating has been updated, then you definitely want to force the ParkRatingManager to load before your own Manager.

A good example for this particular case is the Ingen Database UI Manager of JWE2. This manager is responsible for preparing the data to be displayed in the Ingen Database tab, however this information is different for each user because it depends on a) Gene unlocks achieved by the player, b) the current techtree defined for the game. This is why, the IngenDatabaseUIManager Manager specifies the following phase ordering and requirements:

```Lua
-- ..
-- Define this Manager class using a custom Interface:
local InGenDatabaseUIManager = module(..., Mutators.Manager("Interfaces.IInGenDatabaseUIManager"))

-- Execute our Init() function after Managers.GeneLibraryManager:Init()
InGenDatabaseUIManager.PhaseDependencies = {
  Init = {
     "Managers.GeneLibraryManager"
  }
}

-- Execute our Init() function after Managers.TechTreeManager:Init() if possible
-- Execute our Activate() function after Managers.TechTreeManager:Activate() if possible
InGenDatabaseUIManager.OptionalPhaseDependencies = {
  Init = {
    "Managers.TechTreeManager"
  }, 
  Activate = {
    "Managers.TechTreeManager"
  }
}
```

Using the PHaseDependencies table, a Manager can instruct the Environment to execute its functions (e.g. Init or Activate) after the other Managers functions have been executed (in this case GeneLibraryManager and TechTreeManager). While the OptionalPhaseDependencies is not an enforced execution order, it will be honored by the game if it is defined and possible. This is because in some cases, other Managers might have other phase dependencies and circular references can ocurr at some point (Manager A requiring Manager B and viceversa).

## Injecting Managers

As mentioned before, the current method to inject Managers in the game is through [ACSE](https://opennaja.github.io/ACSE/). You can still edit existing Managers in the game through the normal editing process using Cobra Tools.

ACSE needs to know what environment you want your Managers to be injected into. ACSE has three different methods to add Managers, two of them are specific for the main common Environments (Start Screen and Park), and the third allows any other Environment specified.

This is a code snippet to add Managers with ACSE, and can be pasted in any of the Database Lua scripts of your mod (ACSE will find them and use them):

```Lua
-- List of custom managers to force injection on the starting screen
YourModLoader.tStartScreenManagers = {
    ["Managers.MyCustomStartManager"] = { }, -- Add your custom settings inside the table.
}

-- @brief Add our custom Manager to the starting screen
YourModLoader.AddStartScreenManagers = function(_fnAdd)
    local tData = YourModLoader.tStartScreenManagers
    for sManagerName, tParams in pairs(tData) do
        _fnAdd(sManagerName, tParams)
    end
end

-- List of custom managers to force injection on a park
YourModLoader.tParkManagers = {
    ["Managers.MyCustomParkManager"] = { },  -- Add your custom settings inside the table.
}

-- @brief Add our custom Manager to the starting screen
YourModLoader.AddParkManagers = function(_fnAdd)
    local tData = YourModLoader.tParkManagers
    for sManagerName, tParams in pairs(tData) do
        _fnAdd(sManagerName, tParams)
    end
end
```

Usually this is enough to have your Managers added to the game. For the case where you want your Manager added to a different environment, you can use the following piece of code:

```Lua
-- List of custom managers to force injection on a custom Environment
YourModLoader.tManagers = {
    ["Environments.WhateverEnvironment"] = {
        ["Managers.CustomEnvironmentManager"] = {},
    },
}

-- @brief Add our custom Manager to the different environments
YourModLoader.AddManagers = function(_fnAdd)
    local tData = YourModLoader.tManagers
    for sManagerName, tParams in pairs(tData) do
        _fnAdd(sManagerName, tParams)
    end
end

```

## Argument Passing

The Manager gets initialized by the Environment through the `Init()` function like so:

```Lua
CustomManager.Init = function(self, _tProperties, _tEnvironment)
-- ...
```

The `_tProperties` attribute used during the `Init()` call correspond to whatever settings you used to inject the Manager through ACSE. If this was your ACSE Manager definition:

```Lua
YourModLoader.tStartScreenManagers = {
    ["Managers.MyCustomStartManager"] = { 
       bBooleanValue = false, 
       sCustomString = "Testing String",
    },
}
```

You will receive these parameters as `_tProperties` when the Manager gets initialized. the `_tProperties` table allows to have functionality enabled or disabled specifically for each different environment (or game).
