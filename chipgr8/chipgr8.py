import chipgr8.core as core

def init(
    loadState    = None,
    ROM          = None,
    display      = None,
    timing       = None,
    memoryTables = None,
    instances    = None,
    # Additional options
):
    '''
    Initializes the chipgr8 library and returns a new instance of Chip8VM from
    `chipgr8/vm.py`, providing that object the appropriate options. Multiple 
    instances may also be provided.

    @params loadState    A path to a save state to load
            ROM          A ROM to load
            display      If true a window will display the VM display
            timing       The timing convention used when step is called
            memoryTables A method of specifying ROM specific fields
    @returns             The VM instance or instances
    '''
    core.helloSharedLibrary()
    pass #TODO