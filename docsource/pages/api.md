# Introduction
[Click here]() to download the Chip-Gr8 User Manual, which contains more in-depth descriptions of the Chip-Gr8 project.

This section details the API of Chip-Gr8. It is broken down into the primary classes, including all fields and methods, as well as other important functions.


# Chip8VM (Class)
Represents a CHIP-8 virtual machine. Provides interface and controls for display and input. Rather than initializing directly, an instance of this class or its sister class **Chip8VMs** should always be instantiated using **init**.

## Fields

## `.aiInputMask`
A number that controls what keys are usable by AI agents calling **act** and what keys are usable by a user on their keyboard. For example, an **aiInputMask** of 0x0000 will prevent an AI agent from using any keys, but a user will be able to use all keys.

## `.inputHistory`
A list of number pairs that represent changes in key presses. The first value in the pair is the key value, the second is the clock value when input changed to that value.

## `.paused`
A control flag set to True if the display is paused.

## `.pyclock`
The pygame clock used to keep track of time between steps when using the CHIP-GR8 display.

## `.record`
A control flag set to True if **inputHistory** is being recorded.

## `.ROM`
The path to the currently loaded game ROM.

## `.sampleRate`
The number of steps that are performed when an AI calls **act**.

## `.smooth`
A control flag for the experimental smooth rendering mode. This mode is slow on most machines.

## `.VM`
A direct reference to the CHIP-8 c-struct. This provides direct memory access (eg. **VM.RAM[0x200]**) as well as register reference (eg. **VM.PC**). Use these fields with caution as inappropriate usage can result in a segmentation fault. Direct references to **VM** should not be maintained (no aliasing).

## Methods

## `.act(action)`
Allows an AI agent to perform **action** (action is an input key value) and steps the CHIP-8 emulator forward **sampleRate** clock cycles.

## `.ctx()`
Returns an instance of the CHIP-8’s VRAM in a numpy compliant format (lazyarray). Pixel values can be addressed directly. (eg. a pixel at position (16, 8) can be retrieved with **ctx()[16, 8]**). This method is safe to call repeatedly.

## `.done()`
Returns True if the VM is done and has NOT been reset.

## `.doneIf(done)`
Signals to the VM that it is done.

## `.go()`
Starts the VM in an until **done()** loop, calling **act(0)** repeatedly. This is ideal for user interaction without an AI agent.

## `.input(keys)`
Send an input key value to the CHIP-8 emulator. Input keys are masked by **aiInputMask**.

## `.loadROM(nameOrPath, reset=True)`
Loads a ROM from the provided path or searches for the name in the set of provided ROM files. If **reset** is True then VM will be reset prior to loading the ROM.

## `.loadState(path=None, tag=None)`
Load a CHIP-8 emulator state from a **path** or by associated **tag**, restoring a previous state of **VM**.

## `.saveState(path=None, tag=None)`
Save the current CHIP-8 emulator state to a **path** or **tag**.

## `.reset()`
Reset the VM with the current ROM still loaded.

## `.step()`
Step the VM forward 1 clock cycle.

# Chip8VMs (Class)
Represents a collection of CHIP-8 virtual machines. Provides an interface for interfacing with and filtering several virtual machines at the same time. This class is iterable, and will iterate over all vms that are NOT **done()**.

## Methods

## `.done()`
Returns True if all vm instances are done.

## `.find(predicate)`
Find a specific vm using a function **predicate** that takes a vm as an argument and returns True or False. Returns the first vm for which the **predicate** was True. Searches done and not done vms.

## `.inParallel(do)`
Performs a function **do** on all not done vms in parallel. The function is expected to take the vm as an argument. When using this method external vm references can become out of date due to pickling across processes. 

## `.maxBy(projection)`
Returns the vm with the maximum value by the given **projection**, a function that takes a vm as its argument and returns a comparable value.

## `.minBy(projection)`
Returns the vm with the minimum value by the given **projection**, a function that takes a vm as its argument and returns a comparable value.

## `.reset()`
Resets all the vms

# disassemble((Parameters))
Converts a binary ROM into an assembly source file. Returns the source. Provides option for disassembling with labels and special format.

## Parameters

## `buffer=None`
The binary ROM to disassemble as a set of bytes. Optional if **inPath** is provided.

## `inPath=None`
The path to a binary ROM to disassemble. Optional if **buffer** is provided.

## `outPath=None`
If the path is provided, the source code is written to that file.

## `labels={}`
A dictionary used to generate labels. If None is passed, labels will not be generated in the source.

