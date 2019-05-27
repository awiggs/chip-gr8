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

# Build Using mekpie

To build the c code you will need to have mekpie installed

```
pip install mekpie
```

To build the dll prior to running the python script:

```
mekpie -m dll build
```

To run the c tests run

```
mekpie test
```

# Build Using Make

```
make
```