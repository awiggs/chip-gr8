from chipgr8 import Query, Observer, NamedList

class Game(object):
    '''
    A generic class for game specific data. Game specific instances of this 
    class exist for each included ROM (cave, pong, worm).
    '''

    actions = None
    '''
    A list of valid actions (key values) for the given game.
    '''

    ROM = None
    '''
    The name of the ROM file for this game.
    '''

    def __init__(self, ROM, observer, actions):
        '''
        Creates a new standard game object.

        @params ROM         str         the game ROM path
                observer    Observer    the game observer
                actions     ndarray     valid game actions
        '''
        self.ROM        = ROM
        self.actions    = actions
        self.__observer = observer

    def observe(self, vm):
        '''
        Returns a set of game specific observations given a vm.
        '''
        return self.__observer.observe(vm)

cave = Game(
    ROM         = 'Cave',
    observer    = Observer()
        .addQuery("myX", Query(addr=379))
        .addQuery("myY", Query(addr=380)),
    actions     = NamedList(
        ['up', 'right', 'down', 'left', 'start'],
        [0x4,   0x40,    0x100,  0x80,   0x8000]
    )
)
    
pong = Game(
    ROM      = 'pong',
    observer = Observer()
        .addQuery('opponent', Query(addr=756))
        .addQuery('score', Query(addr=755))
        .addQuery('done', lambda o, vm: vm.VM.RAM[755] == 3 or vm.VM.RAM[756] == 3),
    actions  = NamedList(
        ['none', 'up', 'down'],
        [0x0,    0x10,  0x2],
    ),
)

squash = Game(
    ROM      = 'squash',
    Observer = Observer()
        .addQuery('lives',   Query(addr=370))
        .addQuery('ballX',   Query(addr=375))
        .addQuery('ballY',   Query(addr=376))
        .addQuery('paddleY', Query(addr=372)),
    actions  = NamedList(
        ['none', 'up', 'down'],
        [ 0x0,    0x2,  0x10 ],
    ),
)

worm = Game(
    ROM      = 'worm',
    observer = Observer()
        .addQuery('score',  Query(addr=370))
        .addQuery('length', Query(addr=370))
        .addQuery('headX',  Query(addr=378))
        .addQuery('headY',  Query(addr=379))
        .addQuery('foodX',  Query(addr=380))
        .addQuery('foodY',  Query(addr=381))
        .addQuery('done',   lambda o, vm : vm.VM.PC == 0x36E),
    actions  = NamedList(
        ['none', 'left', 'right', 'up', 'down'],
        [ 0x0,    0x10,   0x40,    0x4,  0x100],
    ),
)