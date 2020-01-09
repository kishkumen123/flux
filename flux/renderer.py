import pygame
from screen import Display


class Renderer:
    def __init__(self):
        #self.fonts = {"consolas": pygame.font.SysFont('Consolas', 22)}
        #self.font = pygame.font.SysFont('Consolas', 22)
        pass

    def draw_quad(self, position, size, color):
        rect = pygame.Rect(position, size)
        pygame.draw.rect(Display.fake_display, color, rect)

    #def draw_text(self, text, position, color):
        #_font = self.fonts[font]
        #surface = self.font.render(text, True, color)
        #Display.fake_display.blit(surface, position)


#class Renderer:
#    def __init__(self):
#        self.render_list = []
#
#    def add_layer(self, layer):
#        self.render_list.append(layer)


class RenderLayer:
    def __init__(self, name, z):
        self.name = name
        self.z = z
        self.groups = []

    def add_group(self, group):
        self.groups.append(group)


class Group:
    def __init__(self, z, *items):
        self.z = z
        if items:
            self.items = items
        else:
            self.items = []

    def add_item(self, item):
        self.items.append(item)


renderer = Renderer()