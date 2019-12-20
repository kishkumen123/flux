import pygame

from screen import Display

running = True
history_output = []
history_input = []
cursor_underscored = 1
editor = 1
poly_dict = []
selection = None
selection_list = []
player = None

rects = []


def add_rect(_rect, _color, _layer):
    global rects
    new_rect = Rect(_rect, _color, _layer)
    rects.append(new_rect)
    sorted(rects, key=lambda rect: rect.layer)


def draw(item=None):
    if item is None:
        global rects
        for rect in rects:
            pygame.draw.rect(Display.fake_display, rect.color, rect.rect)
    else:
        pass


def set_selection(value):
    global selection
    selection = value


def get_selection():
    global selection
    return selection


class Rect:

    def __init__(self, rect, color, layer):
        self.rect = rect
        self.color = color
        self.layer = layer
