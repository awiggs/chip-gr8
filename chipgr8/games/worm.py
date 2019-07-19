from chipgr8.observer    import Observer
from chipgr8.query       import Query
from chipgr8.games.game  import Game
from chipgr8.namedArray  import NamedArray

worm = Game(
    ROM      = 'worm',
    observer = (Observer()
        .addQuery('score',  Query(addr=370))
        .addQuery('length', Query(addr=370))
        .addQuery('headX',  Query(addr=378))
        .addQuery('headY',  Query(addr=379))
        .addQuery('foodX',  Query(addr=380))
        .addQuery('foodY',  Query(addr=381))
        .addQuery('done',   lambda o, vm : vm.VM.PC == 0x36E)
    ),
    actions  = NamedArray(
        ['none', 'left', 'right', 'up', 'down'],
        [ 0x0,    0x10,   0x40,    0x4,  0x100],
    ),
)
