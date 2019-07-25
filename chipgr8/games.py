from chipgr8 import Query, Observer, NamedList
from numpy   import clip

K_NONE = 0x0000
K_0    = 0x0001
K_1    = 0x0002
K_2    = 0x0004
K_3    = 0x0008
K_4    = 0x0010
K_5    = 0x0020
K_6    = 0x0040
K_7    = 0x0080
K_8    = 0x0100
K_9    = 0x0200
K_A    = 0x0400
K_B    = 0x0800
K_C    = 0x1000
K_D    = 0x2000
K_E    = 0x4000
K_F    = 0x8000

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


Puzzle15 = Game(
    ROM      = '15 Puzzle',
    observer = Observer(),
    actions  = NamedList(
        [
            'none', 
            'shift0', 'shift1', 'shift2', 'shift3', 
            'shift4', 'shift5', 'shift6', 'shift7',
            'shift8', 'shift9', 'shiftA', 'shiftB',
            'shiftC', 'shiftD', 'shiftE', 'shiftF',
        ], [
            K_NONE,
            K_1, K_2, K_3, K_C,
            K_3, K_5, K_6, K_D,
            K_7, K_8, K_9, K_E,
            K_A, K_0, K_B, K_F,
        ],
    )
)

Airplane = Game(
    ROM      = 'Airplane',
    observer = Observer(),
    actions  = NamedList(
        ['none', 'drop'],
        [ K_NONE, K_8  ],
    )
)

AnimalRace = Game(
    ROM      = 'Animal Race',
    observer = Observer(),
    actions  = NamedList(
        [
            'none', 
            'betA',  'betB',  'betC', 'betD', 'betE',
            'bet1$', 'bet2$', 'bet3$', 
            'bet4$', 'bet5$', 'bet6$',
            'bet7$', 'bet8$', 'bet9$',
        ], [
            K_NONE, 
            K_A, K_B, K_C, K_D, K_E,
            K_1, K_2, K_3,
            K_4, K_5, K_6,
            K_7, K_8, K_9,
        ],
    )
)

AstroDodge = Game(
    ROM      = 'Astro Dodge',
    observer = Observer(),
    actions  = NamedList(
        ['none', 'start', 'left', 'right'],
        [ K_NONE, K_5,     K_4,    K_6   ],
    )
)

Blinky = Game(
    ROM      = 'Blinky',
    observer = Observer(),
    actions  = NamedList(
        ['none', 'left', 'right', 'up', 'done', 'blink'],
        [ K_NONE, K_7,    K_8,     K_3,  K_6,    K_F   ],
    )
)

Breakout = Game(
    ROM      = 'Breakout',
    observer = Observer()
        .addQuery("ballX", Query(addr=374))
        .addQuery("ballY", Query(addr=375))
        .addQuery("myX", Query(addr=380))
        .addQuery("score", Query(addr=373)),
    actions  = NamedList(
        ['none', 'left', 'right'],
        [ K_NONE, K_4,    K_6   ],
    )
)

Brix = Game(
    ROM      = 'Brix',
    observer = Observer(),
    actions  = NamedList(
        ['none', 'left', 'right'],
        [ K_NONE, K_4,    K_6   ],
    )
)

Cave = Game(
    ROM      = 'Cave',
    observer = Observer()
        .addQuery('x',          Query(addr=379))
        .addQuery('y',          Query(addr=380))
        .addQuery('upClear',    lambda o, vm : not vm.ctx()[clip(o.x, 0, 63), clip(o.y - 1, 0, 31)])
        .addQuery('downClear',  lambda o, vm : not vm.ctx()[clip(o.x, 0, 63), clip(o.y + 1, 0, 31)])
        .addQuery('leftClear',  lambda o, vm : not vm.ctx()[clip(o.x - 1, 0, 63), clip(o.y, 0, 31)])
        .addQuery('rightClear', lambda o, vm : not vm.ctx()[clip(o.x + 1, 0, 63), clip(o.y, 0, 31)])
        .addQuery('done',       lambda o, vm : vm.VM.PC == 0x570),
    actions  = NamedList(
        ['none', 'left', 'right', 'up', 'down', 'start'],
        [ K_NONE, K_4,    K_6,     K_2,  K_8,    K_F],
    )
)

