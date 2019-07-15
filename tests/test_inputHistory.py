import os, sys
sys.path.append(os.path.expanduser('C:/Users/torrey/Desktop/UVic/Fifth Year/summer/seng499/chip-gr8'))

import chipgr8.vm as vm

# Visual assertion that the input history is correct
def testHumanRecord():
    c = vm.Chip8VM(ROM='pong', inputHistory=None, display=True)
    assert c.record, "c.record was expected to be True"
    c.go()
    print(c.inputHistory)

# Visual assertion that the playback is correct
def testPlayback():
    history = [(0, 0), (2, 1314), (0, 1394), (2, 1502), (0, 1541), (16, 1713), (0, 1843), (16, 1974), (0, 2114), (16, 2224), 
               (0, 2333), (2, 2502), (0, 2596), (2, 2862), (0, 2930), (16, 4701), (0, 4811), (2, 4918), (0, 5051)]
    
    c = vm.Chip8VM(ROM='pong', inputHistory=history, display=True)
    assert c.inputHistory == history, "c.inputHistory was not as expected"
    assert c.record is False, "c.record was expected to be False"
    c.go()

# Visual assertion that the recorded play and the played-back play are the same
def testHumanRecordAndPlayback():
    # record
    c = vm.Chip8VM(ROM='pong', inputHistory=None, display=True)
    assert c.record, "c.record was expected to be True"
    history = c.inputHistory
    c.go()
    
    # playback
    d = vm.Chip8VM(ROM='pong', inputHistory=history, display=True)
    assert d.inputHistory == history, "d.inputHistory was not as expected"
    assert d.record is False, "d.record was expected to be False"
    d.go()

# Visual assertion that the AI input is saved and that the playback is correct
def testAIRecordAndPlayback():
    c = vm.Chip8VM(ROM='pong', inputHistory=None, display=False)
    assert c.record, "c.record was expected to be True"
    for _ in range(1000):
        c.act(0)
    for _ in range(1000):
        c.act(1 << 1)
    for _ in range(2000):
        c.act(0)
    for _ in range(1000):
        c.act(1 << 4)
    for _ in range(1000):
        c.act(0)
    print(c.inputHistory)

    # playback
    d = vm.Chip8VM(ROM='pong', inputHistory=c.inputHistory, display=True)
    assert d.record is False, "d.record was expected to be False"
    d.go()

# Test that a human user can input keypresses at the same time as an AI and that the playback
# displays both of them correctly
def testMixedHumanAndAIInput():
    def aiFunc(vm):
        if vm.VM.clock < 1000:
            vm.input(0)
        if vm.VM.clock >= 1000 and vm.VM.clock < 3000:
            vm.input(1 << 4)
        if vm.VM.clock >= 2000:
            vm.input(0)

    # record
    c = vm.Chip8VM(ROM='pong', inputHistory=None, display=True, aiInputMask=16)
    assert c.record, "c.record was expected to be True"
    c.go(aiFunc)
    print(c.inputHistory)

    # playback
    d = vm.Chip8VM(ROM='pong', inputHistory=c.inputHistory, display=True)
    assert d.record is False, "d.record was expected to be False"
    d.go()

# Visual assertion that 
def testSingleInputHistory():
    history = [(0, 0)]

    c = vm.Chip8VM(ROM='pong', inputHistory=history, display=True)
    assert c.record is False, "c.record was expected to be False"
    print(c.inputHistory)
    c.go()


# Run tests
# testRecord()
# testPlayback()
# testRecordAndPlayback()
# testAIRecordAndPlayback()
# testMixedHumanAndAIInput()
testSingleInputHistory()
