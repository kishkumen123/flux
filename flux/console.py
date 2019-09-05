import pygame
from screen import Display
from layer import Layer
from events import events


class Console:
    console = pygame.draw.rect(Display.fake_display, (128, 128, 128), (0, 0, 100, 0))
    current_opennes = 0
    max_open = 0.4
    min_open = 0.1

    openess_dict = {"CLOSED": 0, "MIN": 0.1, "MAX": 0.4}
    open_type = "CLOSED"
    y = 0

    layer = "layer_999"

    @classmethod
    def calc_openess(cls, type):
        cls.open_type = type
        ratio = cls.openess_dict[cls.open_type]
        return Display.y * ratio

    @classmethod
    def update(cls):
        if events.key_pressed("TAB", "layer_all") and events.key_pressed("LSHIFT", "layer_all"):
            cls.y = cls.calc_openess("MAX")
            Layer.set_layer("layer_999")

        if events.key_pressed("TAB", "layer_all") and not events.key_pressed("LSHIFT", "layer_all"):
            cls.y = cls.calc_openess("MIN")
            Layer.set_layer("layer_999")

        if events.key_pressed_once("ESCAPE", "layer_999"):
            cls.y = cls.calc_openess("CLOSED")
            Layer.pop_layer()

        cls.console = pygame.draw.rect(Display.fake_display, (128, 128, 128), (0, 0, Display.x, cls.y))
