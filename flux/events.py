import pygame

from layer import Layer


class Events:

    def __init__(self):
        self.keys_pressed = []
        self.mouse_pressed = []
        self.MONE = 1
        self.MMIDDLE = 2
        self.MTWO = 3
        self.assign_keys()

    def assign_keys(self):
        for name in dir(pygame):
            if "K_" in name:
                new_name = name.replace("K_", "")
                self.__dict__[new_name] = pygame.__dict__[name]

    def key_pressed(self, key, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            value = self.__dict__[key]
            return value in self.keys_pressed

    def key_pressed_once(self, key, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            value = self.__dict__[key]
            if value in self.keys_pressed:
                self.keys_pressed.remove(value)
                return True
        return False

    def button_pressed(self, button):
        value = self.__dict__[button]
        return value in self.mouse_pressed

    def register_keys_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pressed.append(event.button)
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_pressed.remove(event.button)

        if event.type == pygame.KEYDOWN:
            self.keys_pressed.append(event.key)
        if event.type == pygame.KEYUP and event.key in self.keys_pressed:
            self.keys_pressed.remove(event.key)

    def update(self):
        for event in pygame.event.get():
            self.register_keys_pressed(event)


events = Events()
