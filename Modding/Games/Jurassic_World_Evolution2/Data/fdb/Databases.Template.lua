-----------------------------------------------------------------------
--  @file    Databases.${Name}.lua for Planet Zoo
--  @author  open-naja
--  @version 1.0
--
--  @brief  Defines the ${Name} items merging into the different 
--          database configurations. Requires ACSE > ${ACSE} to work.
--
--  @see    https://github.com/OpenNaja/ACSE
-----------------------------------------------------------------------
local global = _G

--/ Create the custom module for the package Init.
local ${Name}DatabaseConfig = module(...)

-- @brief GameDatabase hook to add load and merge custom databases
${Name}DatabaseConfig.GetDatabaseConfig = function()

    -- Do not load any database if ACSE is not correctly installed.
    if not global.api.acse or global.api.acse.versionNumber < ${ACSE} then
        return {}
    end 

    -- Process the following fdb files and merge them with the game databases
    return {
        tLoad = {
${tLoad}        },
        tCreateAndMerge = {
${tMerge}        }
    }

end