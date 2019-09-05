import pygame
from screen import Display
#from key import Events
from layer import Layer
from events import Events


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
        if Events.key_pressed("TAB") and Events.key_pressed("LSHIFT"):
            cls.y = cls.calc_openess("MAX")
            Layer.set_layer("layer_999")

        if Events.key_pressed("TAB") and not Events.key_pressed("LSHIFT"):
            cls.y = cls.calc_openess("MIN")
            Layer.set_layer("layer_999")

        if Events.key_pressed_once("ESCAPE", "layer_999"):
        #if Events.key_pressed_once("ESCAPE", "layer_999"):
            cls.y = cls.calc_openess("CLOSED")
            print("OK")
            Layer.set_layer("layer_0")
            #State.pop_layer()

        cls.console = pygame.draw.rect(Display.fake_display, (128, 128, 128), (0, 0, Display.x, cls.y))
