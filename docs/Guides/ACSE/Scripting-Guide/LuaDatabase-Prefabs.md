---
title: LuaDatabase and Prefabs
icon: material/numeric-4-box
---

While there are multiple ways to achieve the same goal (having your mod running flawlesly in the game), the way you interact with ACSE is totally up to you. We have however defined a 'best practice' for mods when you interact with ACSE to make sure we can guarantee compatibility with other tools moving forward.

## Checking ACSE is present in the game.

If you mod depends on ACSE, to avoid the game crashing it is recommended to test the right version of ACSE is installed. You can just simply ignore all your mod loading steps if ACSE is not present, or even show a prompt to the user to inform ACSE is needed to use your mod. This is a template for JWE2.

If your mod provides custom FDBs to the game, first you'll need to make sure these FDBs are not loaded. Your **Init/Databases.YOURMODNAME.lua** file should look like this (the .... indicates this is your own content and change from mod to mod):

```lua
-----------------------------------------------------------------------
--/  @file    Databases.YOURMODNAME.lua
--/  @author  yourself
--/  @version 1.0
--/
--/  @brief  Defines additional FDB configuration. 
--/          Requires ACSE > 0.641 to work due to add custom prefabs.
--/
--/  @see    https://github.com/OpenNaja/ACSE
-----------------------------------------------------------------------
local global = _G

--/ Create the custom module for the package Init.
local YOURMODNAMEDatabaseConfig = module(...)

--
-- Define the databases to be merged and the merging rules
-- 
YOURMODNAMEDatabaseConfig.tConfig = {

    -- Load our Paths database
    tLoad = {
         ....
    },

    -- Merge with the existing Paths database.
    tCreateAndMerge = {
         ....
    }

}

-- @brief GameDatabase hook to add load and merge custom databases
YOURMODNAMEDatabaseConfig.GetDatabaseConfig = function()

  -- Prevent the inclusion of this assets if ACSE <= 0.641 because
  -- prefab support wasn't included until later versions.
  if not global.api.acse or global.api.acse.versionNumber < 0.641 then
    return {}
  else 
    return YOURMODNAMEDatabaseConfig.tConfig
  end
  
end

```

This change will prevent your FDBs being added to the game unless the right version of ACSE is installed. The same way, we now have to prevent the Prefabs and other UI information being added to the game. The next file we need to touch is your mod LuaDatabase.lua (**Main/YOURMODNAMELuaDatabase.lua**), that should look like this (the .... indicates this is your own content and change from mod to mod): 

```lua
--
-- @brief Informs the main game database about custom databases provided by this content pack
-- @param _tContentToCall (table) table of additional database modules provided.
--
YOURMODNAMELuaDatabase.AddContentToCall = function(_tContentToCall)

    -- Verify the game environment complies with the requirements before adding our gameplay items.
    if not api.acse or api.acse.versionNumber < 0.641 then
        -- Note: Push/Pop user messages is only available in JWE1 and JWE2 games. 
        api.game.PushUserMessage(
            "[STRING_LITERAL:Value='The YOURMODNAME Mod requires ACSE 0.641\n or greater installed and has been disabled.']", nil
        )
        return
    end 

    -- Add these module to the game database list.
    -- Continue your normal loading here.
    table.insert(
	_tContentToCall,
	require("Database.YOURMODNAMEInGenDatabaseData")
    )

    table.insert(
	_tContentToCall,
	require("Database.YOURMODNAMEPrefabData")
    )
	
    table.insert(
	_tContentToCall, 
	require("Database.YOURMODNAMEtechtreeData") 
    )
end
```

## The Lua prefabs

Up until now have been organizing prefabs in a Lua table and feeding them to ACSE through that function from a custom .lua file. While this has its pros and cons, it prevents using the prefabs from outside of this massive .lua file. The suggested method is to separate each prefab in its own file from now on.

This is what a mod would loook like in its prefab data definition:
```lua
--[[
Rename YOURMODNAME into the name of your folder
Rename SPECIESNAME into the codename of your species
NOTE: Both renames are Case-Sensitive!
]]--

local global = _G
local api = global.api
local require = global.require
local pairs = global.pairs
local Vector2 = require("Vector2")
local Vector3 = require("Vector3")
local YOURMODNAMEPrefabData = module(...)

YOURMODNAMEPrefabData.tPrefabs = {
   -- A massive confusing unorganized table of data
   .....
}

YOURMODNAMEPrefabData.AddLuaPrefabs = function(_fnAdd)
    for _, tData in global.ipairs(YOURMODNAMEPrefabData.tPrefabs) do
        for sPrefabName, tParams in global.pairs(tData) do
            _fnAdd(sPrefabName, tParams)
        end
    end
end
```

