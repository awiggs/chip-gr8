# Run

To run the python module (make sure you use some version of python 3, preferably 3.6 or later):

```
python -m chipgr8
```

To load a ROM and run it (where ROM is either a path to a ROM or the start of a name)

```
python -m chipgr8 -r ROM
 # eg.
python -m chipgr8 -r pong 
```

To disassemble a ROM

```
python -m chipgr8 -d ROM -o OUTFILE
```

To assemble a ROM

```
python -m chipgr8 -a SRC -o OUTFILE
```

For more commandline options see

```
python -m chipgr8 -h
```

# Requirements

Before building and running, make sure you have pygame and pytest. You can install them globally or for your user

# Globally

```
python -m pip install pygame
python -m pip install pytest
```

# User

```
python -m pip install -U pygame --user
python -m pip install -U pytest --user
```

# Changing the VM Struct

To update the VM struct used in the C and python code modify `defineChip8VMStruct.py` and then run 

```
python ./defineChip8VMStruct.py
```

# Build Using mekpie

To build the c code you will need to have mekpie installed

```
pip install mekpie
```

To build the shared library prior to running the python script:

```
mekpie build
```

To run the c tests run

```
mekpie test
```

# Build Using Make

```
make
```