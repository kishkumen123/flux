import pygame

from flux import _globals
from collections import OrderedDict
from flux.display import display
from flux.fonts import fonts
from flux.utils import load_image
from flux.events import events


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group, layer, image, x, y, name=None):
        if name:
            self.name = name
        else:
            self.name = image.split(".")[0]
        self.image, self.rect = load_image(image)
        self.rect.x = x
        self.rect.y = y
        self._layer = layer
        pygame.sprite.Sprite.__init__(self, group)
        self.offset_calced = False
        self.offset = (0, 0)
        self.render = False

    def __repr__(self):
        return "<Sprite %s>" % self.name

    def update(self, mouse):
        if events.button_pressed("MONE", "layer_all"):
            if _globals.sprite_selection is not None:
                if _globals.sprite_selection == self:
                    if mouse.get_rect().colliderect(self.rect):
                        if not self.offset_calced:
                            self.offset = (mouse.get_pos()[0] - self.rect.x, mouse.get_pos()[1] - self.rect.y)
                            self.offset_calced = True
                        if self.offset_calced:
                            self.rect.x = mouse.get_pos()[0] - self.offset[0]
                            self.rect.y = mouse.get_pos()[1] - self.offset[1]
            else:
                for sprite in _globals.sprite_selection_list:
                    if sprite == self:
                        if not self.offset_calced:
                            self.offset = (mouse.get_pos()[0] - self.rect.x, mouse.get_pos()[1] - self.rect.y)
                            self.offset_calced = True
                        if self.offset_calced:
                            self.rect.x = mouse.get_pos()[0] - self.offset[0]
                            self.rect.y = mouse.get_pos()[1] - self.offset[1]
        else:
            self.offset_calced = False

    #    if events.key_pressed("a", "layer_all"):
    #        self.rect.x -= 1
    #    if events.key_pressed("d", "layer_all"):
    #        self.rect.x += 1
    #    if events.key_pressed("w", "layer_all"):
    #        self.rect.y -= 1
    #    if events.key_pressed("s", "layer_all"):
    #        self.rect.y += 1




class Renderer:
    
    def __init__(self):
        self.sprite_group_dict = {}

    def create_sprite_group(self, name):
        self.sprite_group_dict[name] = pygame.sprite.LayeredUpdates()
        return self.sprite_group_dict[name]

    def create_sprite(self, group, layer, image, x, y):
        if isinstance(group, str):
            return Sprite(self.sprite_group_dict[group], layer, image, x, y)
        if isinstance(group, pygame.sprite.LayeredUpdates):
            return Sprite(group, layer, image, x, y)
    
    def update_sprite_groups(self, mouse, exclude=None):
        for group in self.sprite_group_dict.values():
            if exclude is not None:
                if key not in exclude:
                    group.update(mouse)
            else:
                group.update(mouse)

    def draw_sprite_groups(self, screen, exclude=None):
        for key, group in self.sprite_group_dict.items():
            if exclude is not None:
                if key not in exclude:
                    group.draw(screen)
            else:
                group.draw(screen)

    def get_group(self, name):
        return self.sprite_group_dict[name]




    def draw_circle(self, position, radius, color, width=0):
        return pygame.draw.circle(display.display, color, position, radius, width)

    def draw_quad(self, position, size, color, width=0):
        rect = pygame.Rect(position, size)
        pygame.draw.rect(display.display, color, rect, width)
        return rect

    def draw_poly(self, points, color, width=0):
        return pygame.draw.polygon(display.display, color, points, width)

    def draw_text(self, text="TEXT", position=None, color=(255, 0, 0), rect=None, clamp=None, padding=(0, 0)):
        surface = fonts["consolas"].render(text, True, color)

        if position:
            display.display.blit(surface, position)
        elif rect and clamp:
            clamp_position = self.get_text_clamp(rect, clamp, surface, padding)
            if clamp_position is None:
                raise Exception("clamp attribute doesnt exist: %s" % clamp)

            display.display.blit(surface, clamp_position)
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
        return pygame.draw.circle(display.display, color, position, radius, width)

    def draw(self, _type, data):
        if _type is "text":
            self.draw_text(*data)
        if _type is "quad":
            self.draw_quad(*data)
        if _type is "circle":
            self.draw_circle(*data)


class Renderable:

    def __init__(self, _name, _type, _data):
        self._type = _type
        self._data = _data
        self._name = _name

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    def update(self, _data):
        self._data = _data


class RenderGroup:
    def __init__(self):
        self.group = OrderedDict()
        self.size = len(self.group)

    def add(self, name, _type, data):
        renderable = Renderable(name, _type, data)
        self.group[name] = renderable
        self.size = len(self.group)

    def get_group(self):
        return self.group

    def get_keys(self):
        return self.group.keys()

    def get(self, key):
        return self.group[key]

    def values(self):
        return self.group.values()

    def update(self, name, data):
        self.group[name].update(data)


class RenderLayer:
    def __init__(self):
        self.layer = OrderedDict()
        self.length = len(self.layer)

    def add_group(self, _layer, _group_name, _group):
        exists = self.layer.get(_layer)
        if exists is None:
            while exists is None:
                self.layer["layer_" + str(self.length)] = OrderedDict()
                self.length += 1
                exists = self.layer.get(_layer)

        self.layer[_layer][_group_name] = _group

    def items(self):
        return self.layer.items()

    def keys(self):
        return self.layer.keys()

    def values(self):
        return self.layer.values()

    def update(self, _layer, _group_name, group_element, _data):
        self.layer[_layer][_group_name].update(group_element, _data)

render_layer = RenderLayer()

renderer = Renderer()