Filter = Game(
    ROM      = 'Filter',
    observer = Observer(),
    actions  = NamedList(
        ['none', 'left', 'right'],
        [ K_NONE, K_4,    K_6   ],
    )
)

Hidden = Game(
    ROM      = 'Hidden',
    observer = Observer(),
    actions  = NamedList(
        ['none', 'start', 'left', 'right', 'up', 'down', 'select'],
        [ K_NONE, K_F,     K_4,    K_6,     K_2,  K_8,    K_5    ],
    )
)

LunarLander = Game(
    ROM      = 'Lunar Lander',
    observer = Observer(),
    actions  = NamedList(
        [
            'none', 
            'option1', 'option2', 'option3', 
            'thrust', 'left', 'right', 
        ], [
            K_NONE,
            K_1, K_2, K_3,
            K_2, K_4, K_6,
        ],
    )
)
    
Pong1Player = Game(
    ROM      = 'Pong (1 player)',
    observer = Observer()
        .addQuery('opponent',    Query(addr=756))
        .addQuery('p1Score',     Query(addr=755))
        .addQuery('p2Score',     Query(addr=756))
        .addQuery('score',       lambda o, vm: o.p1Score - o.p2Score)
        .addQuery('bestOf3Done', lambda o, vm: o.p1Score >= 3 or o.p2Score >= 3)
        .addQuery('bestOf5Done', lambda o, vm: o.p1Score >= 5 or o.p2Score >= 5)
        .addQuery('bestOf5Done', lambda o, vm: o.p1Score >= 7 or o.p2Score >= 7)
        .addQuery('bestOf5Done', lambda o, vm: o.p1Score >= 9 or o.p2Score >= 9)
        .addQuery('done',        lambda o, vm: o.p1Score >= 9 or o.p2Score >= 9),
    actions  = NamedList(
        ['none',   'up', 'down'],
        [ K_NONE,   K_1,  K_4  ],
    ),
)

Pong2Player = Game(
    ROM      = 'Pong (2 player)',
    observer = Observer()
        .addQuery('opponent', Query(addr=756))
        .addQuery('score',    Query(addr=755))
        .addQuery('done',     lambda o, vm: vm.VM.RAM[755] >= 3 or vm.VM.RAM[756] >= 3),
    actions  = NamedList(
        ['none',   'p1Up', 'p1Down', 'p2Up', 'p2Down'],
        [ K_NONE,   K_1,    K_4,      K_C,    K_D    ],
    ),
)

SpaceInvaders = Game(
    ROM      = 'Space Invaders',
    observer = Observer(),
    actions  = NamedList(
        ['none', 'start', 'shoot', 'left', 'right'],
        [ K_NONE, K_5,     K_5,     K_4,    K_6   ],
    )
)

Squash = Game(
    ROM      = 'Squash',
    observer = Observer()
        .addQuery('lives',   Query(addr=370))
        .addQuery('ballX',   Query(addr=375))
        .addQuery('ballY',   Query(addr=376))
        .addQuery('paddleY', Query(addr=372))
        .addQuery('score',   lambda o, vm: vm.VM.clock)
        .addQuery('done',    lambda o, vm: o.lives == 0 and vm.VM.clock > 12),
    actions  = NamedList(
        ['none', 'up', 'down'],
        [ K_NONE, K_1,  K_4  ],
    ),
)

Tetris = Game(
    ROM      = 'Tetris',
    observer = Observer(),
    actions  = NamedList(
        ['none', 'rotate', 'left', 'right', 'drop'],
        [ K_NONE, K_4,      K_5,    K_6,     K_8  ],
    )
)

Tron = Game(
    ROM      = 'Tron',
    observer = Observer(),
    actions  = NamedList(
        [],
        [],
    )
)

Worm = Game(
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
        [ K_NONE, K_4,    K_6,     K_2,  K_8  ],
    ),
)