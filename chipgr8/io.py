import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import sys
import time
import pygame
import numpy as np

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
    currDisassemblyLine = 1
    disScrollChange  = False
    disassemblyWidth = 300
    disHighlight = None
    disHighlightColour = (242, 231, 163)
    disHighlightAlpha = 128
    tone        = os.path.realpath(os.path.join(__file__, "../../data/sound/pureTone.mp3"))

    # TODO: Modularize warning tooltip
    warning     = os.path.realpath(os.path.join(__file__, "../../data/ui/warning.png"))
    warningSize = (50, 50)
    displayWarning = False
    minWarningAlpha = 150
    currWarningAlpha = 150
    warningIsHovered = False
    warningFadeTime = 30


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
        self.fontSize = 24
        self.lineHeight = 24
        self.font = pygame.font.Font(None, self.fontSize)
        self.disassemblyMenu   = self.screen.subsurface(Rect((self.gameSize[0], 0), (self.disassemblyWidth, self.gameSize[1])))
        self.disassemblyScroll = pygame.surface.Surface((self.disassemblyWidth, self.gameSize[1]))
        self.disassemblyMenu.fill(self.fontBackCol)
        self.disassemblyScroll.fill(self.fontBackCol)
        self.disHighlight = pygame.Surface((self.disassemblyWidth, self.lineHeight))
        self.disHighlight.set_alpha(self.disHighlightAlpha)
        self.disHighlight.fill(self.disHighlightColour)

        # Warning tooltip
        self.warningImg = pygame.transform.scale(pygame.image.load(self.warning), self.warningSize).convert()
        self.warningImg.set_colorkey((0, 0, 0))
        self.warningPos = (self.disassemblyWidth - self.warningSize[0] - 10, self.gameSize[1] - self.warningSize[1] - 10)

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
        labelCounter = 0
        for i in range(self.disLen):
            if len(disSrc[i]) > 0 and disSrc[i][0] is '.':
                self.disassemblyScroll.blit(self.font.render(disSrc[i], True, self.fontCol, self.fontBackCol), (40, (i - labelCounter) * self.lineHeight))
                labelCounter += 1
                continue

            self.disassemblyScroll.blit(self.font.render(str(i - labelCounter + 1), True, self.lineFontCol, self.fontBackCol), (0, (i - labelCounter) * self.lineHeight))
            self.disassemblyScroll.blit(self.font.render(disSrc[i], True, self.fontCol, self.fontBackCol), (120, (i - labelCounter) * self.lineHeight))

        # Subtract labels from line count
        self.disLen -= labelCounter

    def getLastDisassemblyLine(self):
        return self.disLen
    
    def scrollDisassemblyUp(self, numLines=2):
        self.disScrollChange = True
        self.disScrollY -= self.lineHeight * numLines
        if self.disScrollY < 0:
            self.disScrollY = 0

    def scrollDisassemblyDown(self, numLines=2):
        self.disScrollChange = True
        self.disScrollY += self.lineHeight * numLines
        max = (self.disLen - 1) * self.lineHeight
        if self.disScrollY > max:
            self.disScrollY = max

    def setCurrDisassemblyLine(self, numLines):
        if numLines > self.disLen or numLines < 1:
            return
        self.currDisassemblyLine = numLines

    def scrollDissassemblyToCurrLine(self):
        self.scrollDissassemblyToLine(self.currDisassemblyLine)

    def offsetScrollDisassembly(self, numLines=1):
        self.disScrollChange = True
        self.disScrollY += self.lineHeight * numLines
        if self.disScrollY < 0:
            self.disScrollY = 0
        max = (self.disLen - 1) * self.lineHeight
        if self.disScrollY > max:
            self.disScrollY = max

    def scrollDissassemblyToLine(self, numLines, centre=True):
        self.disScrollChange = True
        centringValue = self.gameSize[1] // self.lineHeight // 2 if centre else 0
        self.disScrollY = self.lineHeight * (numLines - centringValue)
        if self.disScrollY < 0:
            self.disScrollY = 0
        max = (self.disLen - 1) * self.lineHeight
        if self.disScrollY > max:
            self.disScrollY = max

    # Update the disassembly menu
    def renderDisassembly(self, override=False, highlight=False):
        # TODO: Separate warning tooltip
        if self.disScrollChange or override \
                or (self.warningRect().collidepoint(pygame.mouse.get_pos()) and self.currWarningAlpha != 255) \
                or (not self.warningRect().collidepoint(pygame.mouse.get_pos()) and self.currWarningAlpha != self.minWarningAlpha):
            self.disassemblyMenu.fill(self.fontBackCol)
            self.disassemblyMenu.blit(self.disassemblyScroll, (10, 10 - self.disScrollY))
            if highlight:
                self.disassemblyMenu.blit(self.disHighlight, (0, 5 + (self.currDisassemblyLine - 1) * self.lineHeight - self.disScrollY))
            self.disScrollChange = False


            if self.displayWarning:
                alphaDiff = (255 - self.minWarningAlpha) / self.warningFadeTime
                if self.warningRect().collidepoint(pygame.mouse.get_pos()): # Is hovered
                    self.currWarningAlpha = min(self.currWarningAlpha + alphaDiff, 255)
                else: # Is not hovered
                    self.currWarningAlpha = max(self.currWarningAlpha - alphaDiff, self.minWarningAlpha)
                self.warningImg.set_alpha(self.currWarningAlpha)
                self.disassemblyMenu.blit(self.warningImg, self.warningPos)


            pygame.display.update(Rect(self.gameSize[0], 0, self.disassemblyWidth, self.gameSize[1]))

    def warningRect(self):
        return self.warningImg.get_rect(left=self.warningPos[0] + self.gameSize[0], top=self.warningPos[1])

    def setWarningStatus(self, status):
        self.displayWarning = status



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