In this process we will move the prefabs out of the the database.YOURMODNAMEPrefabData.lua into single files. As a consequence, the table inside this file (and all the problems this has created) will be gone. Instead, we'll copy/paste the content of each prefab into its own file now.

First, we'll define a template for every new prefab:
```lua
-----------------------------------------------------------------------
--/  @file    PREFABNAME.lua
--/  @author  Yourself
--/  @version 1.0
--/
--/  @brief  Defines an ACSE prefab
--/
--/  @see    https://github.com/OpenNaja/ACSE
-----------------------------------------------------------------------
local global  = _G
local api     = global.api
local require = global.require
local pairs   = global.pairs
local ipairs  = global.ipairs

local PREFABNAME = module(...)

-- PropTool uses GetRoot to build the inject the prefabs in ACSE
PREFABNAME.GetRoot = function()
    -- Your prefab information goes in here
    return {}
end 

-- Relay on the current entity API to generate the complete prefab
PREFABNAME.GetFlattenedRoot = function()
    local tPrefab = api.entity.CompilePrefab( PREFABNAME.GetRoot(), 'PREFABNAME')
    return api.entity.FindPrefab('PREFABNAME')
end

return PREFABNAME
```

Save this template in Main/PREFABNAME.lua (add as many as prefabs in your mod).

This template should allow for an easy search and replace of PREFABNAME with the actual name of the prefab. You need to replace PREFABNAME with the final name of the prefab, even in the file name. For example, if your mod defines 3 prefabs (MonolophosaurusDinoFootPrint, Monolophosaurus and Monolophosaurus_01) you need 3 lua files in Main:
- Main/MonolophosaurusDinoFootPrint.lua
- Main/Monolophosaurus.lua
- Main/Monolophosaurus_01.lua

To understand what we need to move to these files, I'll start with the footprint that is small enough to see the changes.

Regardless if you have ordered the prefabs in this table or not, I'll hightlight was is important to extract. This is what the Database.YOURMODNAMEPrefabData.lua file uses to look like. There could be more or less {} around your data, but in overall will just be a list of PrefabName = PrefabData:

```lua
YOURMODNAMEPrefabData.tPrefabs = {

	MonolophosaurusDinoFootPrint = {
		Prefab = 'DinoFootprintTheropods',
		Properties = {
			Size = {
				Default = vec3_const(0.35, 0.35, 0.35)
			}
		}	
	},
        ....
```
In this example, consider the = sign,  **MonolophosaurusDinoFootPrint** is the prefab name, and everything on the right of the sign is the 'data':
```lua
  {
     Prefab = 'DinoFootprintTheropods',
     Properties = {
       Size = {
           Default = vec3_const(0.35, 0.35, 0.35)
       },
     }	
  }
```
You have to be aware of the opening and closing keys {} because we need to copy all this data into the new prefab template.lua file. This is who it would look like:
```lua
-----------------------------------------------------------------------
--/  @file    MonolophosaurusDinoFootPrint.lua
--/  @author  Yourself
--/  @version 1.0
--/
--/  @brief  Defines an ACSE prefab
--/
--/  @see    https://github.com/OpenNaja/ACSE
-----------------------------------------------------------------------
local global  = _G
local api     = global.api
local require = global.require
local pairs   = global.pairs
local ipairs  = global.ipairs
local Vector2 = require("Vector2")
local Vector3 = require("Vector3")

local MonolophosaurusDinoFootPrint = module(...)

-- PropTool uses GetRoot to build the inject the prefabs in ACSE
MonolophosaurusDinoFootPrint.GetRoot = function()
    -- Your prefab information goes in here
    -- paste the data after this return keyword
    return 
    {
       Prefab = 'DinoFootprintTheropods',
       Properties = {
         Size = {
             Default = vec3_const(0.35, 0.35, 0.35)
         },
       }	
    }
end 

-- Relay on the current entity API to generate the complete prefab
MonolophosaurusDinoFootPrint.GetFlattenedRoot = function()
    local tPrefab = api.entity.CompilePrefab( MonolophosaurusDinoFootPrint.GetRoot(), 'MonolophosaurusDinoFootPrint')
    return api.entity.FindPrefab('MonolophosaurusDinoFootPrint')
end

return MonolophosaurusDinoFootPrint
```
It is strongly recommended to use a Lua beautifier to make sure the code formatting is readable and you can check if there are any errors.

