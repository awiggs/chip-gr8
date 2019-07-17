class Module(object):

    def __init__(self, surface, theme):
        (x, y) = surface.get_offset()
        self.surface = surface
        self.theme   = theme
        self.bounds  = (x, y, surface.get_width(), surface.get_height())
    
    def render(self):
        return self.bounds

    def update(self, vm, events, ignore=[]):
        pass