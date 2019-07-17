from chipgr8.module import Module

class RegModule(Module):

    def __init__(self, surface, theme):
        super().__init__(surface, theme)
        self.surface.fill(self.theme.foreground)
        self.surface.fill(self.theme.background, rect=(
            1, 1,
            self.surface.get_width() - 1,
            self.surface.get_height() - 1,
        ))

    def render(self):
        return None