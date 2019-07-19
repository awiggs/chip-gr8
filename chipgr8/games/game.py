class Game(object):

    ROM = None
    '''The game ROM path'''

    actions = None
    '''Valid game actions'''
    
    observe = None
    '''The game observe function'''

    def __init__(self, ROM, observer, actions):
        '''
        Creates a new standard game object.

        @params ROM         str         the game ROM path
                observer    Observer    the game observer
                actions     ndarray     valid game actions
        '''
        self.ROM     = ROM
        self.actions = actions
        self.observe = lambda vm : observer.observe(vm)
    
