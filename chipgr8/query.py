class Query(object):
    '''
    Used to find a specific memory address. When using a query to search for a 
    memory address, several predicates can be used to filter the query. 
    '''

    __addr = None
    '''The address'''

    __vm = None
    '''VM struct reference'''

    done = False
    '''
    True if the query has found 0 or 1 addresses.
    '''
    
    success = None
    '''
    True if the query has found 1 address.
    '''

    previous = None
    '''
    Pevious iteration
    '''

    def __init__(self, vm=None, addr=None):
        '''
        Creates a new query object. Can eitheer be a finished query which 
        observes a provided addreess, or an unfinished query on a provided VM.

        @params vm          Chip8VM     the vm instance
                addr        int         the byte address
        '''
        assert vm or addr, 'Query must be created with a VM instance or an address!'

        self.done     = addr is not None
        self.success  = self.done or None
        self.__addr   = addr
        self.__vm     = vm
        self.previous = None if vm is None else [(addr, self.__vm.VM.RAM[addr]) 
            for addr 
            in range(0x1000)
        ]

    def __repr__(self):
        '''
        Converts this Query to python code that when evaluated, recreates
        this Query.
        '''
        if not self.success:
            return 'Query(addr=???, count={})'.format(len(self.previous))
        return 'Query(addr={})'.format(self.__addr)

    def __checkIfDone(self):
        if self.done:
            return 'Query finished.'
        numFound = len(self.previous)
        if numFound > 1:
            return 'Query matched {} addresses.'.format(len(self.previous))
        self.done    = True
        self.success = numFound == 1
        self.__addr  = self.previous[0][0] if numFound == 1 else None
        return 'Query finished.'

    def filter(self,pred):
        self.previous = [(addr, self.__vm.VM.RAM[addr])
            for (addr, value)
            in self.previous
            if pred(self.__vm.VM.RAM[addr], value)
        ]
        return self.__checkIfDone()

    def observe(self, vm):
        '''
        If a query is finished this method returns the value at the VM 
        instance's RAM corresponding to this query, otherwise it raises an 
        Excception.
        '''
        return vm.VM.RAM[self.__addr]

    def eq(self, value):
        '''
        Filter queiried memory addresses by values that equal value.
        '''
        return self.filter(lambda cur, prev : cur == value)

    def lt(self, value):
        '''
        Filter queiried memory addresses by values that are less than value.
        '''
        return self.filter(lambda cur, prev : cur < value)

    def gt(self, value):
        '''
        Filter queiried memory addresses by values that are greater than value.
        '''
        return self.filter(lambda cur, prev : cur > value)

    def lte(self, value):
        '''
        Filter queiried memory addresses by values that are less than or equal 
        to value.
        '''
        return self.filter(lambda cur, prev : cur <= value)

    def gte(self, value):
        '''
        Filter queiried memory addresses by values that are greater than or 
        equal to value.
        '''
        return self.filter(lambda cur, prev : cur >= value)

    def unknown(self):
        '''
        Refresh the previous values of all currently queried memory addresses.
        '''
        return self.filter(lambda cur, prev : True)

    def inc(self):
        '''
        Filter queiried memory addresses by values that have increased since 
        the last query.
        '''
        return self.filter(lambda cur, prev : cur > prev)

    def dec(self):
        '''
        Filter queiried memory addresses by values that have decreased since 
        the last query.
        '''
        return self.filter(lambda cur, prev : cur < prev)

    
