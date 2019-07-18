class Chip8VMs(object):
    '''
    Represents a collection of Chip8VMs.
    '''

    __instances = []
    '''A list of Chip8VM instances'''

    __notDoneInstances = []
    '''A list of all Chip8VM instances that are not done'''

    __doneInstances = []
    '''A list of all Chip8VM instances taht are done'''

    def get(self):
        return self.__instances

    def __init__(self, instances):
        '''
        @param instances List[Chip8VM]  a list of Chip8VM instances 
        '''
        self.__instances        = instances[:]
        self.__notDoneInstances = instances[:]
        self.__doneInstances    = []
        for vm in instances:
            vm.linkVMs(self) # Need to link so that VMs can signal us

    def done(self):
        '''
        Returns true if all VMs are done. 
        '''
        return len(self.__notDoneInstances) == 0

    def reset(self):
        '''
        Resets all VMs.
        '''
        for vm in self.__instances:
            vm.reset()
        self.__notDoneInstances = self.__instances[:]
        self.__doneInstances    = []

    def signalDone(self, vm):
        '''
        Allows a VM to signal to its collection that it is done.

        @param vm   Chip8VM     the done VM
        '''
        self.__notDoneInstances.remove(vm)
        self.__doneInstances.append(vm)

    def find(self, predicate):
        '''
        Find a particular vm based off a predicate. Returns None if no VM matches.

        @param predicate    Callable[[Chip8VM], bool]   
               return true for the desired VM
        '''
        for vm in self.__instances:
            if predicate(vm):
                return vm

    def maxBy(self, projection):
        '''
        Returns the max of all VM instances by the criteria of `projection`.

        @param projection   Callable[[Chip8VM], Comparable]    
              projects a Chip8VM to a Comparable value, eg. a number
        '''
        return max(self.__instances, key=projection)

    def minBy(self, projection):
        '''
        Returns the min of all VM instances by the criteria of `projection`.

        @param projection   Callable[[Chip8VM], Comparable]    
              projects a Chip8VM to a Comparable value, eg. a number
        '''
        return min(self.__instances, key=projection)

    def inParallel(self, do):
        '''
        Runs do in parallel across all not done VM instances.

        @param do   Callable[[Chip8VM]]     action to perform
        '''
        pass # TODO

    def __iter__(self):
        '''
        Returns an iterable of all not done VM instances.
        '''
        return iter(self.__notDoneInstances)
