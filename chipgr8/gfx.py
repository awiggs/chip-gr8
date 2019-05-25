import sys, pygame, time
from pygame.locals import *


class ChipGr8Window():
    screen = None
    scale = 5

    def __init__(self):
        pygame.init()
        
        size = width, height = 64*self.scale , 32*self.scale
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0,0,0))

    def render(self, bitMap):
        self.screen.fill((0,0,0))
        for row in range(len(bitMap)):
            for pixel in range(len(bitMap[row])):
                if bitMap[row][pixel] == 1:
                    pygame.draw.rect(self.screen, (255,255,255), (pixel*self.scale,row*self.scale,self.scale,self.scale))
        pygame.display.flip()



# TESTS
# =======================================================================================================================

def test1():
    w = ChipGr8Window()
    w.render(getTestBitMap())
    input("press enter to quit")

def test2():
    w = ChipGr8Window()
    w.render(getTestBitMap2())
    input("press enter to quit")

def test3():
    w = ChipGr8Window()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        w.render(getTestBitMap())
        time.sleep(0.5)
        w.render(getTestBitMap2())
        time.sleep(0.5)



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


test3()