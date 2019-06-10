def getTestBitMap():
    bM = []
    for _ in range(32):
        bM.append(getTestLine())
    return bM

def getTestBitMap2():
    bM = []
    for x in range(32):
        bM.append(getTestLine2(x))
    return bM

def getTestLine2(x):
    line = []
    for p in range(64):
        if p == x:
            line.append(1)
        else:
            line.append(0)
    return line

def getTestLine():
    line = []
    for x in range(64):
        if x % 7 == 0:
            line.append(1)
        else:
            line.append(0)
    return line
