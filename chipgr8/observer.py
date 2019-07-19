from chipgr8.namedArray import NamedArray
from chipgr8.query import Query

class Observer(object):

    queries = dict()
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
        if self.isObservable(query):
            self.queries[name] = query
        else:
            raise TypeError("Query is not a function or Query object")
        return self

    def isObservable(self, query):
        return callable(query) or isinstance(query, Query)

    def observe(self, vm):
        '''
        Given a vm instance, returns a set of observations as a NamedArray.

        @params vm   Chip8VM     the vm instance to observe
        @returns     NamedArray  the observations
        '''
        observations = NamedArray([], [])
        for name, query in self.queries.items():
            if isinstance(query, Query):
                observations.append(name, query.observe(vm))
        for name, query in self.queries.items():
            if callable(query):
                observations.append(name, query(observations, vm=vm))
        return observations


    def __str__(self):
        '''
        Converts this observer to python code that when evaluated, recreates
        this observer. This functionality will be essential for creating
        observers for games through GUI interactions.

        NOTE: Query objects __str__ method should behave similarly, so to
              produce the desired observationss str(Query) should be used to produce
              the individual query code.

        eg.
            "(Observer().addQuery("score", Query(addr=0x200)))"

        @returns    str     the source code representation
        '''
        return '(Observer(){})'.format(''.join('.addQuery(\'{}\', {})'.format(name, query)
            for (name, query)
            in self.queries.items()
        ))
