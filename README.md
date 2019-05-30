# Run

To run the python module (make sure you use some version of python 3, preferably 3.6 or later):

```
python -m chipgr8
```

# Requirements

Before building and running, make sure you have pygame and pytest.

```
python -m pip install -U pygame --user
pip install pytest
```

# Changing Struct

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