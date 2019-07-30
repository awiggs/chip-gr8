# Overview

Chip-Gr8 is distributed through [pip](https://pypi.org/project/pip/)! To install run

```readonly-nolines
pip install chipgr8
```

Currently Chip-Gr8 only supports python 3.6 and 3.7. We provide binaries for Chip-Gr8's backend for Windows users with the following configurations: Python36 (32 and 64 bit) and Python37 (32 and 64 bit). For Mac and Linux users `pip install` should build the backend binaries using your system's compiler.

For additional documentation see the [Chip-Gr8 Reference Manual](../static/Chip-Gr8-Reference-Manual.pdf).

# Writing Your First Agent

This example will help you write your first AI agent. An AI agent performs two key tasks, observations and actions. To get started import the Chip-Gr8 API, and a game object. The game objects provide useful defaults for observations, actions, as well as the correct ROM name. For this example we will use the game Squash. Squash is a single player Pong. We will also import random for later.

```lang:python-readonly
import random
import chipgr8
from chipgr8.games import Squash
```

AI agents are trained and run in loops. This is typically done with a while loop where you wait for a CHIP-8 VM instance to be done. For our first agent let's just pick a random action. In order to run this agent we will need to create a VM instance to run it on and load the Squash ROM.

```lang:python-readonly
vm = chipgr8.init(ROM=Squash.ROM)
```

By default the API returns a VM appropriate for running a single AI. We will now create a loop where we repeatedly choose a random action. `Squash.actions` provides a list of all the valid Squash game actions. We also need to indicate when the VM instance should be considered done. The Squash object also provides this in its set of observations, so we will observe the VM and check to see if the VM is done.

```lang:python-readonly
while not vm.done():
    vm.act(random.choice(Squash.actions))
    observations = Squash.observe(vm)
    vm.doneIf(observations.done)
```

Our AI will now run, but we will not be able to see it perform any of its actions. We can watch a replay using the `.inputHistory` of our VM. The `.go()` method will loop the VM instance for us.

```lang:python-readonly
vms = chipgr8.init(ROM=Squash.ROM, instances=100)
```

We can now iterate over the vms and run each one like we did before.

```lang:python-readonly
chipgr8.init(
    ROM=Squash.ROM,
    inputHistory=vm.inputHistory,
    display=True
).go()
```

Our AI is not very good, but we can easily make it better just by running multiple random AI agents and picking the best one. Let’s start by creating 100 VM instances.

```lang:python-readonly
while not vms.done():
    for vm in vms:
        vm.act(random.choice(Squash.actions))
        observations = Squash.observe(vm)
        vm.doneIf(observations.done)
```

This approach is a little slow though since we have to run every VM instance as part of the same process. We can take advantage of a machine's multiple cores by using the VMs `.inParallel()` method. This method requires us to refactor our code a little bit. This method expects a function which will be called repeatedly until the vm instance is done. We can do this by taking our inner section of the loop and turning it into a function.

```lang:python-readonly
def action(vm):
    vm.act(random.choice(Squash.actions))
    observations = Squash.observe(vm)
    vm.doneIf(observations.done)

vms.inParallel(action)
```

We can now just pick the best vm of the bunch. The Squash object thankfully has another observation that can help us: score. We can use the VMs `.maxBy()` function to get the best VM.

```lang:python-readonly
best = vms.maxBy(lambda vm : Squash.observe(vm).score)
```

We can now watch this VM like we did before using its `inputHistory`. Congratulations on writing your first Chip-Gr8 AI agent! You can find the final code altogether below.

```lang:python-readonly
import random
import chipgr8
from chipgr8.games import Squash

# This action is performed repeatedly until the VM is done
def action(vm):
    vm.act(random.choice(Squash.actions))
    observations = Squash.observe(vm)
    vm.doneIf(observations.done)

# Create 100 CHIP-8 VM instances
vms = chipgr8.init(ROM=Squash.ROM, instances=100)
# Run all our random agents
vms.inParallel(action)
# Pick the best one
best = vms.maxBy(lambda vm : Squash.observe(vm).score)

# Show a replay of the best
chipgr8.init(
    ROM=Squash.ROM,
    inputHistory=best.inputHistory,
    display=True
).go()
```

# Querying Memory

In order to support more games, or find additional values from CHIP-8 RAM for games already included with Chip-Gr8, components are provided for querying memory. These components are meant to be used in a workflow like the following:

 1. Start the Chip-Gr8 display with the ROM you want to query.
 2. Put the VM into a state you understand.
 3. Create a `Query` object and use a predicate to limit the number of matching memory addresses.
 4. Change the VM to a new state and use a new predicate to further filter the results.
 5. Repeat step 4 until there is only a single address that matches.
 6. Copy the `Query` out to a file.

Several steps are made easier by the fact that `Query` and `Observer` objects will print their own source code in the REPL. You can easily write these to a file using the write function.

## Queries

Queries provide several predicates to limit matched memory addresses, like `.eq()`, `.dec()`, `.lte()`, etc. A list of all memory addresses, along with their previously queried values can be found using the `.previous` field. For example:

```lang:python-readonly
q = Query(vm)
q.eq(0x04)
print(q.previous)
```

You can instantiate a finished `Query` by providing an address instead of a VM instance. For example, to create a query that looks at address 0x200:

```lang:python-readonly
q = Query(0x200)
```

This `Query` can now be used to retrieve the value in CHIP-8 RAM at 0x200 of any VM instance with:

```lang:python-readonly
q.observe(vm)
```

## Observers

Queries can be combined using an `Observer`. An `Observer` is just a collection of queries and functions that provides one method, observe, which applies all these queries and functions to a provided VM instance and returns the result as a `NamedList`. A `NamedList` is a data structure that behaves like a Python list, but can be accessed by attributes and keys. For example, to create a list of one element, y, with a key, `key`

```lang:python-readonly
myNamedList = NamedList(['key'], [7])

# To access the element you can use the following ways:
myNameList[0]     # By index
myNameList.key    # By attribute
myNameList['key'] # By key
```

To add queries to an `Observer` you can call `.addQuery()`. This method also accepts as the query a function that takes two arguments. The first argument is a collection of all non-function observations. The second is the VM instance. This allows you to create combinational queries. For example

```lang:python-readonly
o = Observer()
o.addQuery('lives', Query(0x115))
o.addQuery('done',  lambda o, vm : o.lives == 0)
```

## Games
Games provide actions, observations, and a ROM all in one package. Several games are provided out of the box, but you can also create your own game objects for ROMs not included with Chip-Gr8.

# API Reference

## Constants

### `defaultBindings`

Default key bindings for the Chip-Gr8 display as a Python dictionary.

### `themes`

A Python dictionary of the builtin Chip-Gr8 themes.

## Functions

### `assemble(source=None, inPath=None, outPath=None)`
Converts assembly `source` code, or source code contained in `inPath` into binary data (a ROM). This ROM may optionally be written to file with the `outPath` argument.

### `disassemble((Parameters))`
Converts a binary ROM into an assembly source file. Returns the source. Provides option for disassembling with labels and special format.

##### Parameters

##### `buffer=None`
The binary ROM to disassemble as a set of bytes. Optional if `inPath` is provided.

##### `inPath=None`
The path to a binary ROM to disassemble. Optional if `buffer` is provided.

##### `outPath=None`
If the path is provided, the source code is written to that file.

##### `labels={}`
A dictionary used to generate labels. If None is passed, labels will not be generated in the source.

##### `decargs=True`
If True, instruction numerical operands will be output in decimal rather than hexadecimal.

##### `srcFormat='{label}{labelSep}{prefix}{instruction}\n'`
A format string for lines of source code. Can contain the following variables `label`, `labelSep`, `prefix`, `instruction`, `addr`, and `dump`. For example for hexdump with address use:

```lang:python-readonly
srcFormat='{addr} {dump}'
```

##### `labelSep = '\n  '`
The string used to separate labels from instructions.

##### `prefix=' '`
The string used to prefix all instructions.

##### `addrTable={}`
A table that will have addresses as keys and instructions as values.

##### `findROM(rom)`
Returns the path to `rom` if it is one of the included ROMs.

##### `hexdump(buffer=None, inPath=None, outPath=None)`
Dumps a `buffer` or file at `inPath` as a set of 16-bit hexadecimal values on each line (the number of bits that correspond to a CHIP-8 instruction). Writes the data to `outPath` if provided.

### `init((Parameters))`
Returns an instance of `Chip8VM` or `Chip8VMs`. Used to configure the virtual machines for a user or a given AI agent.

#### Parameters

##### `ROM=None`
If provided will load a ROM into the VM instance or instances.

##### `frequency=600`
The starting `frequency` of the VM instance or instances. Will automatically be set to the closest multiple of 60 less than or equal to the provided `frequency`.

##### `loadState=None`
A path or tag to a VM save state that will be loaded into each VM instance or instances.

##### `inputHistory=None`
If provided user and AI input will be ignored and the history will be used to reproduce the same events.

##### `sampleRate=1`
The number of steps that are performed when an AI calls `act`.

##### `instances=1`
The number of VM instances to create.

##### `display=False`
If True, the VM will create a Chip-Gr8 display. Cannot be True if instances does not equal 1.

##### `smooth=False`
If True, enables the experimental smooth rendering mode. This mode is slow on most machines.

##### `startPaused=False`
If True, the VM instance will start paused.

##### `aiInputMask=0xFFFF`
The keys usable to the AI agent as a bitmask. The keys available to the user are the bitwise inverse of this mask.

##### `foreground=(255, 255, 255)`
The foreground color of the Chip-Gr8 display as an RGB tuple or hex code.

##### `background=(0, 0, 0)`
The background color of the Chip-Gr8 display as an RGB tuple or hex code.

##### `theme=None`
The foreground/background color provided as a tuple.

##### `autoScroll=True`
If True, this disassembly source will automatically scroll when the Chip-Gr8 display is open and a ROM is running.

##### `speed`
The speed at which the UI is tied to the CHIP-8 frequency. When speed is 1, games will appear to run at the provided frequency, but when speed is 2, games will appear to run twice as fast. Must be provided as an integer.

### `readableInputHistory(inputHistory, names)`
Given an `inputHistory` and a set of actions, `names`, as a `NamedList`, produces a human readable version of the `inputHistory`.

## Chip8VM (Class)
Represents a CHIP-8 virtual machine. Provides interface and controls for display and input. Rather than initializing directly, an instance of this class or its sister class `Chip8VMs` should always be instantiated using `init`.

#### `.aiInputMask`
A number that controls what keys are usable by AI agents calling `act` and what keys are usable by a user on their keyboard. For example, an `aiInputMask` of 0x0000 will prevent an AI agent from using any keys, but a user will be able to use all keys.

#### `.inputHistory`
A list of number pairs that represent changes in key presses. The first value in the pair is the key value, the second is the clock value when input changed to that value.

#### `.paused`
A control flag set to True if the display is paused.

#### `.pyclock`
The pygame clock used to keep track of time between steps when using the Chip-Gr8 display.

#### `.record`
A control flag set to True if `inputHistory` is being recorded.

#### `.ROM`
The path to the currently loaded game ROM.

#### `.sampleRate`
The number of steps that are performed when an AI calls `act`.

#### `.smooth`
A control flag for the experimental smooth rendering mode. This mode is slow on most machines.

#### `.VM`
A direct reference to the CHIP-8 C-struct. This provides direct memory access (eg. `VM.RAM[0x200]`) as well as register reference (eg. `VM.PC`). Use these fields with caution as inappropriate usage can result in a segmentation fault. Direct references to `VM` should not be maintained (no aliasing).

#### `.addBreakpoint(addr)`
Add a breakpoint at `addr`. When the VM steps to this address (when PC is equal to `addr`) the Chip-Gr8 display will automatically pause.

#### `.removeBreakpoint(addr)`
Remove a breakpoint at `addr`.

#### `.toggleBreakpoint(addr)`
Toggles a breakpoint at `addr`.

#### `.clearBreakpoints()`
Clear all current breakpoints.

#### `.act(action)`
Allows an AI agent to perform `action` (action is an input key value) and steps the CHIP-8 emulator forward `sampleRate` clock cycles.

#### `.ctx()`
Returns an instance of the CHIP-8’s VRAM in a NumPy compliant format (Lazyarray). Pixel values can be addressed directly. (eg. a pixel at position (16, 8) can be retrieved with `ctx()[16, 8]`). This method is safe to call repeatedly.

#### `.done()`
Returns True if the VM is done and has NOT been reset.

#### `.doneIf(done)`
Signals to the VM that it is done.

#### `.go()`
Starts the VM in an until `done()` loop, calling `act(0)` repeatedly. This is ideal for user interaction without an AI agent.

#### `.input(keys)`
Send an input key value to the CHIP-8 emulator. Input keys are masked by `aiInputMask`.

#### `.loadROM(nameOrPath, reset=True)`
Loads a ROM from the provided path or searches for the name in the set of provided ROM files. If `reset` is True then VM will be reset prior to loading the ROM.

#### `.loadState(path=None, tag=None)`
Load a CHIP-8 emulator state from a `path` or by associated `tag`, restoring a previous state of `VM`.

#### `.saveState(path=None, tag=None)`
Save the current CHIP-8 emulator state to a `path` or `tag`.

#### `.reset()`
Reset the VM with the current ROM still loaded.

#### `.step()`
Step the VM forward 1 clock cycle.

## Chip8VMs (Class)
Represents a collection of CHIP-8 virtual machines. Provides an interface for dealing with and filtering several virtual machines at the same time. This class is iterable, and will iterate over all vms that are NOT `done()`.

#### `.done()`
Returns True if all VM instances are done.

#### `.find(predicate)`
Find a specific VM using a function `predicate` that takes a VM as an argument and returns True or False. Returns the first VM for which the `predicate` was True. Searches done and not done VMs.

#### `.inParallel(do)`
Performs a function `do` on all not done VMs in parallel. The function is expected to take the VM as an argument. When using this method external vm references can become out of date due to pickling across processes.

#### `.maxBy(projection)`
Returns the VM with the maximum value by the given `projection`, a function that takes a VM as its argument and returns a comparable value.

#### `.minBy(projection)`
Returns the VM with the minimum value by the given `projection`, a function that takes a VM as its argument and returns a comparable value.

#### `.reset()`
Resets all the VMs.

## Game (Class)
A generic class for game specific data. Game specific instances of this class exist for each included ROM (Cave, Pong, Worm, etc.).

#### `.actions`
A list of valid actions (key values) for the given game.

#### `.ROM`
The name of the ROM file for this game.

#### `.observe(vm)`
Returns a set of game specific observations given a VM.

## NamedList (Class)
A list-like structure that allows elements to be accessed by named properties. Behaves like a Python list, can be iterated, indexed, spliced, and measured with `len()`.

#### `.names`
A list of keys for the list in order.

#### `.values`
A list of values for the list in order.

#### `.append(name, value)`
Append a `name` and `value` to the list.

#### `.nparray()`
Retrieve the values of the list as a NumPy ndarray.

#### `.tensor()`
Retrieve the values of the list as a TensorFlow tensor.

## Observer (Class)
Represents a collection of queries that can be applied to a VM acquiring a set of observations.

#### `.addQuery(name, query)`
Add a query with an associated name to an observer. Accepts either a finalized query or a function that accepts a set of observations `(NamedList)` as the first argument and a vm instance as its second argument. This function argument can be used to create compound queries.

#### `.observe(vm)`
Retrieve a set of observations as a `NamedList` given a `vm` instance.

## Query (Class)
Used to find a specific memory address. When using a query to search for a memory address, several predicates can be used to filter the query.

#### `.done`
True if the query has found 0 or 1 addresses.

#### `.success`
True if the query has found 1 address.

#### `.dec()`
Filter queried memory addresses by values that have decreased since the last query.

#### `.eq(value)`
Filter queried memory addresses by values that equal `value`.

#### `.gt(value)`
Filter queried memory addresses by values that are greater than `value`.

#### `.gte(value)`
Filter queried memory addresses by values that are greater than or equal to `value`.

#### `.inc()`
Filter queried memory addresses by values that have increased since the last query.

#### `.lt(value)`
Filter queried memory addresses by values that are less than `value`.

#### `.lte(value)`
Filter queried memory addresses by values that are less than or equal to `value`.

#### `.observe(vm)`
If a query is finished this method returns the value at the VM instance's RAM corresponding to this query, otherwise it raises an Excception.

#### `.unknown()`
Refresh the previous values of all currently queried memory addresses.