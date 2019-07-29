import os

from chipgr8.module import Module

class StatusModule(Module):

    __bufferedSurface = None

    def __init__(
        self,
        surface,
        theme,
    ):
        super().__init__(surface, theme)
        self.status     = ''
        self.surface.fill(self.theme.foreground)
        self.surface.fill(self.theme.background, rect=(
            0, 1,
            self.surface.get_width(),
            self.surface.get_height() - 1,
        ))

    def render(self):
        if self.__bufferedSurface:
            self.surface.blit(self.__bufferedSurface, (2, 2))
            return super().render()

    def update(self, vm, events):
        newStatus = '{}    SPS: {:<4.0f}   ROM: {}'.format(
            'PAUSED ' if vm.paused else 'PLAYING',
            0 if vm.paused else vm.pyclock.get_fps(),
            os.path.basename(vm.ROM) if vm.ROM else 'None',
        )
        if newStatus != self.status:
            self.status = newStatus
            self.__bufferedSurface = self.theme.font.render(
                self.status, 
                self.theme.antialias, 
                self.theme.foreground, 
                self.theme.background,
            )