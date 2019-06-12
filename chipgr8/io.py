import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import sys
import time
import pygame

from pygame.locals import *
from pygame import event as evt
import os

import chipgr8.core

class ChipGr8Window():
    screen = None
    scale = 10

    def __init__(self):
        pygame.init()
        
        size = width, height = 64*self.scale , 32*self.scale
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0,0,0))
        pygame.mixer.music.load(os.path.realpath(os.path.join(__file__, "../../data/sound/pureTone.mp3")))

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

    def input(self):
        core.send_input(self.get_keymask())

    def get_keymask(self):
        keymask = bin(0)
        events = evt.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    keymask += 0b1
                if event.key == pygame.K_1:
                    keymask += 0b10
                if event.key == pygame.K_2:
                    keymask += 0b100
                if event.key == pygame.K_3:
                    keymask += 0b1000
                if event.key == pygame.K_4:
                    keymask += 0b10000
                if event.key == pygame.K_5:
                    keymask += 0b100000
                if event.key == pygame.K_6:
                    keymask += 0b1000000
                if event.key == pygame.K_7:
                    keymask += 0b10000000
                if event.key == pygame.K_8:
                    keymask += 0b100000000
                if event.key == pygame.K_9:
                    keymask += 0b1000000000
                if event.key == pygame.K_a:
                    keymask += 0b10000000000
                if event.key == pygame.K_b:
                    keymask += 0b100000000000
                if event.key == pygame.K_c:
                    keymask += 0b1000000000000
                if event.key == pygame.K_d:
                    keymask += 0b10000000000000
                if event.key == pygame.K_e:
                    keymask += 0b100000000000000
                if event.key == pygame.K_f:
                    keymask += 0b1000000000000000
            return keymask

