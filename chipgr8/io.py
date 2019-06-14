import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import sys
import time
import pygame

from pygame.locals import *
from pygame import event
import os

import chipgr8.core         as core
import chipgr8.shaders      as shaders
import chipgr8.disassembler as disassembler

class ChipGr8Window():

    screen      = None
    scale       = 10
    gameSize    = (0, 0)
    screenSize  = (0, 0)
    background  = (0,   0,   0)
    foreground  = (255, 255, 255)
    menu        = (200, 200, 210)
    fontCol     = (80, 80, 80)
    lineFontCol = (150, 150, 150)
    fontBackCol = (240, 240, 240)
    disScrollY  = 0
    disLen      = 0
    disassemblyWidth = 300
    tone        = os.path.realpath(os.path.join(__file__, "../../data/sound/pureTone.mp3"))

    def __init__(self, gameWidth, gameHeight):
        pygame.init()
        pygame.font.init()

        self.gameSize          = gameWidth * self.scale, gameHeight * self.scale
        self.screenSize        = (self.gameSize[0] + self.disassemblyWidth, self.gameSize[1])
        self.gameWidth         = gameWidth
        self.gameHeight        = gameHeight

        # Create display screen and sub-screens
        self.screen            = pygame.display.set_mode(self.screenSize)
        self.gameScreen        = self.screen.subsurface(Rect((0, 0), self.gameSize))
        self.gameScreen.fill(self.background)

        # Disassembler menu - TODO: Aesthetic fixes, scroll bar, customizeable font size/colour?
        self.fontSize = 26
        self.lineHeight = 24
        self.font = pygame.font.Font(None, self.fontSize)
        self.disassemblyMenu   = self.screen.subsurface(Rect((self.gameSize[0], 0), (self.disassemblyWidth, self.gameSize[1])))
        self.disassemblyScroll = pygame.surface.Surface((self.disassemblyWidth, self.gameSize[1]))
        self.disassemblyMenu.fill(self.fontBackCol)
        self.disassemblyScroll.fill(self.fontBackCol)

        self.shader = shaders.default
        pygame.mixer.music.load(self.tone)

    def sound(self, play):
        if play:
            pygame.mixer.music.play()
        else: 
            pygame.mixer.music.stop()

    def initDisassemblyText(self, inPath):
        self.disScrollY = 0
        
        disSrc = disassembler.disassemble(inPath=inPath)
        disSrc = disSrc.split('\n')
        self.disLen = len(disSrc)

        # Create new surface with height corresponding to file length
        self.disassemblyScroll = pygame.surface.Surface((self.disassemblyWidth, self.lineHeight * self.disLen + self.gameSize[1]))
        self.disassemblyScroll.fill(self.fontBackCol)

        # Add text to surface
        # For loop needed since newlines don't work in pygame
        for i in range(self.disLen):
            self.disassemblyScroll.blit(self.font.render(str(i + 1), True, self.lineFontCol, self.fontBackCol), (0, i * self.lineHeight))
            self.disassemblyScroll.blit(self.font.render(disSrc[i], True, self.fontCol, self.fontBackCol), (40, i * self.lineHeight))

    def scrollDisassemblyUp(self):
        self.disScrollY -= self.lineHeight * 2
        if self.disScrollY < 0:
            self.disScrollY = 0

    def scrollDisassemblyDown(self):
        self.disScrollY += self.lineHeight * 2
        max = (self.disLen - 1) * self.lineHeight
        if self.disScrollY > max:
            self.disScrollY = max

    # Update the disassembly menu
    def renderDisassembly(self):
        self.disassemblyMenu.blit(self.disassemblyScroll, (10, 10 - self.disScrollY))
        pygame.display.update(Rect(self.gameSize[0], 0, self.disassemblyWidth, self.gameSize[1]))

    def clear(self):
        self.gameScreen.fill(self.background)

    def fullRender(self, ctx):
        s = self.scale
        self.clear()
        for x in range(self.gameWidth):
            for y in range(self.gameHeight):
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
        pygame.display.update((x * s, y * s, 8 * s, rows * s))

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
