from chipgr8.namedArray import NamedArray

class Observer(object):

    queries = []
    '''A list of all queries associated with this observer'''

    def addQuery(self, name, query):
        '''
        Adds a query to this observer. A query can either be an instance of
        a query object, or a function. A query function takes a set of 
        observations (as a NamedArray) as its argument and returns a new
        value to add to that array.

        @params name    str     
                the name to associate to the query
                query   Query | Callable[[NamedArray], int]
                the query object or callable funcntion
        @returns        Obsesrver   itself
        '''
        return self

    def observe(self, vm):
        '''
        Given a vm instance, returns a set of observations as a NamedArray.

        @params vm   Chip8VM     the vm instance to observe
        @returns     NamedArray  the observations
        '''
        NamedArray(['names'], ['values'])
        pass # TODO

    def __str__(self):
        '''
        Converts this observer to python code that when evaluated, recreates
        this observer. This functionality will be essential for creating
        observers for games through GUI interactions.

        NOTE: Query objects __str__ method should behave similarly, so to
              produce the desired results str(Query) should be used to produce
              the individual query code.

        eg.
            "(Observer().addQuery("score", Query(addr=0x200)))"

        @returns    str     the source code representation
        '''
        pass # TODO