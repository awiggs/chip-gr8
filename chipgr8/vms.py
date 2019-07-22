from multiprocessing import Pool, cpu_count

class Chip8VMs(object):
    '''
    Represents a collection of CHIP-8 virtual machines. Provides an interface 
    for interacting with and filtering several virtual machines at the same 
    time. This class is iterable, and will iterate over all vms that are NOT 
    done().
    '''

    __instances = set()
    '''A list of Chip8VM instances'''

    __notDoneInstances = set()
    '''A list of all Chip8VM instances that are not done'''

    __doneInstances = set()
    '''A list of all Chip8VM instances that are done'''

    __toBeRemoved = set()

    def __init__(self, instances):
        '''
        @param instances List[Chip8VM]  a list of Chip8VM instances 
        '''
        self.__instances        = set(instances)
        self.__notDoneInstances = set(instances)
        self.__doneInstances    = set()
        for vm in instances:
            vm._linkVMs(self) # Need to link so that VMs can signal us

    def __iter__(self):
        '''
        Returns an iterable of all not done VM instances.
        '''
        return iter(self.__notDoneInstances)

    def _signalDone(self, vm):
        '''
        Allows a VM to signal to its collection that it is done.

        @param vm   Chip8VM     the done VM
        '''
        self.__toBeRemoved.add(vm)

    def done(self):
        '''
        Returns True if all vm instances are done.
        '''
        for vm in self.__toBeRemoved:
            self.__doneInstances.add(vm)
            self.__notDoneInstances.remove(vm)
        self.__toBeRemoved.clear()
        return len(self.__notDoneInstances) == 0

    def find(self, predicate):
        '''
        Find a specific vm using a function predicate that takes a vm as an 
        argument and returns True or False. Returns the first vm for which the 
        predicate was True. Searches done and not done vms.
        '''
        for vm in self.__instances:
            if predicate(vm):
                return vm
    
    def inParallel(self, do):
        '''
        Performs a function do on all not done vms in parallel. The function is 
        expected to take the vm as an argument. When using this method external 
        vm references can become out of date due to pickling across processes.
        '''
        for vm in self.__notDoneInstances:
            vm._clearCtx()
        with Pool(cpu_count()) as pool:
            run = set(pool.map(_PoolHandler(do), self.__notDoneInstances))
        self.__instances     = run.union(self.__doneInstances)
        self.__doneInstances = self.__instances.copy()
        self.__notDoneInstances.clear()

    def maxBy(self, projection):
        '''
        Returns the vm with the maximum value by the given projection, a 
        function that takes a vm as its argument and returns a comparable value.
        '''
        return max(self.__instances, key=projection)

    def minBy(self, projection):
        '''
        Returns the vm with the minimum value by the given projection, a 
        function that takes a vm as its argument and returns a comparable value.
        '''
        return min(self.__instances, key=projection)

    def reset(self):
        '''
        Resets all vms.
        '''
        for vm in self.__instances:
            vm.reset()
        self.__notDoneInstances = set(self.__instances)
        self.__doneInstances    = set()

class _PoolHandler(object):

    def __init__(self, do):
        self.do = do

    def __call__(self, vm):
        while not vm.done():
            self.do(vm)
        vm._clearCtx()
        return vm