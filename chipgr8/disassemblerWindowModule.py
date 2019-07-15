import os
import pygame
from pygame.locals import *

import chipgr8.disassembler as disassembler

# TODO: Aesthetic fixes, scroll bar, customizeable font size/colour?
class DisassemblerWindowModule:

    fontCol     = (80, 80, 80)
    lineFontCol = (150, 150, 150)
    fontBackCol = (240, 240, 240)
    disScrollY  = 0
    disLen      = 0
    currDisassemblyLine = 1
    disScrollChange  = False
    width = 300
    height = 0
    disHighlight = None
    disHighlightColour = (139, 182, 252)
    disHighlightAlpha = 128

    # TODO: Modularize warning tooltip
    warning          = os.path.realpath(os.path.join(__file__, "../../data/ui/warning.png"))
    warningSize      = (50, 50)
    displayWarning   = False
    minWarningAlpha  = 150
    currWarningAlpha = 150
    warningIsHovered = False
    warningFadeTime  = 30

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.fontSize = 16
        self.lineHeight = 24
        self.font = pygame.font.SysFont("monospace", self.fontSize)
        self.disassemblyScroll = pygame.surface.Surface((self.width, self.height))
        self.disassemblyScroll.fill(self.fontBackCol)
        self.disHighlight = pygame.Surface((self.width, self.lineHeight))
        self.disHighlight.set_alpha(self.disHighlightAlpha)
        self.disHighlight.fill(self.disHighlightColour)

        self.offset = (0, 0)

        self.warningPos = (self.width - self.warningSize[0] - 10, self.height - self.warningSize[1] - 10)

    def setScreen(self, screen):
        self.disassemblyMenu = screen
        self.disassemblyMenu.fill(self.fontBackCol)
        self.offset = self.disassemblyMenu.get_offset() if self.disassemblyMenu.get_offset() else (0, 0)

        self.warningImg = pygame.transform.scale(pygame.image.load(self.warning), self.warningSize).convert()
        self.warningImg.set_colorkey((0, 0, 0))

    def initText(self, inPath):
        self.disScrollY = 0
        
        disSrc = disassembler.disassemble(inPath=inPath)
        disSrc = disSrc.split('\n')
        self.disLen = len(disSrc)

        # Create new surface with height corresponding to file length
        self.disassemblyScroll = pygame.surface.Surface((self.width, self.lineHeight * self.disLen + self.height))
        self.disassemblyScroll.fill(self.fontBackCol)

        # Add text to surface
        # For loop needed since newlines don't work in pygame
        labelCounter = 0
        for i in range(self.disLen):
            if len(disSrc[i]) > 0 and disSrc[i][0] is '.': # Is label
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
        centringValue = self.height // self.lineHeight // 2 if centre else 0
        self.disScrollY = self.lineHeight * (numLines - centringValue)
        if self.disScrollY < 0:
            self.disScrollY = 0
        max = (self.disLen - 1) * self.lineHeight
        if self.disScrollY > max:
            self.disScrollY = max

    # Update the disassembly menu
    def render(self, override=False, highlight=False):
        # TODO: Separate warning tooltip
        if self.disassemblyMenu == None:
            return

        if self.disScrollChange or override \
                or (self.displayWarning and self.warningRect().collidepoint(pygame.mouse.get_pos()) and self.currWarningAlpha != 255) \
                or (self.displayWarning and not self.warningRect().collidepoint(pygame.mouse.get_pos()) and self.currWarningAlpha != self.minWarningAlpha):
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

            pygame.display.update(Rect(self.offset[0], self.offset[1], self.width, self.height))

    def warningRect(self):
        return self.warningImg.get_rect(left=self.warningPos[0] + self.offset[0], top=self.warningPos[1])

    def setWarningStatus(self, status):
        self.displayWarning = status
