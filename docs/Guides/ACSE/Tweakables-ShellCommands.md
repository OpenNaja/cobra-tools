---
title: Tweakables and Shell Commands
---

!!! note
    The functionality explained here requires [ACSE](https://opennaja.github.io/ACSE/) installed in the game to work.

## Introduction

When developing a Mod, it is important to have several facilities that can assist you to trigger certain events, execute certain code or being able to tweak a few parameters without having to build the Mod and launch the game again, or reaching certain gampleay situation for the events to happen the natural way. For this Cobra Engine uses two different features in development that we have reintroduced through ACSE: Tweakables and Shell Commands.

## Tweakable variables

Tweakable variables (from now on Tweakables) is a method to define a variable for your Mod that can be altered with ACSE debug functions. ACSE will register all the Tweakables created by any Manager, Component or database, and exposed them through the ACSE Debug UI. They can later be list and modified from the Debug console with the 'ListTweakables' and 'SetTweakable' commands.

### Creating a Tweakable variable.
Tweakables can have different types, and currently ACSE supports: Integer, Float and Boolean. These are some examples of how to define Tweakable variables:

```Lua
local f_MyFloatValue1 = api.debug.CreateDebugTweakable( api.debug.Tweakable_Float, "Testing.variables.floatvalue1", 60, 0.5, 1000, 1)
local b_MyBoolValue1  = api.debug.CreateDebugTweakable( api.debug.Tweakable_Bool, "Testing.variables.Boolean1", true)
local i_MyIntValue1   = api.debug.CreateDebugTweakable( api.debug.Tweakable_Int32, "Testing.OtherCategory.Intval1", 1, 1, 100, 1)
```
The arguments to create a Tweakable are:
- Type: any of Tweakable_Float, Tweakable_Bool, Tweakable_Int32, Tweakable_UInt32, Tweakable_Int64, Tweakable_UInt64, Tweakable_fVector1
- Name: whatever string name you want to use, it is better to use a clear name based on the variable functionality.
- Default value: (must be in the type of the Tweakable) a float, boolean, etc.
- Minimum value: minimum value of this variable
- Maximum value: maximum value of this variable
- Step value: Step value (to move between minimum and maximum value).

CreateDebugTweakable will create a global variable object and will return that object from the call. When attempting to create an already existing Tweakable, the function will return the existing one.

### Accessing a Tweakable variable

To read or write the value from a Tweakable all you need to do is call any of the functions:
- GetValue() will return the current value casted to the Tweakable type.
- SetValue(value) will store a new value. Needs to be casted to the right type.

So, following with our previous examples, valid ways to access the Tweakables we just created are:

```Lua

  api.debug.Trace(" The value of f_MyFloatValue1 is " .. tostring( f_MyFloatValue1:GetValue() ))

  local int = 10 + i_MyIntValue1:GetValue()

  if b_MyBoolValue1:GetValue() == true then b_MyBoolValue1:SetValue(false)

```
You are just free to use them in your code as normal variables. The only difference is that they are global and can be modified from outside your code, for example through the ACSEDebug console. Example of the commands to modify these Tweakables are:

```
 SetTweakable Testing.OtherCategory.Intval1 15
 SetTweakable Testing.variables.floatvalue1 6.5
 Testing.variables.Boolean1 false
```

## Shell Commands

Shell Commands are predefined functions that allow to execute certain actions on demand. There are some default commands introduced by ACSE, but since these actions are game-dependant usually they are provided from external mods. Examples of these commands (and how specific they are) for Jurassice World Evolution 2 include spawning a custom dinosaur, starting/stopping a storm, or loading an island save file. Other commands could be generic enough to work on all games, including a command to retrieve the localized version of a string, or to list all the loaded prefabs by the engine.

SetTweakable is another shell command that is provided by ACSE itself, allowing the modification of any Tweakable variable. Some commands will have/need arguments to operate, and some of these arguments may be optional. Arguments are defined by type, for example {uint32} or {float}, and to make them optional they will be surounded by brackets [{string}].

This is a list of existing commands as a sample:

- PrintDigSites
- DisplaySubtitle {string} {float}
- OrbitEntityIDCamera {uint32}
- ListCommands [{string}]
- ListTweakables [{string}]
 
To get more information about a command you can type ``Help commandName`` in the debug console, and it will return a detailed description of the command and its arguments. For example, ListTweakables will display the entire list of known Tweakables, and if you specify a string it will use that string to filter the output to include only Tweakables that have that string in their name. Other commands require all their arguments to work, for example DisplaySubtitle requires both a subtitle name and the time in seconds to keep the text displayed.

### Creating a Shell Command

To create a shell command you will need to call the api.debug.RegisterShellCommand function:

```Lua
   local command1 = api.debug.RegisterShellCommand(
      function(tEnv, tArgs)
        -- do something
        return 
      end,
      "ResetCurrentIsland", 
      "Reset the state of the current island to its starting state\n"
    )
```
The arguments for RegisterShellCommand are:
- Function to be executed when the command is issued.
- Command definition string: will include the command Name and/or any arguments required defined by type.
- Command description text.

This is a more complex definition of a command including optional and required arguments:
```Lua
   local command2 = api.debug.RegisterShellCommand(
      function(tEnv, tArgs)
        -- do something
        return 
      end,
      "Storm start|stop {string} [{float}]", 
      "Starts the storm specified by name in the first argument or stops the current active storm\n"
    )
```
It is important to save the shell command object returned by RegisterShellCommand and destroy when the code wont be available anymore (e.g. if you have a manager or a database controller, you will create your Shell Commands on Init() and destroy then on Shutdown(), or any attempt to execute the commands will fail and possible crash the game.

### Removing a shell command

When your code wont be available anymore, you can destroy the existing commands by calling api.debug.UnregisterShellCommand( CommandObject ). The argument for this function is the object created by RegisterShellCommand. Following up with the examples, you will destroy these commands by calling:

```Lua
api.debug.UnregisterShellCommand( command1 ) 
api.debug.UnregisterShellCommand( command2 ) 
```
Note: it is important to unregister all the Shell Commands you have created.

### Executing a shell command

You can execute Shell Commands from either the debug console or through code, calling api.debug.RunShellCommand( commandString). Some examples could be (assuming the commands do exist):

```Lua
  api.debug.RunShellCommand("SetTweakable Testing.OtherCategory.Intval1 15")
  api.debug.RunShellCommand("Game.Quit")
```
In the debug console all you have to do is type the command and press enter.

### Anatomy of a shell command.

Lets go back for a second to the definition of a shell command

```Lua
   local command2 = api.debug.RegisterShellCommand(
      function(tEnv, tArgs)
        -- do something
        return 
      end,
      "Storm start|stop {string} [{float}]", 
      "Starts the storm specified by name in the first argument or stops the current active " ..
      "storm immediately or after the seconds specified by the second argument\n"
    )
```

This command is defined to accept two or there arguments, if there is a second argument it will be a string name of the storm type, if there is a third argument it will be a float value. The command function will receive the arguments in the tArgs table, and will also receive a copy of the current world Environment table in case it needs to access any of the current active managers through their interfaces.

Imagine a different command, one that actually uses the game API and is easier to implement.

```Lua
   local command3 = api.debug.RegisterShellCommand(
      function(tEnv, tArgs)
        if #tArgs < 1 then
            api.debug.Trace("ParkControl requires an action between: open or close")
            return
        end
        if type(tArgs[1]) ~= "string" or tArgs[1]~= 'open' or tArgs[1] ~= 'close' then
            api.debug.Trace("Wrong door control command, use open or close")
            return
        end
        
        -- perform action:
        local worldAPI = api.world.GetWorldAPIs()
        local parkAPI  = worldAPI.park
        
        if tArgs[1] == 'open' then
           ParkAPI:SetParkOpenForGuests(true)
        end
        if tArgs[1] == 'close' then
           ParkAPI:SetParkOpenForGuests(false)
        end
        return 
      end,
      "ParkControl open|closed", 
      "opens or closes the park for guests\n"
    )
```
In your custom commands you want to have at least the minimum fail safe for argument checking so you don't crash the game for using a command incorrectly. 

You can add as many commands as you want, but ideally you want to have commands that helps you speeding up your modding requirements. For example, a command to control storms is useful if you plan to develop a mod that adds or modifies the existing storm system, or if you are working on a mod that modifies the storm damage. This way you don't need to wait for a storm to come randomly to check your modding results.

Finally remember that you need to Unregister the commands when your module is no longer available to avoid misuses or even the game crashing.

Both Tweakables and Shell Commands can be very useful for modding purposes, allowing you to change values and create states without forcing you to test-play everything.
