import chipgr8
import math

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
ANTIALIAS        = True
CURSOR_SWITCH_MS = 500
VALID_CHARACTERS = '''
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789
 ~!@#$%^&*()_-+={}[]|\\:;'"<>,.?/
'''

class ConsoleModule(object):

    __bufferedSurfaces = []
    __cursorSurface    = None
    __screen           = None
    __locals           = {}
    __globals          = {}

    def __init__(
        self,
        screen,
        prompt     = '> ',
        foreground = (255, 255, 255),
        background = (0, 0, 0),
    ):
        self.font            = Font(match_font('monospace'), 16)
        self.prompt          = prompt
        self.foreground      = foreground
        self.background      = background
        self.inputLine       = ''
        self.outputLines     = []
        self.history         = []
        self.historyPos      = -1
        self.cursorPos       = 0
        self.cursorOn        = False
        self.cursorCount     = 0
        self.clock           = Clock()
        self.__cursorSurface = Surface((1, self.font.get_height()))
        self.__screen        = screen
        self.__globals       = {
            'chipgr8'     : chipgr8,
            'findROM'     : chipgr8.findROM,
            'Query'       : chipgr8.Query,
            'Observer'    : chipgr8.Observer,
            'write'       : chipgr8.util.write,
            'read'        : chipgr8.util.read,
            'math'        : math,
        }

        ## Clear surface
        self.__cursorSurface.fill(self.foreground)
        self.__screen.fill(self.foreground)
        self.__screen.fill(self.background, rect=(
            0, 1,
            self.__screen.get_width(),
            self.__screen.get_height() - 1,
        ))
        self.update([])
        self.render()

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
        self.outputLines = (
            [str(self.evaluate(self.inputLine))] + 
            self.outputLines[:MAX_LINES - 1]
        )
        self.history.insert(0, self.inputLine)
        self.historyPos = -1
        self.inputLine  = ''
        for (i, outputLine) in enumerate(self.outputLines):
            self.__bufferedSurfaces.append((
                self.font.get_height() * (i + 1),
                self.font.render(outputLine, ANTIALIAS, self.foreground),
            ))

    def evaluate(self, source):
        try:    return eval(source, self.__globals, self.__locals)
        except: pass
        try:    return exec(source, self.__globals, self.__locals)
        except Exception as error:
            return error

    def render(self):
        for (y, surface) in self.__bufferedSurfaces:
            self.__screen.fill(self.background, rect=(
                MARGIN,
                MARGIN + y,
                self.__screen.get_width(),
                self.font.get_height(),
            ))
            self.__screen.blit(surface, (MARGIN, MARGIN + y))
        self.__bufferedSurfaces.clear()

    def update(self, events, ignores=[]):
        for event in events:
            if event.type in ignores:
                continue
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
        surface = self.font.render(
            self.prompt + self.inputLine, 
            ANTIALIAS, 
            self.foreground,
        )

        # Toggle cursor if needed
        self.cursorCount += self.clock.get_time()
        if self.cursorCount >= CURSOR_SWITCH_MS:
            self.cursorCount %= CURSOR_SWITCH_MS
            self.cursorOn     = not self.cursorOn

        if self.cursorOn:
            x = self.font.size(self.prompt + self.inputLine[:self.cursorPos])[0]
            # Without this, the cursor is invisible when self.cursorPosition > 0:
            if self.cursorPos > 0:
                x -= self.__cursorSurface.get_width()
            surface.blit(self.__cursorSurface, (x, 0))

        self.clock.tick()
        self.__bufferedSurfaces.append((0, surface))
