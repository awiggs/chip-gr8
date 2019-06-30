from chipgr8.observer    import Observer
from chipgr8.query       import Query
from chipgr8.games.game  import Game
from chipgr8.namedArray  import NamedArray

# TODO These values are not real!!!
pong = Game(
    ROM      = 'pong',
    observer = Observer()
        .addQuery('ballX', Query(addr=0x120))
        .addQuery('score', Query(addr=0x200)),
    actions  = NamedArray(
        ['up', 'down'],
        [0x0,  0x1],
    ),
)