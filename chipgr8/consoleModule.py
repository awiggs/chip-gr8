import math
import logging
import chipgr8
import traceback

logger = logging.getLogger(__name__)

from .module import Module

from pygame.locals import (
    KEYDOWN, 
    K_LEFT, 
    K_RIGHT, 
    K_UP, 
    K_DOWN, 
    K_BACKSPACE, 
    K_DELETE,
    K_RETURN,
)
from pygame      import Surface
from pygame.font import Font, match_font
from pygame.time import Clock

MARGIN           = 10
MAX_LINES        = 14
CURSOR_SWITCH_MS = 500
VALID_CHARACTERS = '''
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    abcdefghijklmnopqrstuvwxyz
    0123456789
    ~!@#$%^&*()_-+={}[]|\\:;'"<>,.?/
'''

class ConsoleModule(Module):

    __bufferedSurfaces = []
    __cursorSurface    = None
    __locals           = {}
    __globals          = {}

    def __init__(
        self,
        surface,
        theme,
        prompt = '> ',
    ):
        super().__init__(surface, theme)
        self.prompt          = prompt
        self.inputLine       = ''
        self.outputLines     = []
        self.history         = []
        self.historyPos      = -1
        self.cursorPos       = 0
        self.cursorOn        = False
        self.cursorCount     = 0
        self.clock           = Clock()
        self.__cursorSurface = Surface((1, self.theme.font.get_height()))
        self.__globals       = {
            'chipgr8'     : chipgr8,
            'Observer'    : chipgr8.Observer,
            'write'       : chipgr8.util.write,
            'read'        : chipgr8.util.read,
            'math'        : math,
        }

        ## Clear surface
        self.__cursorSurface.fill(self.theme.foreground)
        self.surface.fill(self.theme.foreground)
        self.surface.fill(self.theme.background, rect=(
            0, 1,
            self.surface.get_width(),
            self.surface.get_height() - 1,
        ))

    def insert(self, key):
        if key in VALID_CHARACTERS:
            self.inputLine = (
                self.inputLine[:self.cursorPos] + 
                key + 
                self.inputLine[self.cursorPos:]
            )
            self.cursorPos += len(key)

    def delete(self):
        back = max(self.cursorPos - 1, 0)
        self.inputLine = self.inputLine[:back] + self.inputLine[self.cursorPos:]
        self.cursorPos = back

    def left(self):
        self.cursorPos = max(self.cursorPos - 1, 0)

    def right(self):
        self.cursorPos = min(self.cursorPos + 1, len(self.inputLine))

    def up(self):
        if not self.history:
            return
        newHistoryPos   = min(self.historyPos + 1, len(self.history) - 1)
        self.inputLine  = self.history[newHistoryPos]
        self.historyPos = newHistoryPos
        self.cursorPos  = len(self.inputLine)
    
    def down(self):
        newHistoryPos   = max(self.historyPos - 1, -1)
        self.inputLine  = '' if newHistoryPos == -1 else self.history[newHistoryPos]
        self.historyPos = newHistoryPos
        self.cursorPos  = len(self.inputLine)

    def submit(self):
        inputLine = self.inputLine.strip()
        if inputLine: 
            self.history.insert(0, inputLine)

        outputLine = str(self.evaluate(inputLine))
        if outputLine:
            self.outputLines = (
                [outputLine] + 
                self.outputLines[:MAX_LINES - 1]
            )
            self.historyPos = -1
            for (i, outputLine) in enumerate(self.outputLines):
                self.__bufferedSurfaces.append((
                    self.theme.font.get_height() * (i + 1),
                    self.theme.font.render(outputLine, self.theme.antialias, self.theme.foreground),
                ))
        self.inputLine = ''
        self.cursorPos = 0

    def evaluate(self, source):
        logger.debug('evaluating `{}`'.format(source))
        try:
            try:    
                return eval(source, self.__globals, self.__locals)
            except SyntaxError as error:
                logger.debug('eval `{}` raised `{}`'.format(source, error), exc_info=error)            
            exec(source, self.__globals, self.__locals)
            return ''
        except Exception as error:
            logger.error('exec: `{}` raised `{}`'.format(source, error), exc_info=error)
            return error

    def render(self):
        if not self.__bufferedSurfaces:
            return None
        for (y, surface) in self.__bufferedSurfaces:
            self.surface.fill(self.theme.background, rect=(
                MARGIN,
                MARGIN + y,
                self.surface.get_width(),
                self.theme.font.get_height(),
            ))
            self.surface.blit(surface, (MARGIN, MARGIN + y))
        self.__bufferedSurfaces.clear()
        return super().render()

    def update(self, vm, events):
        if vm.paused and 'vm' not in self.__globals:
            self.initGlobals(vm)            
        for event in events:
            if event.type == KEYDOWN:
                key           = event.key
                self.cursorOn = True  # So the user sees where he writes

                if   key == K_BACKSPACE: self.delete()
                elif key == K_DELETE:    self.delete()
                elif key == K_RETURN:    self.submit()
                elif key == K_LEFT:      self.left()
                elif key == K_RIGHT:     self.right()
                elif key == K_UP:        self.up()
                elif key == K_DOWN:      self.down()
                else:                    self.insert(event.unicode)

        # Re-render inputLine surface
        surface = self.theme.font.render(
            self.prompt + self.inputLine + ' ', 
            self.theme.antialias, 
            self.theme.foreground,
        )

        # Toggle cursor if needed
        self.cursorCount += self.clock.get_time()
        if self.cursorCount >= CURSOR_SWITCH_MS:
            self.cursorCount %= CURSOR_SWITCH_MS
            self.cursorOn     = not self.cursorOn

        self.cursorOn = self.cursorOn and vm.paused
        if self.cursorOn:
            x = self.theme.font.size(self.prompt + self.inputLine[:self.cursorPos])[0]
            if self.cursorPos > 0:
                x -= self.__cursorSurface.get_width()
            surface.blit(self.__cursorSurface, (x, 0))

        self.clock.tick()
        self.__bufferedSurfaces.append((0, surface))

    def initGlobals(self, vm):
        
        def play():
            vm.paused = False
            return 'Resumed.'

        def reset():
            return vm.reset()

        def step():
            vm.step()
            return 'Stepped.'

        def Query():
            return chipgr8.Query(vm)
        
        self.__globals['vm']    = vm
        self.__globals['play']  = play
        self.__globals['reset'] = reset
        self.__globals['step']  = step 
        self.__globals['Query'] = Query