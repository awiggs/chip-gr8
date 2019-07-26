import pygame
import logging

logger = logging.getLogger(__name__)

from chipgr8.module       import Module
from chipgr8.disassembler import disassemble

class DisModule(Module):

    __addrTable      = None
    __disSurface     = None
    __hlSurface      = None
    __ulSurface      = None
    __lastClock      = 0
    __yChanged       = False
    __ROM            = ''
    __mouseOverLine  = -1
    __showUnderlines = False

    def __init__(self, surface, theme):
        super().__init__(surface, theme)
        self.y   = 0
        self.hl  = 0
        self.dis = []
        self.__brkSurface = self.theme.font.render(
            '*',
            self.theme.antialias,
            self.theme.foreground,
            self.theme.background,
        )
        self.__brkHlSurface = self.theme.font.render(
            '*',
            self.theme.antialias,
            self.theme.background,
            self.theme.foreground,
        )
        self.__brkSep = self.theme.font.render(
            '   ',
            self.theme.antialias,
            self.theme.background,
            self.theme.foreground,
        ).get_width() + 2
        self.surface.fill(self.theme.foreground)
        self.surface.fill(self.theme.background, rect=(
            1, 0,
            self.surface.get_width() - 1,
            self.surface.get_height(),
        ))

    def render(self, force=False, breakpoints=[]):
        if not self.__disSurface or (not self.__yChanged and not force):
            return None
        lineHeight = self.theme.font.get_height()
        self.surface.blit(
            self.__disSurface, 
            (1, 0), 
            (0, self.y * lineHeight, 299, self.surface.get_height())
        )
        self.surface.blit(
            self.__hlSurface,
            (1, (self.hl - self.y) * lineHeight),
            (0, self.hl * lineHeight, 299, lineHeight)
        )
        if self.__showUnderlines:
            underlinedSurface = self.__hulSurface if self.hl == self.__mouseOverLine else self.__ulSurface
            self.surface.blit(
                underlinedSurface,
                (1, (self.__mouseOverLine - self.y) * lineHeight),
                (0, self.__mouseOverLine * lineHeight, 299, lineHeight)
            )
        for addr in breakpoints:
            line = self.__addrTable.get(addr, 0)
            self.surface.blit(
                self.__brkHlSurface if self.hl == line else self.__brkSurface,
                (self.__brkSep, (line - self.y) * lineHeight)
            )
        self.__yChanged = False
        return super().render()

    def update(self, vm, events):
        if not vm.ROM:
            return
        if vm.VM.clock == self.__lastClock and self.__ROM == vm.ROM:
            return
        if self.__ROM != vm.ROM:
            self.__ROM = vm.ROM
            self.initDis(vm.ROM)
        self.__lastClock = vm.VM.clock
        if vm.autoScroll or vm.paused:
            self.hl = self.__addrTable.get(vm.VM.PC, 0)
            self.scrollTo(self.hl - 3)
        else:
            self.hl = -1
            self.__yChanged = True

    def initDis(self, inPath):
        lineHeight = self.theme.font.get_height()
        self.__addrTable = {}
        self.dis = disassemble(
            inPath    = inPath, 
            srcFormat = '{addr:03X} {label:11s}{instruction}\n',
            addrTable = self.__addrTable,
        ).strip().split('\n')
        self.__disSurface = pygame.Surface((299, lineHeight * (len(self.dis) + 100)))
        self.__hlSurface  = pygame.Surface((299, lineHeight * len(self.dis)))
        self.__ulSurface  = pygame.Surface((299, lineHeight * len(self.dis)))
        self.__hulSurface = pygame.Surface((299, lineHeight * len(self.dis)))
        self.__disSurface.fill(self.theme.background)
        self.__hlSurface.fill(self.theme.foreground)
        self.__ulSurface.fill(self.theme.background)
        self.__hulSurface.fill(self.theme.foreground)
        for (i, source) in enumerate(self.dis):
            self.__disSurface.blit(
                self.theme.font.render(
                    source,
                    self.theme.antialias,
                    self.theme.foreground,
                    self.theme.background,
                ),
                (2, i * lineHeight)
            )
            self.__hlSurface.blit(
                self.theme.font.render(
                    source,
                    self.theme.antialias,
                    self.theme.background,
                    self.theme.foreground,
                ),
                (2, i * lineHeight)
            )

        self.__ulSurface = self.__disSurface.copy()
        self.__hulSurface = self.__hlSurface.copy()
        for (i, source) in enumerate(self.dis):
            # Find label names used in instructions
            label = source.rpartition(".")
            if label[1] is not '.' or len(label[2].partition(" ")[2]) > 0:
                continue

            # Calculate label offset
            ulOffset = self.theme.font.render(label[0], True, (0,0,0), (0,0,0)).get_width()

            self.theme.font.set_underline(True)
            self.__ulSurface.blit(
                self.theme.font.render(
                    ('.' + label[2]),
                    self.theme.antialias,
                    self.theme.foreground,
                    self.theme.background
                ),
                (2 + ulOffset, i * lineHeight)
            )
            self.theme.font.set_underline(False)
            
            self.theme.font.set_underline(True)
            self.__hulSurface.blit(
                self.theme.font.render(
                    ('.' + label[2]),
                    self.theme.antialias,
                    self.theme.background,
                    self.theme.foreground
                ),
                (2 + ulOffset, i * lineHeight)
            )
            self.theme.font.set_underline(False)

    def scrollTo(self, y):
        oldY            = self.y
        self.y          = min(max(y, 0), len(self.dis) - 10)
        self.__yChanged = True

    def scrollUp(self, lines=2):
        self.scrollTo(self.y - lines)

    def scrollDown(self, lines=2):
        self.scrollTo(self.y + lines)

    def getClickedAddr(self, pos):
        offset = self.surface.get_abs_offset()
        pos = (pos[0] - offset[0], pos[1] - offset[1])
        if pos[0] < 0 or pos[0] > self.surface.get_width() or pos[1] < 0 or pos[1] > self.surface.get_height():
            return -1

        index = pos[1] // self.theme.font.get_height() + self.y
        if index >= len(self.dis):
            return -1

        try:
            return int(self.dis[index].partition(" ")[0], 16)
        except ValueError:
            logger.error('Clicked disassembly line did not start with hex address')
            return -1

    def updateMouseOverLine(self, pos):
        offset = self.surface.get_abs_offset()
        pos = (pos[0] - offset[0], pos[1] - offset[1])
        line = -1
        if not (pos[0] < 0 or pos[0] > self.surface.get_width() or pos[1] < 0 or pos[1] > self.surface.get_height()):
            line = pos[1] // self.theme.font.get_height() + self.y

        if self.__mouseOverLine is not line:
            self.__yChanged = True
        self.__mouseOverLine = line

    def showUnderlines(self, enable):
        self.__showUnderlines = enable

    def jumpToMousedLabel(self):
        if self.__mouseOverLine < 0 or self.__mouseOverLine >= len(self.dis):
            return
        
        # Find label names used in instructions
        label = self.dis[self.__mouseOverLine].rpartition(".")
        if label[1] is not '.' or len(label[2].partition(" ")[2]) > 0:
            return

        # label[2] contains the label without the '.' prefix
        for (i, lineText) in enumerate(self.dis):
            candidate = lineText.partition("." + label[2])
            # Confirm that candidate label match is an actual label, and not
            # matching part of another label (e.g. .label_1 matches .label_11)
            if len(candidate[2]) > 0 and not candidate[2][0].isdigit():
                self.scrollTo(i - 3)