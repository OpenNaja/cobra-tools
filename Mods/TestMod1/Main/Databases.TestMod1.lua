-----------------------------------------------------------------------
--  @file    Databases.TestMod1.lua
--  @author  open-naja
--  @version 1.0
--
--  @brief  Defines the TestMod1 items merging into the different 
--          database configurations. Requires ACSE > 0.713 to work.
--
--  @see    https://github.com/OpenNaja/ACSE
-----------------------------------------------------------------------
local global = _G

--/ Create the custom module for the package Init.
local TestMod1DatabaseConfig = module(...)

-- @brief GameDatabase hook to add load and merge custom databases
TestMod1DatabaseConfig.GetDatabaseConfig = function()

    -- Do not load any database if ACSE is not correctly installed.
    if not global.api.acse or global.api.acse.versionNumber < 0.713 then
        return {}
    end 

    -- Process the following fdb files and merge them with the game databases
    return {
        tLoad = {
            TestMod1Test = {sSymbol = "TestMod1Test" },
        },
        tCreateAndMerge = {
            Test = { tChildrenToMerge = {"TestMod1Test"} },
        }
    }

end