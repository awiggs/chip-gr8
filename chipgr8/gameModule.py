from chipgr8.module import Module
from pygame         import draw

class GameModule(Module):

    __diff = None

    def __init__(
        self,
        surface,
        theme
    ):
        super().__init__(surface, theme)
        self.surface.fill(self.theme.background)

    def render(self):
        diff = self.__diff
        self.__diff = None
        return diff

    def update(self, vm, events):

        # Clear screen
        if vm.VM.diffClear: self.clearUpdate()
        elif not vm.VM.diffSize: return
        elif vm.smooth:     self.smoothUpdate(vm)
        else:               self.diffUpdate(vm)

    def clearUpdate(self):
        self.surface.fill(self.theme.background)
        self.__diff = self.bounds

    def diffUpdate(self, vm):
        s               = self.theme.scale
        ctx             = vm.ctx()
        (width, height) = ctx.shape
        (x, y, rows)    = vm.VM.diffX, vm.VM.diffY, vm.VM.diffSize
        for xOff in range(8):
            for yOff in range(rows):
                rx = (x + xOff) % width
                ry = (y + yOff) % height
                draw.rect(
                    self.surface,
                    self.theme.foreground if ctx[rx, ry] else self.theme.background,
                    (rx * s, ry * s, s, s),
                )
        self.__diff = self.bounds

    def smoothUpdate(self, vm):
        if vm.smooth and vm.VM.diffSkip:
            return
        self.fullUpdate(vm)

    def fullUpdate(self, vm):
        s               = self.theme.scale
        ctx             = vm.ctx()
        (width, height) = ctx.shape
        self.surface.fill(self.theme.background)
        for x in range(width):
            for y in range(height):
                if ctx[x, y]: 
                    draw.rect(
                        self.surface,
                        self.theme.foreground,
                        (x * s, y * s, s, s),
                    )
        self.__diff = self.bounds