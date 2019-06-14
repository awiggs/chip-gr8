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

# Performance Problems on Mac

From [StackOverflow](https://stackoverflow.com/questions/31685936/pygame-application-runs-slower-on-mac-than-on-pc)

1. Run your pygame program
2. In the dock you will see a snake with controllers in his mouth. Right click him.
3. Go to Options and click "Show in Finder"
4. Finder will open and you will see a the python application.(Mine was in the shape of rocket with the idle symbol on it.)
5. Right click the python application and click "Get Info".
6. Check the box "Open in Low Resolution" and it should now run at around 60fps.