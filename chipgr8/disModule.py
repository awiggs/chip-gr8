import pygame

from chipgr8.module       import Module
from chipgr8.disassembler import disassemble

MARGIN = 10

class DisModule(Module):

    __disSurface       = None
    __hlSurface        = None
    __lastClock        = 0
    __yChanged         = False
    __ROM              = ''

    def __init__(self, surface, theme):
        super().__init__(surface, theme)
        self.y      = 0
        self.hl     = 0
        self.dis    = []
        self.surface.fill(self.theme.foreground)
        self.surface.fill(self.theme.background, rect=(
            1, 0,
            self.surface.get_width() - 1,
            self.surface.get_height(),
        ))

    def render(self):
        if not self.__yChanged or not self.__disSurface:
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
        self.__yChanged = False
        return super().render()

    def update(self, vm, events):
        if vm.VM.clock == self.__lastClock:
            return
        if self.__ROM != vm.ROM:
            self.__ROM = vm.ROM
            self.initDis(vm.ROM)
        self.__lastClock = vm.VM.clock
        self.hl          = (vm.VM.PC[0] - 0x200) // 2
        self.scrollTo(self.hl - 3)

    def initDis(self, inPath):
        lineHeight = self.theme.font.get_height()
        self.dis   = [
            '{:03X}'.format(i) + ' ' + source
            for (i, source)
            in enumerate(disassemble(
                inPath   = inPath, 
                labelSep = '',
                prefix   = ' ' * 10,
            ).split('\n'))
        ]
        self.__disSurface = pygame.Surface((299, lineHeight * (len(self.dis) + 100)))
        self.__hlSurface  = pygame.Surface((299, lineHeight * len(self.dis)))
        self.__disSurface.fill(self.theme.background)
        self.__hlSurface.fill(self.theme.foreground)
        for (i, source) in enumerate(self.dis):
            self.__disSurface.blit(
                self.theme.font.render(
                    source,
                    self.theme.antialias,
                    self.theme.foreground,
                ),
                (2, i * lineHeight)
            )
            self.__hlSurface.blit(
                self.theme.font.render(
                    source,
                    self.theme.antialias,
                    self.theme.background,
                ),
                (2, i * lineHeight)
            )

    def scrollTo(self, y):
        oldY            = self.y
        self.y          = min(max(y, 0), len(self.dis) - 10)
        self.__yChanged = True

    def scrollUp(self, lines=2):
        self.scrollTo(self.y - lines)

    def scrollDown(self, lines=2):
        self.scrollTo(self.y + lines)