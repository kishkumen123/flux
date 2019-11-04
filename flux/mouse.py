import globals
import pygame

from events import events
from layer import Layer
from screen import Display


class Mouse:

    def __init__(self):
        self.rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)
        self.highlight_rect = None

    def get_pos(self):
        return pygame.mouse.get_pos()

    def get_rect(self):
        return self.rect

    def button_pressed(self, button, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            mappings = {"MONE": 0, "MMIDDLE": 1, "MTWO": 2, "WUP": 4, "WDOWN": 5}
            return self.__dict__["MOUSEBUTTON"][mappings[button]]
        return False

    def contains(self, rect):
        self.rect.contains(rect)

    def eval_highlight_color(self, color):
        r, g, b = 0, 0 ,0

        if color[0] + 100 <= 255:
            r = color[0] + 100
        else:
            r = color[0] - 155
        if color[1] + 100 <= 255:
            g = color[1] + 100
        else:
            g = color[1] - 155
        if color[2] + 100 <= 255:
            b = color[2] + 100
        else:
            b = color[2] - 155
        return (r, g, b)

    def update(self):
        if globals.editor:
            if globals.get_selection():
                color = self.eval_highlight_color(globals.get_selection().color)

                #need to have an overloaded draw that just draws everything and is available globally. w.e this is is garbage
                self.highlight_rect = pygame.draw.polygon(Display.fake_display, color, tuple(globals.get_selection().points), 3)

            self.rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)
            if events.button_pressed_once("MONE"):
                found_obj = None
                #this needs to traverse the list from top to bottom layer later
                for obj in globals.poly_dict:
                    if obj.contains(self.rect):
                        found_obj = obj

                globals.set_selection(found_obj)

        else:
            pass


mouse = Mouse()