Now need to repeat the same process with the other two prefabs, in this example: Monolophosaurus and Monolophosaurus_01. I'll include the Monolophosaurus_01.lua as a guide too:

```lua
-----------------------------------------------------------------------
--/  @file    Monolophosaurus_01.lua
--/  @author  Yourself
--/  @version 1.0
--/
--/  @brief  Defines an ACSE prefab
--/
--/  @see    https://github.com/OpenNaja/ACSE
-----------------------------------------------------------------------
local global  = _G
local api     = global.api
local require = global.require
local pairs   = global.pairs
local ipairs  = global.ipairs
local Vector2 = require("Vector2")
local Vector3 = require("Vector3")

local Monolophosaurus_01 = module(...)

-- PropTool uses GetRoot to build the inject the prefabs in ACSE
Monolophosaurus_01.GetRoot = function()
    -- Your prefab information goes in here
    -- paste the data after the return keyword
    return 
    {
        Properties = {
	    MaterialPatternsName = {
	        Default = 'Monolophosaurus_PatternSet_01'
	    },
	    MaterialVariantsName = {
	        Default = 'Monolophosaurus_VariantSet_01'
	    },
	    AssetPackages = {
	        Default = {
	            __inheritance = 'Append'
	        }
	    },
	    MaterialPatternIndex = {
	        Default = 0
	    }
	},
	Components = {
	    Transform = {
	    }
	},
	Prefab = 'Monolophosaurus'
    }

end 

-- Relay on the current entity API to generate the complete prefab
Monolophosaurus_01.GetFlattenedRoot = function()
    local tPrefab = api.entity.CompilePrefab( Monolophosaurus_01.GetRoot(), 'Monolophosaurus_01')
    return api.entity.FindPrefab('Monolophosaurus_01')
end

return Monolophosaurus_01
```

Assuming you followed this process, you should have already 3 new .lua files in your Main/ package folder. Now we need to load these prefabs, however; we want to make sure we add the prefabs in order. For this we have to look into the Prefab keyword usage inside the prefab definition:
- Monolophosaurus_01 prefab has a line that says: **Prefab** = 'Monolophosaurus'
- Monolophosaurus prefab has a chunk that says: Decal**Prefab**Name = {	Default = 'MonolophosaurusDinoFootPrint' }

What this means is that Monolophosaurus_01 DEPENDS on Monolophosaurus, and Monolophosaurus DEPENDS on MonolophosaurusDinoFootPrint. Because of this dependecy tree, we need to load the prefabs in the inverse order:

- 1st MonolophosaurusDinoFootPrint
- 2nd Monolophosaurus
- 3rd Monolophosaurus_01

So back to the **Database.YOURMODNAMEPrefabData.lua** file, we will change everything inside it to this new format (Notice that the massive table of prefabs is no longer present in this file). Replace YOURMODNAME with the final mod name:

```lua
-----------------------------------------------------------------------
-- @file   Database.YOURMODNAMEPrefabData.lua
-- @author yourself
--
-- @brief  Injects the ACSE prefabs into the game
-- @see    https://github.com/OpenNaja/ACSE
-----------------------------------------------------------------------
local global  = _G
local require = global.require

-- @package Database
-- @class YOURMODNAMEPrefabData
local YOURMODNAMEPrefabData= module(...)

YOURMODNAMEPrefabData.AddLuaPrefabs = function(_fnAdd)
    -- Use one line for each prefab, make sure they are in the right order.
    _fnAdd('MonolophosaurusDinoFootPrint', require('MonolophosaurusDinoFootPrint').GetRoot())
    _fnAdd('Monolophosaurus', require('Monolophosaurus').GetRoot())
    _fnAdd('Monolophosaurus_01', require('Monolophosaurus_01').GetRoot())
end
```
After you've done all these changes, once you run the game there should not be any error compiling the prefabs. 

## Species Viewer

IF you followed this process, you have already createst the PREFABNAME.lua file required for the Species viewer. Instead of this become an extra-step, we have reduced the chances of introducing a mistake into the game by having different game and species viewer prefabs.
