class Query(object):

    done = False
    '''Indicates that the query has founnd either 1 or 0 valid addresses'''
    
    success = None
    '''True if query is done and 1 address was found'''

    addr = None
    '''The address'''

    def __init__(self, vm=None, addr=None):
        '''
        Creates a new query object. Can eitheer be a finished query which 
        observes a provided addreess, or an unfinished query on a provided VM.

        @params vm          Chip8VM     the vm instance
                addr        int         the byte address
        '''
        assert vm or addr, 'Query must be created with a VM instance or an address!'

        self.done      = addr is not None
        self.success   = self.done or None
        self.addr      = addr

    def observe(self, vm):
        '''
        Asssumes the query is done and successful and therefore returns the byte
        at addr.

        @param vm   Chip8VM     the vm instance
        @returns    int         the bits
        '''
        return vm.VM.RAM[self.addr]

    def eq(self, value):
        '''
        Limit query to addresses where the current value is `value`.
        '''
        pass # TODO

    def lt(self, value):
        '''
        Limit query to addresses where the current value is less than `value`.
        '''
        pass # TODO

    def gt(self, value):
        '''
        Limit query to addresses where the current value is greater than 
        `value`.
        '''
        pass # TODO

    def lte(self, value):
        '''
        Limit query to addresses where the current value is less than or equal
        to `value`.
        '''
        pass # TODO

    def gte(self, value):
        '''
        Limit query to addresses where the current value is greater than or
        equal to `value`.
        '''
        pass # TODO

    def unknown(self):
        '''
        Indicate an unknown starting value for the query. Does not limit the
        query. If no query has started adds all addresses to the query.
        '''
        pass # TODO

    def inc(self):
        '''
        Limit query to addresses where the value has decreased since the last
        query.
        '''
        pass # TODO

    def dec(self):
        '''
        Limit query to addresses where the evalue has increased since the last
        query.
        '''
        pass # TODO

    def __str__(self):
        '''
        Converts this Query to python code that when evaluated, recreates
        this Query.
        '''
        pass # TODO