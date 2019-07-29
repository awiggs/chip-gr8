import os
import pygame
import chipgr8

from chipgr8.controlModule import ControlModule
from chipgr8.gameModule    import GameModule
from chipgr8.consoleModule import ConsoleModule
from chipgr8.statusModule  import StatusModule
from chipgr8.disModule     import DisModule
from chipgr8.regModule     import RegModule

MIN_FRAMES = 16

class Window():

    def __init__(
        self, 
        gameWidth,
        gameHeight,
        scale      = 10,
        foreground = (255, 255, 255),
        background = (0, 0, 0),
        antialias  = True,
        tone       = os.path.realpath(os.path.join(__file__, '../data/sound/pureTone.mp3')),
        icon       = os.path.realpath(os.path.join(__file__, '../data/icon.png'))
    ):
        pygame.init()
        pygame.font.init()
        # pygame.mixer.music.load(tone)

        self.scale      = scale
        self.foreground = foreground
        self.background = background
        self.antialias  = antialias
        self.lastFrame  = 0

        (w, h)          = gameWidth * self.scale, gameHeight * self.scale
        self.gameSize   = gameWidth * self.scale, gameHeight * self.scale
        self.screenSize = (w + 300, h + 290)
        self.screen     = pygame.display.set_mode(self.screenSize)
        self.font       = pygame.font.Font(pygame.font.match_font('monospace') , 16)
        pygame.display.set_caption(chipgr8.DESCRIPTION)
        pygame.display.set_icon(pygame.image.load(icon))

        self.controlModule = ControlModule()
        self.gameModule = GameModule(
            self.screen.subsurface((0, 0, w, h)), 
            self,
        )
        self.consoleModule = ConsoleModule(
            self.screen.subsurface((0, h, w, 270)),
            self,
        )
        self.statusModule = StatusModule(
            self.screen.subsurface((0, h + 270, w + 300, 20)),
            self,
        )
        self.disModule = DisModule(
            self.screen.subsurface((w, 0, 300, h)),
            self,
        )
        self.regModule = RegModule(
            self.screen.subsurface((w, h, 300, 270)),
            self
        )
        pygame.display.flip()

    def sound(self, play):
        if play:
            pass # pygame.mixer.music.play()
        else: 
            pass # ygame.mixer.music.stop()

    def refresh(self, vm):
        self.update(vm)
        self.gameModule.fullUpdate(vm)
        pygame.display.flip()

    def update(self, vm):
        events = self.controlModule.update(vm, pygame.event.get())
        self.gameModule.update(vm, events)
        self.consoleModule.update(vm, events)
        self.statusModule.update(vm, events)
        self.disModule.update(vm, events)
        self.regModule.update(vm, events)

    def render(self, force=False, breakpoints=[]):
        gameBounds      = self.gameModule.render()
        self.lastFrame += 1
        if gameBounds or force or self.lastFrame > MIN_FRAMES:
            self.lastFrame = 0
            pygame.display.update([bounds
                for bounds
                in [
                    gameBounds,
                    self.consoleModule.render(),
                    self.statusModule.render(),
                    self.disModule.render(force=force, breakpoints=breakpoints),
                    self.regModule.render(),
                ] if bounds
            ])
