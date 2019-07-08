import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import sys
import time
import pygame
import numpy as np

from pygame.locals import *
from pygame import event

import chipgr8.core         as core
import chipgr8.shaders      as shaders
import chipgr8.disassemblerWindowModule as disWinModule

class ChipGr8Window():

    screen      = None
    scale       = 10
    gameSize    = (0, 0)
    screenSize  = (0, 0)
    background  = (0,   0,   0)
    foreground  = (255, 255, 255)
    tone        = os.path.realpath(os.path.join(__file__, "../../data/sound/pureTone.mp3"))

    def __init__(self, gameWidth, gameHeight):
        pygame.init()
        pygame.font.init()

        self.gameSize          = gameWidth * self.scale, gameHeight * self.scale
        self.disModule         = disWinModule.DisassemblerWindowModule(300, self.gameSize[1])
        self.screenSize        = (self.gameSize[0] + self.disModule.width, self.gameSize[1])
        self.gameWidth         = gameWidth
        self.gameHeight        = gameHeight

        # Create display screen and sub-screens
        self.screen            = pygame.display.set_mode(self.screenSize)
        self.gameScreen        = self.screen.subsurface(Rect((0, 0), self.gameSize))
        self.gameScreen.fill(self.background)

        # Disassembler menu
        self.disModule.setScreen(self.screen.subsurface(Rect((self.gameSize[0], 0), (self.disModule.width, self.disModule.height))))

        self.shader = shaders.default
        pygame.mixer.music.load(self.tone)

    def sound(self, play):
        if play:
            pygame.mixer.music.play()
        else: 
            pygame.mixer.music.stop()


    def clear(self):
        self.gameScreen.fill(self.background)
        pygame.display.flip()

    def fullRender(self, ctx):
        s = self.scale
        self.clear()
        for (x, y) in np.ndindex(ctx.shape):
            if ctx[x, y]:
                pygame.draw.rect(
                    self.gameScreen, 
                    self.shader(self, x, y), 
                    (x * s, y * s, s, s),
                )
        pygame.display.flip()

    def render(self, ctx, x, y, rows):
        s = self.scale
        for xOff in range(8):
            for yOff in range(rows):
                rx = (x + xOff) % self.gameWidth
                ry = (y + yOff) % self.gameHeight
                pygame.draw.rect(
                    self.gameScreen, 
                    self.shader(self, rx, ry) if ctx[rx, ry] else self.background, 
                    (rx * s, ry * s, s, s),
                )
        pygame.display.update(Rect(x * s, y * s, 8 * s, rows * s))
