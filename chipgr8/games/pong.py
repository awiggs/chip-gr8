from chipgr8.observer    import Observer
from chipgr8.query       import Query
from chipgr8.games.game  import Game
from chipgr8.namedArray  import NamedArray

pong = Game(
    ROM      = 'pong',
    observer = Observer()
        .addQuery('opponent', Query(addr=756))
        .addQuery('score', Query(addr=755))
        .addQuery('done', lambda vm: vm.VM.RAM[755] == 3 or vm.VM.RAM[756] == 3),
    actions  = NamedArray(
        ['up', 'down'],
        [0x10,  0x2],
    ),
)
