import pygame

from flux import _globals
from flux.events import events
from flux.layer import layer
from flux.screen import Display
from flux.renderer import renderer


class Mouse:

    def __init__(self):
        self.rect = renderer.circle_rect(pygame.mouse.get_pos(), 5, (250, 0, 0, 0))
        self.highlight_rect = None
        self.calced = False
        self.point_at_click = None
        self.move_offset = None
        self.focus = None
        self.focus_index = None

    def get_pos(self):
        return pygame.mouse.get_pos()

    def get_rect(self):
        return self.rect

    def button_pressed(self, button, _layer="layer_0"):
        if _layer == layer.get_layer() or _layer == "layer_all":
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

    def get_starting_point(self):
        if not events.button_pressed("MTWO"):
            self.calced = False
        if not self.calced:
            self.calced = True
            return pygame.mouse.get_pos()

    def move_point(self, obj):
        for i, point in enumerate(obj.points):
            if self.rect.collidepoint(point[0], point[1]):
                self.focus = obj
                self.focus_index = i

    def move_rect(self, obj):
        if obj.move_offset is not None:
            for i, _ in enumerate(obj.points):
                obj.points[i] = (self.get_pos()[0] + obj.move_offset[i][0], self.get_pos()[1] + obj.move_offset[i][1])
        else:
            obj.move_offset = [(obj.points[i][0] - mouse.get_pos()[0], obj.points[i][1] - mouse.get_pos()[1]) for i, _ in enumerate(obj.points)]

    def update(self):
        if _globals.editor:
            self.rect = renderer.draw_circle(pygame.mouse.get_pos(), 5, (250, 0, 0, 0))

            if _globals.selection_list:
                for obj in _globals.selection_list:
                    color = self.eval_highlight_color(obj.color)
                    renderer.draw_poly(tuple(obj.points), color, 3)

            if events.button_pressed_once("MONE"):
                found_obj = None
                #this needs to traverse the list from top to bottom layer later
                for obj in _globals.poly_dict:
                    if obj.contains(self.rect):
                        found_obj = obj

                _globals.set_selection(found_obj)
                if found_obj:
                    if found_obj not in _globals.selection_list:
                        if not events.key_pressed("LSHIFT"):
                            _globals.selection_list = []
                        _globals.selection_list.append(found_obj)
                else:
                    _globals.selection_list = []

            if events.button_pressed_once("MTWO"):
                self.point_at_click = pygame.mouse.get_pos()

            if events.button_pressed("MTWO"):
                self.selection_box = renderer.draw_quad((self.point_at_click[0], self.point_at_click[1]), (pygame.mouse.get_pos()[0] - self.point_at_click[0], pygame.mouse.get_pos()[1] - self.point_at_click[1]), (100, 100, 100), 3)

            if events.button_released("MTWO"):
                self.point_at_click = None
                _globals.selection_list = []
                for obj in _globals.poly_dict:
                    if self.selection_box.colliderect(obj.rect):
                        _globals.selection_list.append(obj)

                if _globals.selection_list:
                    _globals.selection = None

            if events.button_pressed("MONE") and events.key_pressed("LSHIFT"):
                if self.focus is None:
                    for obj in _globals.poly_dict:
                        self.move_point(obj)
                else:
                    self.focus.points[self.focus_index] = self.get_pos()
            else:
                self.focus = None
                self.focus_index = None

            # this for loop should be in the if statement, this is super inefficient
            for obj in _globals.selection_list:
                if events.button_pressed("MONE") and not events.key_pressed("LSHIFT"):
                    self.move_rect(obj)
                else:
                    obj.move_offset = None
        else:
            pass


mouse = Mouse()
