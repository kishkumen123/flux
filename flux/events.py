import pygame
import string

from layer import Layer


class Events:

    def __init__(self):
        self.keys_pressed = []
        self.mouse_pressed = []
        self.mouse_pressed_once = []
        self.events_triggered = []
        self.mouse_wheel_down = False
        self.mouse_wheel_up = False

        self.MONE = 1
        self.MMIDDLE = 2
        self.MTWO = 3
        self.TEXT_INPUT_EVENT_DOWN = pygame.USEREVENT + 1
        self.TEXT_INPUT_EVENT_UP = pygame.USEREVENT + 2

        self.start_ticks = None
        self.first_click = False
        self.second_tick = False
        self.repeat_timer = 0.04
        self.first_stroke_timer = 0.4
        self.last_key_pressed = None

        self.start_ticks_txt = None
        self.first_click_txt = False
        self.second_tick_txt = False
        self.repeat_timer_txt = 0.04
        self.first_stroke_timer_txt = 0.4
        self.last_key_pressed_txt = None

        self.valid_text_list = string.digits + string.ascii_letters + string.punctuation + " space"
        self.valid_text_list = self.valid_text_list.replace("`", "")
        self.valid_text_list = self.valid_text_list.replace("~", "")

        self.assign_keys()

    def key_converter(self, key):
        actual_key = chr(key)
        mappings = {"1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(", "0": ")", "-": "_", "=": "+", "[": "{", "]": "}", ";": ":", "'": "\"", ",": "<", ".": ">", "/": "?", "\\": "|"}

        if actual_key in mappings.keys():
            new_key = mappings[actual_key]
        elif 87 <= key <= 122:
            binary = bin(key)
            new_binary = binary[:3] + "0" + binary[4:]
            new_ascii = int(new_binary, 2)
            new_key = chr(new_ascii)
        else:
            raise("KEY MAPPINGS ARE MEST UP ON KEY %s PLEASE LOOK INTO IT RIGHT FUCKING NOW" % key)
        return new_key

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
            for event in self.events_triggered:
                if event.type == self.TEXT_INPUT_EVENT_DOWN:
                    return event.key
        return None

    def handle_text_input_event_repeat(self, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            for event in self.events_triggered:
                if event.type == self.TEXT_INPUT_EVENT_DOWN:
                    last_key_pressed = event.key
                    if self.last_key_pressed_txt != last_key_pressed:
                        self.start_ticks_txt = None
                        self.first_click_txt = False
                        self.second_tick_txt = False
                    self.last_key_pressed_txt = last_key_pressed
                if event.type == self.TEXT_INPUT_EVENT_UP:
                    if event.key == self.last_key_pressed_txt:
                        self.last_key_pressed_txt = None

            if self.last_key_pressed_txt is not None:
                if self.start_ticks_txt is None:
                    self.start_ticks_txt = pygame.time.get_ticks()
                elapsed_time = (pygame.time.get_ticks() - self.start_ticks_txt) / 1000
                if self.first_click_txt is False:
                    self.first_click_txt = True
                    return self.last_key_pressed_txt
                elif elapsed_time > self.first_stroke_timer_txt and self.second_tick_txt is False:
                    self.second_tick_txt = True
                    self.start_ticks_txt = None
                elif elapsed_time > self.repeat_timer_txt and self.second_tick_txt:
                    self.start_ticks_txt = None
                    return self.last_key_pressed_txt
            else:
                self.start_ticks_txt = None
                self.first_click_txt = False
                self.second_tick_txt = False
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

    def key_pressed_repeat(self, key, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            value = self.__dict__.get(key)
            last_key_pressed = self.keys_pressed[-1] if len(self.keys_pressed) else None
            if value == last_key_pressed:
                if self.last_key_pressed != last_key_pressed:
                    self.start_ticks = None
                    self.first_click = False
                    self.second_tick = False
                self.last_key_pressed = last_key_pressed
                if self.start_ticks is None:
                    self.start_ticks = pygame.time.get_ticks()
                elapsed_time = (pygame.time.get_ticks() - self.start_ticks)/1000
                if self.first_click is False:
                    self.first_click = True
                    return True
                if elapsed_time > self.first_stroke_timer and self.second_tick is False:
                    self.second_tick = True
                    self.start_ticks = None
                if elapsed_time > self.repeat_timer and self.second_tick:
                    self.start_ticks = None
                    return True
            elif self.last_key_pressed != value:
                return False
            else:
                self.start_ticks = None
                self.first_click = False
                self.second_tick = False
                self.last_key_pressed = None
                return False

    def button_pressed_once(self, button, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            value = self.__dict__.get(button)
            if value in self.mouse_pressed_once:
                self.mouse_pressed_once.remove(value)
                return value

        return False

    def button_pressed(self, button, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            value = self.__dict__.get(button)
            return value in self.mouse_pressed

        return False

    def event_triggered(self, event_name, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            value = self.__dict__.get(event_name)
            for event in self.events_triggered:
                if value == event.type:
                    return True

        return False

    def register_mouse_buttons_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pressed.append(event.button)
            self.mouse_pressed_once.append(event.button)
            if event.button == 5:
                self.mouse_wheel_down = True
            if event.button == 4:
                self.mouse_wheel_up = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_pressed.remove(event.button)
            if event.button in self.mouse_pressed_once:
                self.mouse_pressed_once.remove(event.button)

    def register_keys_pressed(self, event):
        if event.type == pygame.KEYDOWN:
            self.keys_pressed.append(event.key)
        if event.type == pygame.KEYUP and event.key in self.keys_pressed:
            self.keys_pressed.remove(event.key)

    def register_text_input_event(self, event):
        if event.type == pygame.KEYDOWN:
            if str(event.unicode) in self.valid_text_list:
                text_input_event = pygame.event.Event(self.TEXT_INPUT_EVENT_DOWN, {"type": "text_input_down", "key": str(event.unicode)})
                pygame.event.post(text_input_event)
        if event.type == pygame.KEYUP:
            if pygame.key.name(event.key) in self.valid_text_list:
                if pygame.key.name(event.key) == "space":
                    key = " "
                else:
                    key = pygame.key.name(event.key)

                if event.mod == 1 or event.mod == 2:
                    key = self.key_converter(event.key)
                text_input_event = pygame.event.Event(self.TEXT_INPUT_EVENT_UP, {"type": "text_input_up", "key": key})
                pygame.event.post(text_input_event)

    def update(self):
        self.events_triggered = pygame.event.get()

        self.mouse_wheel_down = False
        self.mouse_wheel_up = False

        for event in self.events_triggered:
            self.register_mouse_buttons_pressed(event)
            self.register_keys_pressed(event)
            self.register_text_input_event(event)


events = Events()
