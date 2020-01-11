import pygame

from flux.screen import Display
from flux.fonts import fonts


class Renderer:

    def __init__(self):
        self.clamps = {
            "center": (.5, .5),
            "left": (0, .5),
            "right": (1, .5),
            "top": (.5, 0),
            "bottom": (.5, 1),
        }

    def draw_circle(self, position, radius, color, width=0):
        return pygame.draw.circle(Display.fake_display, color, position, radius, width)

    def draw_quad(self, position, size, color, width=0):
        rect = pygame.Rect(position, size)
        pygame.draw.rect(Display.fake_display, color, rect, width)
        return rect

    def draw_poly(self, points, color, width=0):
        return pygame.draw.polygon(Display.fake_display, color, points, width)

    def draw_text(self, text="TEXT", position=None, color=(255, 0, 0), rect=None, clamp=None, padding=(0, 0)):
        surface = fonts["consolas"].render(text, True, color)

        if position:
            Display.fake_display.blit(surface, position)
        elif rect and clamp:
            clamp_position = self.get_text_clamp(rect, clamp, surface, padding)
            if clamp_position is None:
                raise Exception("clamp attribute doesnt exist: %s" % clamp)

            Display.fake_display.blit(surface, clamp_position)
        else:
            raise Exception("rect and clamp must be set or position- rect: %s - clamp: %s - position: %s" % (rect, clamp, position))
        return surface

    def get_text_clamp(self, rect, clamp, surface, padding):
        if clamp is "bottomleft":
            return rect.bottomleft[0] + padding[0], rect.bottomleft[1] - surface.get_height() + padding[1]
        if clamp is "bottomright":
            return rect.bottomright[0] - surface.get_width() + padding[0], rect.bottomright[1] - surface.get_height() + padding[1]
        if clamp is "center":
            return rect.center[0] - surface.get_width()/2 + padding[0], rect.center[1] - surface.get_height()/2 + padding[1]
        if clamp is "midbottom":
            return rect.midbottom[0] - surface.get_width()/2 + padding[0], rect.midbottom[1] - surface.get_height() + padding[1]
        if clamp is "midleft":
            return rect.midleft[0] + padding[0], rect.midleft[1] - surface.get_height()/2 + padding[1]
        if clamp is "midright":
            return rect.midright[0] - surface.get_width() + padding[0], rect.midright[1] - surface.get_height()/2 + padding[1]
        if clamp is "midtop":
            return rect.midtop[0] - surface.get_width()/2 + padding[0], rect.midtop[1] + padding[1]
        if clamp is "topleft":
            return rect.topleft[0] + padding[0], rect.topleft[1] + padding[1]
        if clamp is "topright":
            return rect.topright[0] - surface.get_width() + padding[0], rect.topright[1] + padding[1]

    def text_rect(self, text, color):
        return fonts["consolas"].render(text, True, color).get_rect()

    def circle_rect(self, position, radius, color, width=0):
        return pygame.draw.circle(Display.fake_display, color, position, radius, width)


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