from multiprocessing import Pool, cpu_count

class Chip8VMs(object):
    '''
    Represents a collection of Chip8VMs.
    '''

    __instances = set()
    '''A list of Chip8VM instances'''

    __notDoneInstances = set()
    '''A list of all Chip8VM instances that are not done'''

    __doneInstances = set()
    '''A list of all Chip8VM instances taht are done'''

    def items(self):
        '''
        Returns the collection of instance of Virtual Machines
        '''
        return self.__instances

    def __init__(self, instances):
        '''
        @param instances List[Chip8VM]  a list of Chip8VM instances 
        '''
        self.__instances        = set(instances)
        self.__notDoneInstances = set(instances)
        self.__doneInstances    = set()
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
        self.__notDoneInstances = set(self.__instances)
        self.__doneInstances    = set()

    def signalDone(self, vm):
        '''
        Allows a VM to signal to its collection that it is done.

        @param vm   Chip8VM     the done VM
        '''
        print('here')
        self.__notDoneInstances.remove(vm)
        self.__doneInstances.add(vm)

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
        for vm in self.__notDoneInstances:
            vm.clearCtx()
        with Pool(cpu_count()) as pool:
            stepped = set(pool.map(PoolHandler(do), self.__notDoneInstances))
        self.__instances        = stepped.union(self.__doneInstances)
        self.__notDoneInstances = set(vm for vm in stepped if not vm.done)
        self.__doneInstances    = set(vm for vm in stepped if vm.done)

    def __iter__(self):
        '''
        Returns an iterable of all not done VM instances.
        '''
        return iter(self.__notDoneInstances)

class PoolHandler(object):

    def __init__(self, do):
        self.do = do

    def __call__(self, vm):
        self.do(vm)
        vm.clearCtx()
        return vm
