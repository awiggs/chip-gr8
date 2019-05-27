import sys, pygame, time
from pygame.locals import *


class ChipGr8Window():
    screen = None
    scale = 10

    def __init__(self):
        pygame.init()
        
        size = width, height = 64*self.scale , 32*self.scale
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0,0,0))

    def renderScreen(self, bitMap):
        self.screen.fill((0,0,0))
        for row in range(len(bitMap)):
            for pixel in range(len(bitMap[row])):
                if bitMap[row][pixel] == 1:
                    pygame.draw.rect(self.screen, (255,255,255), (pixel*self.scale,row*self.scale,self.scale,self.scale))
        pygame.display.flip()

    