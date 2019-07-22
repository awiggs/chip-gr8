from chipgr8.module import Module

class RegModule(Module):

    __diff   = None
    __regs   = []

    def __init__(self, surface, theme):
        super().__init__(surface, theme)
        self.surface.fill(self.theme.foreground)
        self.surface.fill(self.theme.background, rect=(
            1, 1,
            self.surface.get_width() - 1,
            self.surface.get_height() - 1,
        ))

    def render(self):
        return self.__diff

    def update(self, vm, events):
        regs = [
            'V0 = 0x{:02X}    '.format(vm.VM.V[0x0]) + ' VE = 0x{:02X}'.format(vm.VM.V[0xE]),
            'V1 = 0x{:02X}    '.format(vm.VM.V[0x1]) + ' VF = 0x{:02X}'.format(vm.VM.V[0xF]),
            'V2 = 0x{:02X}    '.format(vm.VM.V[0x2]),
            'V3 = 0x{:02X}    '.format(vm.VM.V[0x3]) + ' DT = 0x{:02X}'.format(vm.VM.DT),
            'V4 = 0x{:02X}    '.format(vm.VM.V[0x4]) + ' ST = 0x{:02X}'.format(vm.VM.ST),
            'V5 = 0x{:02X}    '.format(vm.VM.V[0x5]),
            'V6 = 0x{:02X}    '.format(vm.VM.V[0x6]) + '  K = 0x{:04X}'.format(vm.VM.K),
            'V7 = 0x{:02X}    '.format(vm.VM.V[0x7]) + '  W = 0x{:02X}'.format(vm.VM.W),
            'V8 = 0x{:02X}    '.format(vm.VM.V[0x8]),
            'V9 = 0x{:02X}    '.format(vm.VM.V[0x9]) + '  I = 0x{:03X}'.format(vm.VM.I),
            'VA = 0x{:02X}    '.format(vm.VM.V[0xA]) + ' PC = 0x{:03X}'.format(vm.VM.PC),
            'VB = 0x{:02X}    '.format(vm.VM.V[0xB]) + ' SP = 0x{:03X}'.format(vm.VM.SP),
            'VC = 0x{:02X}    '.format(vm.VM.V[0xC]),
            'VD = 0x{:02X}    '.format(vm.VM.V[0xD]) + 'CLK = 0x{:06X}'.format(vm.VM.clock),
        ]
        if regs != self.__regs:
            lineHeight = self.theme.font.get_height()
            for (i, reg) in enumerate(regs):
                self.surface.blit(
                    self.theme.font.render(
                        reg,
                        self.theme.antialias,
                        self.theme.foreground,
                        self.theme.background,
                    ),
                    (4, 4 + (i * lineHeight)),
                )
            self.__reg = reg
            self.__diff = self.bounds
