import sys, pygame, time
from pygame.locals import *
import os


class ChipGr8Window():
    screen = None
    scale = 10

    def __init__(self):
        pygame.init()
        
        size = width, height = 64*self.scale , 32*self.scale
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0,0,0))
        pygame.mixer.music.load(os.path.join(__file__, "../../data/sound/pureTone.mp3"))

    # Takes a bitmap of the screen and renders the screen using pygame.
    # Takes an optional boolean parameter if you want to have sound playing for that frame
    def render(self, bitMap, soundBool=False):
        # Handle the pure tone
        if soundBool:
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.stop()

        # Handle the screen draw
        self.screen.fill((0,0,0))
        for row in range(len(bitMap)):
            for pixel in range(len(bitMap[row])):
                if bitMap[row][pixel] == 1:
                    pygame.draw.rect(self.screen, (255,255,255), (pixel*self.scale,row*self.scale,self.scale,self.scale))
        pygame.display.flip()

    
