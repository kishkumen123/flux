import pygame

from collections import OrderedDict
from flux.screen import Display
from flux.fonts import fonts


class Renderer:

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

    def draw(self, _type, data):
        if _type is "text":
            self.draw_text(*data)
        if _type is "quad":
            self.draw_quad(*data)
        if _type is "circle":
            self.draw_circle(*data)


class RenderGroup:
    def __init__(self):
        self.group = OrderedDict()
        self.size = len(self.group)

    def add(self, name, _type, data):
        self.group[name] = {"type": _type, "data": data}
        self.size = len(self.group)

    def update(self, name, data):
        self.group[name]["data"] = data

    def get_group(self):
        return self.group

    def get_keys(self):
        return self.group.keys()

    def get(self, key):
        return self.group[key]

    def values(self):
        return self.group.values()


class RenderLayer:
    def __init__(self):
        self.layer = OrderedDict()
        self.length = len(self.layer)

    def create_layer(self):
        layer_name = "layer_" + str(self.length)
        self.layer[layer_name] = OrderedDict()
        self.length = len(self.layer)

    def add_group(self, _layer, _group_name, _group):
        #exists = self.layer.get(_layer)
        #if not exists:
            #while not exists:
                #layer_name = "layer_" + str(self.length)
                #self.layer[layer_name] = OrderedDict()
                #self.length = len(self.layer)
                #exists = self.layer.get(_layer)

        self.layer[_layer][_group_name] = _group

    def items(self):
        return self.layer.items()

    def keys(self):
        return self.layer.keys()

    def values(self):
        return self.layer.values()

    def update(self, _layer, _group_name, group_element, _data):
        self.layer[_layer][_group_name].update(group_element, _data)


#group = RenderGroup()
#group.add(name, type, data)

#class Renderer:
#    def __init__(self):
#        self.render_list = []
#
#    def add_layer(self, layer):
#        self.render_list.append(layer)



#class Group:
#    def __init__(self, z, *items):
#        self.z = z
#        if items:
#            self.items = items
#        else:
#            self.items = []
#
#    def add_item(self, item):
#        self.items.append(item)


renderer = Renderer()