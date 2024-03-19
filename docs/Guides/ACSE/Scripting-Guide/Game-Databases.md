---
title: Game Databases
icon: material/numeric-2-box
---

Lua scripting for Cobra Engine is not complicated; the problem is the context in which you run your Lua script. Some of these contexts (e.g. park managers) require the injection of your Lua script through [ACSE](https://github.com/OpenNaja/ACSE); however, there are other contexts where the game can be scripted without the need for ACSE. One of these contexts which are initialized early and available throughout the game is the Game Database.


The Cobra Engine uses a modular approach for its internal runtime database. Most of the game configuration is done and made available through the Game Database. Whether it is the cost of a lion in Planet Zoo or the list of available dinosaurs in Jurassic World Evolution, the Game Database holds this information. There is a set of database modules pre-defined in the game's main script (gamescript), but the database driver can load additional modules during the initialization process of every Content Pack.

## Using the Game Database

There are different ways to interact with the database and perform [CRUD](https://en.wikipedia.org/wiki/CRUD) operations on it while the game is running, but this will happen outside of the context of the main database and will be covered later.

For now, to access the Game Database through the exposed game API, all you need to do is require the corresponding module and call its functions; however, the content of the database depends on the game title. For example, we can get an `Island` definition from the database in Jurassic World Evolution 2 with this code:

```lua
local GameDatabase = require("Database.GameDatabase")
local tIslandData = GameDatabase.GetIslandTable('Challenge_01_Taiga')
```
The Game Database will return the `Island` information that we can now modify at our own will. There are more `Island` related functions in Jurassic World Evolution 2 available, like `AddIsland`, `RemoveIsland`, `RemoveAllIslands`, `SaveIsland`, and `LoadIsland`. These functions have been added to the Game Database by the `Island` Database Manager, which has been loaded as part of a Content Pack.

At this point, we still do not have a Lua context to run our code in.

To address this, we continue expanding our **ExampleContentPack** project from Part 1, adding database support. This step is optional and only required if we want to have our custom data loaded into the game database. In addition to having our custom Lua code added to the database, our Lua code will be executed inside the game database context. This will be our first Lua execution point for our Content Pack.

## Game Database Hot-Plug Module Implementation

The Game Database allows for hot-plugin definition in two different initialization steps, one being the content merging process and the other being the database operation.

### Game Database Content Merging

We will create a custom database module in our Content Pack to interact with the game during the database initialization process. The game will try to merge all the database information from all Content Packs. For that, the game will look for any file inside the Init or Main OVL files called 'Databases.{contentpackname}.lua" and load it.

Start with creating the following file ```ExampleContentPack\Init\Databases.ExampleContentPack.lua``` with the following content:
```lua
-- ExampleContentPack Database script
-- This script will hook into the GameDatabase content merging process

-- This little block is required for non-compiled Lua scripts. It re-defines some globals for use within the script
local global = _G
local api = global.api
local debug = api.debug
local table = global.table
local require = require
local string = string
local ExampleContentPackDatabase = module(...)

local tConfig = {
    -- Tell the main Game Database controller to load the following FDB files
    tLoad = {},
    -- Tell the game to create and/or merge the in-Game Databases 
    tCreateAndMerge = {},
}

ExampleContentPackDatabase.GetDatabaseConfig = function()
    return tConfig
end
```

This Lua script will be executed and the function GetDatabaseConfig called once during the Game Database merging process. It is still too early to have access to most of the game features, as the game data is still being loaded; however, this gives you the scaffolding to modify some of the game information without replacing the original files. 

### Game Database Files

The main Game Database Manager in Cobra Engine supports different methods to hold its data. While internally it creates a volatile SQLite database, some of the information it handles is saved as tables by their content providers. One of these examples is the `Island` Database Manager of Jurassic World Evolution 1 and 2. The `Island` data is not stored in any file and created ad-hoc in memory from a Lua table. Some other modules like the Buildings provider in the same title, stores all the building-related information in a SQLite database. These Game Databases have the extension `.fdb` and can be edited with any SQLite browser. Our recommendation is [SQLiteStudio](https://sqlitestudio.pl/).

### Modifying Existing Game Databases

This point is where the game is merging the content, and therefore it is asking to all Content Packs to provide them with any 'data' that needs to be added to the database. We can use this point in the game execution to modify or add existing data to the game, however; the data being process depends on the game title. 

For a quick test we can extract the FDB from its OVL, edit and modify the attributes we want, inject back in the OVL file using cobra-tools and save it back to its original file, but this change will stop working in the next update of the game when the files are replaced with their newer versions. 

Ideally we want our content to be merged to the original content. The overall process is to select which game FDB file(s) you want to modify, make a copy of it into your Content Pack folder, modify to whatever values you want and instruct how to load and merge this database file in our Databases.ExampleContentPackDatabase.Lua

In the case of Jurassic World Evolution 2, the game defines the price for the different buildings in a database from its main Content Pack called: ```Content0\Main\C0Buildings.fdb```. Extract this file and make a copy in our ```ExampleContentPack\Main\```, and rename the file to ```TestBuildings.fdb```

We now want to modify one of the entries in this database. Open the database, expand the table list and navigate to the table called 'Power'. This table defines how much power a building uses or produces. Lets change the power used by the Hatchery:
- Browse the data of the table 'Power'.
- Find the line that has PWR_Generator in the Building column. 
- Edit the PowerOutput in that row to 300.
- Commit and save the changes in the database.

Now we need to instruct the game to load this file and merge its contents with the existing database. Back to your Databases.ExampleContentPack.lua it is time to add information to the tConfig table. Replace the previous tConfig Table with this one and save the lua file.

```lua
local tConfig = {
    -- Tell the main Game Database controller to load the following FDB files
    -- where sSymbol is the FDB name, and the key is the name we will use
    -- to reference this FDB name. We are loading TestBuildings.fdb as 'TestBuildingsFile'.
    -- You can load different tables at this point
    tLoad = {
        TestBuildingsFile = {
            sSymbol = "TestBuildings"
        }
    },

    -- Additionally, we need to tell the game to create the in-game runtime database
    -- and merge its content. To interact with the database we need to specify the
    -- tables to look from and the prepared
    -- statements to use (the PSCollection name):
    -- If the runtime database already exists, the current data will be
    -- merged with the existing one based on the table/colum rules defined
    -- in the database.
    tCreateAndMerge = {
        -- Define the new entry here. This Key will give the name to the table in the Game Database.
        -- We are modifying the original database called 'Buildings' by the game created in content0.
        -- The in-Game Databases can be found in the content0\Init\Databases.content0.lua file.
        Buildings = {
            -- Specify our merging content, we loaded as TestBuildingsFile before. You can merge
            -- several databases here as long as they have the same structure. For now we just merge
            -- our single file.
            tChildrenToMerge = {
                "TestBuildingsFile"
            }
        },
    }
}
```

Now we need to pack both the ```Init``` folder into Init.ovl and the ```Main``` folder into Main.ovl again and launch the game, the power generated by the backup generator has changed to the value of your choice.

It is important to remove every entry in the new database that has not been modified and is not required, this will reduce merging errors.

While this method works with FDB files, other databases do not store its data in a file, instead they are stored in a Lua table provided by the database script responsible for it. 

### Adding Custom Databases

When writing a Content Pack at some point you might want to introduce your own database files too. The game engine supports that using a different scheme. This time we have to tell the Game Database that our database file needs to be added to the game and it will be the main content provider where other Content Packs can merge their information to.

#### Adding the FDB Files 

To add a custom database file to our ExampleContentPack mod, we first need to create the database. It needs to be a SQLite3 database and saved with the .fdb extension in the Main folder and we will name it ```ExampleContent\Main\TestCustomData.fdb```. 

Open the database FDB file and for this example we will create a table called 'TestTable1' With three columns:
- Column name: "ID", type integer, Primary Key, Unique, Not Null
- Column name: "Name", type string
- Column name: "Value", type string

This SQL sentence will create the table for you:
```
CREATE TABLE TestTable1 (
    Id    INTEGER UNIQUE
                  NOT NULL
                  PRIMARY KEY,
    Name  STRING,
    Value STRING
);
```

We want to have our table populated with some values, so lets go ahead an create a few entries, using IDs starting from 1001 (later we will query the table for these values). In this example I'll add the following entries:
|  ID  | Name  |  Value |
|------|-------|--------|
| 1001 | Name1 | Value1 |
| 1002 | Name2 | Value2 |

Note: these values and Ids are not relevant, they are just to showcase the use of a custom database.

Back to our ```ExampleContentPack\Init\Databases.ExampleContentPack.lua``` file, it is time to introduce the new FDB file in the game. Edit the lua file and modify the tConfig table to include the following:

```lua
local tConfig = {
    -- Tell the main Game Database controller to load the following FDB files
    -- where sSymbol is the FDB name, and the key is the name we will use
    -- to reference this FDB name. We are loading TestBuildings.fdb as 'TestBuildingsFile'.
    -- Additionally, we are loading our custom FDB file as well
    tLoad = {
        TestBuildingsFile = {
            sSymbol = "TestBuildings"
        },
        TestCustomDataFile = {
            sSymbol = "TestCustomData"
        }
    },

    -- Additionally, we need to tell the game to create the in-game runtime database
    -- and merge its content. To interact with the database we need to specify the
    -- tables to look from and the prepared
    -- statements to use (the PSCollection name):
    -- If the runtime database already exists, the current data will be
    -- merged with the existing one based on the table/colum rules defined
    -- in the database.
    tCreateAndMerge = {
        -- Define the new entry here. This Key will give the name to the table in the Game Database.
        -- We are modifying the original database called 'Buildings' by the game created in content0.
        -- The in-Game Databases can be found in the content0\Init\Databases.content0.lua file.
        Buildings = {
            -- Specify our merging content, we loaded as TestBuildingsFile before. You can merge
            -- several databases here as long as they have the same structure. For now we just merge
            -- our single file.
            tChildrenToMerge = {
                "TestBuildingsFile"
            }
        },

        -- Define the new entry here. This Key will give the name to the table in the Game Database.
        -- This time are creating a new database instead of modifying an existing one, so the entry
        -- will look a bit different.
        -- ExampleTestData is the name of table the game will create for us.
        ExampleTestData = {
            -- Specify Which one of the database files is to be considered the first one
            -- One to which other databases can merge to. We associated our custom FDB file 
            -- to the key: 'TestCustomDataFile'
            FirstChild = "TestCustomDataFile"
            -- Specify one or more Prepared Statement Collections to operate with
            -- this database. For the game to access the data in the FDB file, it needs a set of 
            -- Prepared Statements. This list of statements will be associated to the table
            -- internally by the Game Database
            tCollections = {"ExampleContentPackPSList"},			
            -- Additionally, we could just specify specific Prepared Statements to be assigned 
            -- to this database adding their names to the statements table.
            -- tStatements = { "PreparedStatementName"}
        }
        
    }
}
```

With this new config table in our database merging code, the game will load an FDB, assign it a table and associate the Prepared Statements with the database. But before we can use this new database, we need to create the Prepared Statement Collection.

#### Adding a Prepared Statement Collection

Prepared Statements are predefined SQL queries to interact with a database. It can support any number of arguments and operate with many different tables. The only difference to raw SQL queries is that they have been predefined, they have type constrains in their arguments and are less prone to fail because they are not build randomly. They are static and can't be modified. 

During this example we have added a database with a table called 'TestTable1', with columns 'Id', 'name' and 'value'. We need to create a collection of Prepared Statements based on the interactions we expect to have with this database. For this example we will have:
- A SQL Query to load all TestTable1 ID different values. It does not need arguments.
- A SQL Query to find an ID based on the Name. It will need one argument of type String.
- A SQL Query to find a Value based on an ID. It will need one argument of type Int.
- A SQL Query to update a value based on an ID. It will need two arguments, Int for the ID and string for the new value.

Cobra-tools treats PSCollections as an XML file, and therefore they are easy to craft manually with any editor. Based on the previous list of SQL queries, we will create the ```ExampleContentPack\Init\ExampleContentPackPSList.pscollection``` file and edit with a text editor. Add the following content to it:

```xml
<PscollectionRoot game="Games.JURASSIC_WORLD_EVOLUTION_2">
    <prepared_statements pool_type="4">
        <preparedstatement>
            <args />
            <statement_name>GetAllIdFromTestTable1</statement_name>
            <sql_query>SELECT id FROM TestTable1;</sql_query>
        </preparedstatement>
        <preparedstatement>
            <args pool_type="4">
                <arg arg_type="3" arg_index="1" />
            </args>
            <statement_name>GetTestTable1IdFromName</statement_name>
            <sql_query>SELECT id from TestTable1 WHERE name=?1;</sql_query>
        </preparedstatement>
        <preparedstatement>
            <args pool_type="4">
                <arg arg_type="0" arg_index="1" />
            </args>
            <statement_name>GetTestTable1ValueFromId</statement_name>
            <sql_query>SELECT value from TestTable1 WHERE id=?1;</sql_query>
        </preparedstatement>
        <preparedstatement>
            <args pool_type="4">
                <arg arg_type="0" arg_index="1" />
                <arg arg_type="3" arg_index="2" />
            </args>
            <statement_name>SetTestTable1ValueForId</statement_name>
            <sql_query>UPDATE TestTable1 SET value=?2 WHERE id=?1;</sql_query>
        </preparedstatement>
</PscollectionRoot>
```

> `arg_type` 0 indicates an integer value  
  `arg_type` 2 indicates a float value  
  `arg_type` 3 indicates a string value.  
  `arg_index` is the order; `arg_index="1"` belongs to the Prepared Statement parameter ?1, and so on.  

We could add more SQL Queries to the PSCollection as we need. Some in-game databases have dozens of statements in their Prepared Statements collection, but for now as an example these will be enough.

At this point we can re-pack our Init.ovl and Main.ovl files. Our Content Pack will load and modify the existing Buildings database, and add a custom FDB database to the game. All this happens during the Game Database bootstrap/initialization process. However, we are still unable to make use of our custom FDB data. Our Lua injection is happening too early in the database merging process and at this point probably not all the game tables have been populated with their final data.


## Database Managers

To provide the game with support for the different data, Content Packs can inject custom Database Managers into the main game. Each one of these managers will be responsible for their data, whether it is in a FDB file or a Lua table, or every other method available. The main game script will define a set of 'hardcoded' Database Managers it is expecting, however; additional Database Managers can be provided from a Content Pack. In this example we have added a custom FDB file to the game, now it is time to provide the game with access to this information through a custom Database Manager. 

### Creating a Database Main Loader

After the early initialization content merging process, the Game Database will later look for Content Pack Lua database controllers through its modular system. Each Content Pack can define one or more Database Managers but initially it will look for a default one. It is time we go back to our Main content folder and create the ```ExampleContentPack\Main\Database.ExampleContentPackLuaDatabase.lua``` file, with the following content:
```lua
local global = _G
local table = global.table
local require = require
local ExampleContentPackLuaDatabase = module(...)

-- AddContentToCall is the hot-plug mechanism used by the Game Database to help Content Packs
-- attach their own Database Managers to the game.
ExampleContentPackLuaDatabase.AddContentToCall = function(_tContentToCall)
    -- We tell the Database Manager to load our custom Database Manager by its Lua name
    -- You can add as many as you want, ideally separating each manager for each content type you add
    table.insert(_tContentToCall, require("Database.ExampleContentDatabaseManager"))
end
```

With this file, the Game Database now Knows it needs to look for a file called: Database.ExampleContentDatabaseManager, so go ahead and create the ```ExampleContentPack\Main\Database.ExampleContentDatabaseManager.lua``` file, with the following content:
```lua
-- This file is responsible of managing the data inside the TestCustomData.fdb and providing it to the game
local global = _G
local api = global.api
local pairs = pairs
local ipairs = ipairs
local type = type
local table = global.table
local tostring = global.tostring
local GameDatabase = require("Database.GameDatabase")
local ExampleContentDatabaseManager = module(...)

--
-- Initialization functions. These functions are called during the initialization process only
--

-- This method will be called when our manager gets initialized, early in the game launch after
-- all data has been merged for all the Content Packs. This method allows our manager to know
-- the database is getting initialized.
ExampleContentDatabaseManager.Init = function()

end

-- This table contains the list of functions our module wants to add to the Game Database.
ExampleContentDatabaseManager.tDatabaseFunctions = {}

-- This method will be called when our manager gets initialized to inject custom functions 
-- in the Game Database. These functions will be available for the rest of the game Lua modules.
ExampleContentDatabaseManager.AddDatabaseFunctions = function(_tDatabaseFunctions)
    for sMethod,fnMethod in pairs(ExampleContentDatabaseManager.tDatabaseFunctions) do
        _tDatabaseFunctions[sMethod] = fnMethod
    end
end

-- This method will be called after our manager gets initialized, all Database and Player methods have 
-- been added to the main Game Databases.
ExampleContentDatabaseManager.Setup = function()

end

--
-- Database active functions. These functions are optional and can be called while our Database Manager is active.
--
-- Nothing included yet.


--
-- De-initialization functions. These functions are called during the shutdown or restart processes only
--

-- This method will be called when the Game Database is shutting down for re-initialization. It is a soft Re-Init
-- of the database. We don't need to close or free resources if we don't want, but remember we have them open when
-- the Game Database calls our :Init() function again.
ExampleContentDatabaseManager.ShutdownForReInit = function()

end

-- This method will be called when the Game Database is shutting down and we need to close any 
-- or free any resource we have open. The module will be unloaded after.
ExampleContentDatabaseManager.Shutdown = function()

end

```

The file above is a good template for a Database Manager. Database Managers can have more hooks used by the game, but for our current purpose we will limit the template to what we need. This file will be loaded by the Database Manager and the different methods will get called in the following order:

1. `Setup()`
2. `AddDatabaseFunctions()`
3. `Init()`

### Adding GameDatabase Functions

It is time to add our custom database functions to the game. We created SQL queries above to:

1. Get all TestTable1 IDs
2. Look up a TestTable1 ID based on a name
3. Find a value based on a TestTable1 ID
4. Update an entry value for a TestTable1 ID

We will create four functions to provide this functionality through the Game Database.

Start with populating the `ExampleContentDatabaseManager.tDatabaseFunctions` table in the ```ExampleContentPack\Main\Database.ExampleContentDatabaseManager.lua``` file with the following content:
```lua
ExampleContentDatabaseManager.tDatabaseFunctions = {
    -- This function will return all the Ids inside TestTable1 of TestCustomData.fdb
    GetAllTestDataIds = function()
        return ExampleContentDatabaseManager._GetAllTestDataIds()
    end,
    -- This function will return the Id for a name inside TestTable1 of TestCustomData.fdb
    GetTestDataIdFromName = function(_sName)
        return ExampleContentDatabaseManager._GetTestDataIdFromName(_sName)
    end,
    -- This function will return the value for an Id inside TestTable1 of TestCustomData.fdb
    GetTestDataValueFromId = function(_nId)
        return ExampleContentDatabaseManager._GetTestDataValueFromId(_nId)
    end,
    -- This function will set the value for an Id inside TestTable1 of TestCustomData.fdb
    SetTestDataValueFromId = function(_nId, _sValue)
        return ExampleContentDatabaseManager._SetTestDataValueFromId(_nId, _sValue)
    end
}
```
Each one of these GameDatabase functions calls another function (defined below) to perform each custom database query through the Prepared Statements we added before. 

The functions called by the above GameDatabase functions will be defined in the following code:

```lua
-- The following code utilizes the Game Database Lua component to perform SQL queries on the Game Database.
-- Read each one to understand how to use the Prepared Statements in-game interface when interacting with a database.
--
-- Custom Database API
--

ExampleContentDatabaseManager._GetAllTestDataIds() = function
    local result = nil
    local database = global.api.database

    -- We called our database 'ExampleTestData' in the Databases.ExampleContentPack.Lua file
    -- We created a Prepared Statement called 'GetAllIdFromTestTable1'
    local cPSInstance = database.GetPreparedStatementInstance("ExampleTestData", "GetAllIdFromTestTable1")
    if cPSInstance ~= nil then
        database.BindComplete(cPSInstance)
        database.Step(cPSInstance)
        result = database.GetAllResults(cPSInstance, false)
    end

    return result
end

-- This function will search the database for rows with the name = _sName and return
-- the first match. _sName has to be a string.
ExampleContentDatabaseManager._GetTestDataIdFromName  = function(_sName)
    local result = nil
    local database = global.api.database
    
    -- We called our database 'ExampleTestData' in the Databases.ExampleContentPack.Lua file
    -- We created a Prepared Statement called 'GetTestTable1IdFromName'
     local cPSInstance = database.GetPreparedStatementInstance("ExampleTestData", "GetTestTable1IdFromName")
     if cPSInstance ~= nil then
        database.BindParameter(cPSInstance, 1, _sName)
        database.BindComplete(cPSInstance)
        database.Step(cPSInstance)
        local tRows = database.GetAllResults(cPSInstance, false)
        result = tRows[1] or nil
    end

    return result
end

-- This function will search the database for rows with the Id = _sId and return
-- the first match. _sId has to be a number.
ExampleContentDatabaseManager._GetTestDataValueFromId = function(_nId)
    local result = nil
    local database = global.api.database
    
    -- We called our database 'ExampleTestData' in the Databases.ExampleContentPack.Lua file
    -- We created a Prepared Statement called 'GetTestTable1ValueFromId'
     local cPSInstance = database.GetPreparedStatementInstance("ExampleTestData", "GetTestTable1ValueFromId")
     if cPSInstance ~= nil then
        database.BindParameter(cPSInstance, 1, _sId)
        database.BindComplete(cPSInstance)
        database.Step(cPSInstance)
        local tRows = database.GetAllResults(cPSInstance, false)
        result = tRows[1] or nil
    end

    return result
end

ExampleContentDatabaseManager._SetTestDataValueFromId = function(_nId, _sValue)
    local result = nil
    local database = global.api.database
    
    -- Before we try to change the database we need to enable writing mode to it.
    -- By default all databases are Read-Only after they are being loaded and merged.
    database.SetReadOnly("ExampleTestData", false)

    -- We called our database 'ExampleTestData' in the Databases.ExampleContentPack.Lua file
    -- We created a Prepared Statement called 'SetTestTable1ValueForId'
     local cPSInstance = database.GetPreparedStatementInstance("ExampleTestData", "SetTestTable1ValueForId")
     if cPSInstance ~= nil then
        database.BindParameter(cPSInstance, 1, _sId)
        database.BindParameter(cPSInstance, 2, _sName)
        database.BindComplete(cPSInstance)
        database.Step(cPSInstance)
        local tRows = database.GetAllResults(cPSInstance, false)
        result = tRows[0] or nil
    end

    -- Before returning, lock the database again.
    database.SetReadOnly("ExampleTestData", true)

    return result
end

```

With this finished, re-pack the Init.ovl and Main.ovl files and try again. We have modified the Game Database API, with newly created functions provided by our own custom Database Manager module.

Once our module has been initialized, our API methods will be added to the main Game Database, and any module can use them with the following code snippet:
```lua
local GameDatabase = require("Database.GameDatabase")
local tIds = GameDatabase.GetAllTestDataIds()
local tId  = GameDatabase.GetTestDataIdFromName("Name1")
```

## Modifying Other Content Pack Databases

We have seen before how to merge our custom content data into another Content Pack database. However due to the merging process, another Content Pack can overwrite our changes if it is loaded after our Content Pack. With the use of Prepared Statements it is possible to have access to other databases after the content merging process has been completed. 

Initially we modified the Buildings module increasing the power produced by the backup generator. We can do it again, but this time without needing any extra FDB file.

First we need a custom Prepared Statement to modify the appropriate table. So we start by creating a new Prepared Statement Collection called ```ExampleContentPack\Init\ExampleBuildingsPSList.pscollection``` file and editing with a text editor. Add the following content to it:

```xml
<PscollectionRoot count="1" game="Games.JURASSIC_WORLD_EVOLUTION_2">
    <preparedstatement arg_count="2">
        <args pool_type="4">
            <arg arg_type="3" arg_index="1" />
            <arg arg_type="0" arg_index="2" />
        </args>
        <statement_name>SetPowerOutputForBuildingName</statement_name>
        <sql_query>UPDATE Power SET PowerOutput=?2 WHERE Building=?1;</sql_query>
    </preparedstatement>
</PscollectionRoot>
```

Now, back to our ```ExampleContentPack\Main\Database.ExampleContentDatabaseManager.lua```, we will modify our `Setup()` to update the Building's power after the merging process has completed. It should look like this:

```lua
-- This method will be called after our manager gets initialized, all Database and Player methods have 
-- been added to the main Game Databases.
ExampleContentDatabaseManager.Setup = function()
    -- Get access to the Game Database interface
    local database = global.api.database

    -- Before we try to change the database we need to enable writing mode to it.
    -- By default all databases are Read-Only after they are being loaded and merged.
    database.SetReadOnly("Buildings", false)

    -- We need to bind our new Prepared Statement Collection to the Buildings database before
    -- we can use any of its statements.
    local bSuccess = database.BindPreparedStatementCollection("Buildings", "ExampleBuildingsPSList")
    if bSuccess == 0 then return nil end

    -- We created a Prepared Statement called 'SetTestTable1ValueForId'
    local cPSInstance = database.GetPreparedStatementInstance("Buildings", "SetPowerOutputForBuildingName")
    if cPSInstance ~= nil then
        database.BindParameter(cPSInstance, 1, "PWR_Generator") -- first argument, string
        database.BindParameter(cPSInstance, 2, 123)             -- second argument, number
        database.BindComplete(cPSInstance)
        database.Step(cPSInstance)
        database.GetAllResults(cPSInstance, false)
    end

    -- Before returning, lock the database again
    database.SetReadOnly("Buildings", true)
end
```

Now re-pack both the Init.ovl and the Main.ovl files again, and the Backup Generator will always produce 123 units regardless of the value in any of the Building databases loaded during the merging process. The same Prepared Statement can be used to modify other building power outputs; just run the query several times with different values. Consider creating a function in the main database controller to clean up and centralize your code.

We haven't finished with the Game Databases yet, but the next topic covers a completely different area of database controllers and therefore needs to be split from this tutorial.
