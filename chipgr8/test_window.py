from chipgr8.window import Window
import sys, pygame, time
from pygame.locals import *

def demo1():
    w = Window()
    w.render(getTestBitMap())
    input("press enter to quit")

def demo2():
    w = Window()
    w.render(getTestBitMap2())
    input("press enter to quit")

def demo3():
    w = Window()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        w.render(getTestBitMap())
        time.sleep(0.5)
        w.render(getTestBitMap2(), True)
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