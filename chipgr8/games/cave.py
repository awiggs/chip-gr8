from chipgr8.observer       import Observer
from chipgr8.query          import Query
from chipgr8.games.game     import Game
from chipgr8.namedArray     import NamedArray

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