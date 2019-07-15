import os, sys
sys.path.append(os.path.expanduser('C:/Users/torrey/Desktop/UVic/Fifth Year/summer/seng499/chip-gr8'))

import chipgr8.vm as vm

# Visual assertion that the input history is correct
def testRecord():
    c = vm.Chip8VM(ROM='pong', inputHistory=None, display=True)
    assert c.record, "c.record was not True"
    c.go()
    print(c.inputHistory)

# Visual assertion that the playback is correct
def testPlayback():
    history = [(0, 0), (2, 1314), (0, 1394), (2, 1502), (0, 1541), (16, 1713), (0, 1843), (16, 1974), (0, 2114), (16, 2224), 
               (0, 2333), (2, 2502), (0, 2596), (2, 2862), (0, 2930), (16, 4701), (0, 4811), (2, 4918), (0, 5051)]
    
    c = vm.Chip8VM(ROM='pong', inputHistory=history, display=True)
    assert c.inputHistory == history, "c.inputHistory was not as expected"
    assert c.record is False, "c.record was not False"
    c.go()

# Visual assertion that the recorded play and the played-back play are the same
def testRecordAndPlayback():
    c = vm.Chip8VM(ROM='pong', inputHistory=None, display=True)
    assert c.record, "c.record was not True"
    history = c.inputHistory
    c.go()
    
    d = vm.Chip8VM(ROM='pong', inputHistory=history, display=True)
    assert d.inputHistory == history, "d.inputHistory was not as expected"
    assert d.record is False, "d.record was not False"
    d.go()

# Run tests
testRecord()
testPlayback()
testRecordAndPlayback()
