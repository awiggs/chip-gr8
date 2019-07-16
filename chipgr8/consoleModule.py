from chipgr8.pygame_textinput import TextInput
import pygame

class ConsoleModule:
    def __init__(self, screen):
        self.ti = TextInput(font_size=16)
        self.screen = screen

    def render(self):
        self.screen.fill((255,255,255))
        self.screen.blit(self.ti.get_surface(), (10, 10))
        pygame.display.update()

    def update(self, events, ignores=[]):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print(self.ti.get_text())
                self.ti.clear_text()
                break
        self.ti.update(events, ignores=ignores)
