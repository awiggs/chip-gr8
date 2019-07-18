class Game(object):

    ROM = None
    '''The game ROM path'''

    observer = None
    '''The game observer'''

    actions = None
    '''Valid game actions'''

    def __init__(self, ROM, observer, actions):
        '''
        Creates a new standard game object.

        @params ROM         str         the game ROM path
                observer    Observer    the game observer
                actions     ndarray     valid game actions
        '''
        self.ROM      = ROM
        self.observer = lambda vm : observer.observe(vm)
        self.actions  = actions
