from chipgr8.namedList import NamedList
from chipgr8.query import Query


class Observer(object):
    '''
    Represents a collection of queries that can be applied to a vm acquiring a 
    set of observations.
    '''

    def __init__(self):
        self.queries = {}

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

    def addQuery(self, name, query):
        '''
        Add a query with an associated name to an observer. Accepts either a 
        finalized query or a function that accepts a set of observations 
        (NamedList) as the first argument and a vm instance as its second 
        argument. This function argument can be used to create compound queries.
        '''
        if callable(query) or isinstance(query, Query):
            self.queries[name] = query
        else:
            raise TypeError("Query is not a function or Query object")
        return self

    def observe(self, vm):
        '''
        Retrieve a set of observations as a NamedList given a vm instance.
        '''
        observations = NamedList([], [])
        for name, query in self.queries.items():
            if isinstance(query, Query):
                observations.append(name, query.observe(vm))
        for name, query in self.queries.items():
            if callable(query):
                observations.append(name, query(observations, vm=vm))
        return observations