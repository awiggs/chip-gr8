from chipgr8.query      import Query
from chipgr8.observer   import Observer
from chipgr8.games.game import Game
from chipgr8.namedArray import NamedArray

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

cave = Game(
    ROM         = 'Cave',
    observer    = Observer()
        .addQuery("myX", Query(addr=379))
        .addQuery("myY", Query(addr=380)),
    actions     = NamedArray(
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
    actions  = NamedArray(
        ['none', 'up', 'down'],
        [0x0,    0x10,  0x2],
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
    actions  = NamedArray(
        ['none', 'left', 'right', 'up', 'down'],
        [ 0x0,    0x10,   0x40,    0x4,  0x100],
    ),
)