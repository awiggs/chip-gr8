import os
import sys
import chipgr8

# Visual assertion that the input history is correct
def testHumanRecord():
    vm = chipgr8.init(ROM='pong', inputHistory=None, display=True)
    assert vm.record, "c.record was expected to be True"
    vm.go()
    print(vm.inputHistory)

# Visual assertion that the playback is correct
def testPlayback():
    history = [
        (0, 0), 
        (2, 1314), 
        (0, 1394), 
        (2, 1502), 
        (0, 1541), 
        (16, 1713), 
        (0, 1843), 
        (16, 1974), 
        (0, 2114), 
        (16, 2224), 
        (0, 2333),
        (2, 2502), 
        (0, 2596), 
        (2, 2862), 
        (0, 2930), 
        (16, 4701), 
        (0, 4811), 
        (2, 4918), 
        (0, 5051),
    ]
    vm = chipgr8.init(ROM='pong', inputHistory=history, display=True)
    assert vm.inputHistory == history, "c.inputHistory was not as expected"
    assert vm.record is False, "c.record was expected to be False"
    vm.go()

# Visual assertion that the recorded play and the played-back play are the same
def testHumanRecordAndPlayback():
    # record
    vm1 = chipgr8.init(ROM='pong', display=True, aiInputMask=0)
    assert vm1.record, "c.record was expected to be True"
    history = vm1.inputHistory
    vm1.go()
    # playback
    vm2 = chipgr8.init(ROM='pong', inputHistory=history, display=True)
    assert vm2.inputHistory == history, "d.inputHistory was not as expected"
    assert vm2.record is False, "d.record was expected to be False"
    vm2.go()

# Visual assertion that the AI input is saved and that the playback is correct
def testAIRecordAndPlayback():
    vm1 = chipgr8.init(ROM='pong')
    assert vm1.record, "c.record was expected to be True"
    for _ in range(1000):
        vm1.act(0)
    for _ in range(1000):
        vm1.act(1 << 1)
    for _ in range(2000):
        vm1.act(0)
    for _ in range(1000):
        vm1.act(1 << 4)
    for _ in range(1000):
        vm1.act(0)
    print(vm1.inputHistory)

    # playback
    vm2 = chipgr8.init(ROM='pong', inputHistory=vm1.inputHistory, display=True)
    assert vm2.record is False, "d.record was expected to be False"
    vm2.go()

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
    vm1 = chipgr8.init(ROM='pong', aiInputMask=16, display=True)
    assert vm1.record, "c.record was expected to be True"
    for _ in range(1000):
        vm1.act(0)
    for _ in range(1000):
        vm1.act(1 << 1)
    for _ in range(2000):
        vm1.act(0)
    for _ in range(1000):
        vm1.act(1 << 4)
    for _ in range(1000):
        vm1.act(0)
    print(vm1.inputHistory)

    # playback
    vm2 = chipgr8.init(ROM='pong', inputHistory=vm1.inputHistory, display=True)
    assert not vm2.record
    vm2.go()

# Visual assertion that 
def testSingleInputHistory():
    history = [(0, 0)]
    vm = chipgr8.init(ROM='pong', inputHistory=history, display=True)
    assert vm.record is False, "c.record was expected to be False"
    print(vm.inputHistory)
    vm.go()


# Run tests
# testHumanRecord()
# testPlayback()
# testHumanRecordAndPlayback()
# testAIRecordAndPlayback()
testMixedHumanAndAIInput()
# testSingleInputHistory()