## `decargs=True`
If True, instruction numerical operands will be output in decimal rather than hexadecimal.

## `prefix=' '`
The string used to prefix all instructions.

## `hexdump=False`
If True, all instructions will be postfixed with a comment displaying the hexadecimal value of the instruction.

## `labelSep = '\n '`
The string used to separate labels from instructions.

# findROM(rom)
Returns the path to **rom** if it is one of the included ROMs.

# Game (Class)
A generic class for game specific data. Game specific instances of this class exist for each included ROM (cave, pong, work).

## Fields

## `.actions`
A list of valid actions (key values) for the given game.

## `.ROM`
The name of the ROM file for this game.

## Methods

## `.observe(vm)`
Returns a set of game specific observations given a vm.

# hexdump(buffer=None, inPath=None, outPath=None)
Dumps a **buffer** or file at **inPath** as a set of 16bit hexadecimal values on each line (the number of bits that correspond to a CHIP-8 instruction). Writes the data to **outPath** if provided.

# init((Parameters))

## Parameters

## `ROM=None`
If provided will load a ROM into the vm instance or instances.

## `frequency=600`
The starting **frequency** of the vm instance or instances. Will automatically be set to the closest multiple of 60 less than or equal to the provided **frequency**.

## `loadState=None`
A path or tag to a vm save state that will be loaded into each vm instance or instances.

## `inputHistory=None`
If provided user and AI input will be ignored and the history will be used to reproduce the same events.

## `sampleRate=1`
The number of steps that are performed when an AI calls **act**.

## `instances=1`
The number of vm instances to create.

## `display=False`
If True, the vm will create a Chip-Gr8 display. Cannot be True if instances does not equal 1.

## `smooth=False`
If True, enables the experimental smooth rendering mode. This mode is slow on most machines.

## `startPaused=False`
If True, the vm instance will start paused.

## `aiInputMask=0xFFFF`
The key usable to the AI agent as a bitmask. The keys available to the user are the bitwise inverse of this mask.

## `foreground=(255, 255, 255)`
The foreground color of the Chip-Gr8 display as an RGB tuple or hex code.

## `background=(0, 0, 0)`
The background color of the Chip-Gr8 display as an RGB tuple or hex code.

## `theme=None`
The foreground/background color provided as a tuple.

## `autoScroll=True`
If True, this disassembly source will automatically scroll when the Chip-Gr8 display is open and a ROM is running.

# NamedList (Class)
A list-like structure that allows elements to be accessed by named properties. Behaves like a Python list, can be iterated, indexed, spliced, and measured with **len()**.

## Fields

## `.names`
A list of keys for the list in order.

## `.values`
A list of values for the list in order.

## Methods

## `.append(name, value)`
Append a **name** and **value** to the list.

## `.nparray()`
Retrieve the valyes of the list as a numpy ndarray.

## `.tensor()`
Retrieve the values of the list as a tensorflow tensor.

# Observer (Class)
Represents a collection of queries that can be applied to a vm acquiring a set of observations.

## Methods

## `.addQuery(name, query)`
Add a query with an associated name to an observer. Accepts either a finalized query or a function that accepts a set of observations **(NamedList)** as the first argument and a vam instance as its second argument. This function argument can be used to create compound queries.

## `.observe(vm)`
Retrieve a set of observations as a **NamedList** given a **vm** instance.

# Query (Class)
Used to find a specific memory address. When using a query to search for a memory address, several predicates can be used to filter the query.

## Fields

## `.done`
True if the query has found 0 or 1 addresses.

## `.success`
True if the query has found 1 address.

## Methods

## `.dec()`
Filter queried memory addresses by values that have decreased since the last query.

## `.eq(value)`
Filter queried memory addresses by values that equal **value**.

## `.gt(value)`
Filter queried memory addresses by values that are greater than **value**.

## `.gte(value)`
Filter queried memory addresses by values that are greater than or equal to **value**.

## `.inc()`
Filter queried memory addresses by values that have increased since the last query.

## `.lt(value)`
Filter queried memory addresses by values that are less than **value**.

## `.lte(value)`
Filter queried memory addresses by values that are less than or equal to **value**.

## `.observe(vm)`
If a query is successful this method returns the value at the vm instance's RAM corresponding to this query.

## `.unknown()`
Refresh the previous values of all currently queried memory addresses.

# readableInputHistory(inputHistory, names)
Given an **inputHistory** and a set of actions, **names**, as a **NamedList**, produces a human readable version of the **inputHistory**.
