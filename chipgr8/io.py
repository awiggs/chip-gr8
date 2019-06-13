import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import sys
import time
import pygame

from pygame.locals import *
from pygame import event
import os

import chipgr8.core as core

class ChipGr8Window():

    screen     = None
    scale      = 10
    background = (0,   0,   0)
    foreground = (255, 255, 255)
    tone       = os.path.realpath(os.path.join(__file__, "../../data/sound/pureTone.mp3"))

    def __init__(self, width, height):
        pygame.init()
        size        = width * self.scale, height * self.scale
        self.width  = width
        self.height = height
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(self.background)
        pygame.mixer.music.load(self.tone)

    def sound(self, play):
        if play:
            pygame.mixer.music.play()
        else: 
            pygame.mixer.music.stop()

    def clear(self):
        self.screen.fill(self.background)

    def render(self, ctx, x, y, rows):
        s = self.scale
        for xOff in range(8):
            for yOff in range(rows):
                rx = x + xOff
                ry = y + yOff
                pygame.draw.rect(
                    self.screen, 
                    self.foreground if ctx[rx, ry] else self.background, 
                    (rx * s, ry * s, s, s),
                )
        pygame.display.flip()

    def input(self):
        core.sendInput(self.get_keymask())

    def get_keymask(self):
        keymask = bin(0)
        events = event.get()
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

