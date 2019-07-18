class Query(object):

    done = False
    '''Indicates that the query has founnd either 1 or 0 valid addresses'''
    
    success = None
    '''True if query is done and 1 address was found'''

    previous = None
    '''Pevious iteration'''

    __addr = None
    '''The address'''

    __RAM = None
    '''VM struct reference'''

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
        self.__RAM    = None if vm is None else vm.VM.RAM
        self.__addr   = addr
        self.previous = [(addr, 0) for addr in range(0x1000)] if vm else None

    def checkIfDone(self):
        if self.done:
            return 'Query finished.'
        numFound = len(self.previous)
        if numFound > 1:
            return 'Query matched {} addresses.'.format(len(self.previous))
        self.done    = True
        self.success = numFound == 1
        self.__addr  = self.previous[0][0] if numFound == 1 else None
        return 'Query finished.'

    def observe(self, vm):
        '''
        Asssumes the query is done and successful and therefore returns the byte
        at addr.

        @param vm   Chip8VM     the vm instance
        @returns    int         the bits
        '''
        return vm.VM.RAM[self.__addr]

    def eq(self, value):
        '''
        Limit query to addresses where the current value is `value`.
        '''
        self.previous = [(addr, self.__RAM[addr])
            for (addr, _)
            in self.previous
            if self.__RAM[addr] == value
        ]
        return self.checkIfDone()

    def lt(self, value):
        '''
        Limit query to addresses where the current value is less than `value`.
        '''
        self.previous = [(addr, self.__RAM[addr])
            for (addr, _)
            in self.previous
            if self.__RAM[addr] < value
        ]
        return self.checkIfDone()

    def gt(self, value):
        '''
        Limit query to addresses where the current value is greater than 
        `value`.
        '''
        self.previous = [(addr, self.__RAM[addr])
            for (addr, _)
            in self.previous
            if self.__RAM[addr] > value
        ]
        return self.checkIfDone()

    def lte(self, value):
        '''
        Limit query to addresses where the current value is less than or equal
        to `value`.
        '''
        self.previous = [(addr, self.__RAM[addr])
            for (addr, _)
            in self.previous
            if self.__RAM[addr] <= value
        ]
        return self.checkIfDone()

    def gte(self, value):
        '''
        Limit query to addresses where the current value is greater than or
        equal to `value`.
        '''
        self.previous = [(addr, self.__RAM[addr])
            for (addr, _)
            in self.previous
            if self.__RAM[addr] >= value
        ]
        return self.checkIfDone()

    def unknown(self):
        '''
        Indicate an unknown starting value for the query. Does not limit the
        query. If no query has started adds all addresses to the query.
        '''
        self.previous = [(addr, self.__RAM[addr])
            for (addr, _)
            in self.previous
        ]
        return self.checkIfDone()

    def inc(self):
        '''
        Limit query to addresses where the value has decreased since the last
        query.
        '''
        self.previous = [(addr, self.__RAM[addr])
            for (addr, value)
            in self.previous
            if self.__RAM[addr] > value
        ]
        return self.checkIfDone()

    def dec(self):
        '''
        Limit query to addresses where the evalue has increased since the last
        query.
        '''
        self.previous = [(addr, self.__RAM[addr])
            for (addr, value)
            in self.previous
            if self.__RAM[addr] < value
        ]
        return self.checkIfDone()

    def __repr__(self):
        '''
        Converts this Query to python code that when evaluated, recreates
        this Query.
        '''
        if not self.success:
            return 'Query(addr=???, count={})'.format(len(self.previous))
        return 'Query(addr={})'.format(self.__addr)
