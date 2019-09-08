import pygame
import string

from layer import Layer


class Events:

    def __init__(self):
        self.keys_pressed = []
        self.mouse_pressed = []
        self.events_triggered = []

        self.MONE = 1
        self.MMIDDLE = 2
        self.MTWO = 3
        self.TEXT_INPUT_EVENT = pygame.USEREVENT + 1

        self.assign_keys()

    def assign_keys(self):
        for name in dir(pygame):
            if "K_" in name:
                new_name = name.replace("K_", "")
                self.__dict__[new_name] = pygame.__dict__[name]
            else:
                constant = pygame.__dict__[name]
                if type(constant) == int:
                    self.__dict__[name] = pygame.__dict__[name]

    def handle_text_input_event(self, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            value = self.__dict__.get("TEXT_INPUT_EVENT")
            for event in self.events_triggered:
                if event.type == value:
                    return event.key

        return None

    # capital letters are not working
    def key_pressed(self, key, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            value = self.__dict__.get(key)
            return value in self.keys_pressed

    def key_pressed_once(self, key, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            value = self.__dict__.get(key)
            if value in self.keys_pressed:
                self.keys_pressed.remove(value)
                return True
        return False

    def button_pressed(self, button):
        value = self.__dict__.get(button)
        return value in self.mouse_pressed

    def event_triggered(self, event_name):
        value = self.__dict__.get(event_name)
        for event in self.events_triggered:
            if value == event.type:
                return True

        return False

    def register_buttons_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pressed.append(event.button)
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_pressed.remove(event.button)

    def register_keys_pressed(self, event):
        if event.type == pygame.KEYDOWN:
            self.keys_pressed.append(event.key)
        if event.type == pygame.KEYUP and event.key in self.keys_pressed:
            self.keys_pressed.remove(event.key)

    def register_text_input_event(self, event):
        if event.type == pygame.KEYDOWN:
            if str(event.unicode) in (string.digits + string.ascii_letters + " "):
                text_input_event = pygame.event.Event(self.TEXT_INPUT_EVENT, {"key": str(event.unicode)})
                pygame.event.post(text_input_event)

    def update(self):
        self.events_triggered = pygame.event.get()

        for event in self.events_triggered:
            self.register_buttons_pressed(event)
            self.register_keys_pressed(event)
            self.register_text_input_event(event)


events = Events()
