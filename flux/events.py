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
        self.TEXT_INPUT_EVENT_DOWN = pygame.USEREVENT + 1
        self.TEXT_INPUT_EVENT_UP = pygame.USEREVENT + 2

        self.start_ticks = None
        self.first_click = False
        self.second_tick = False
        self.repeat_timer = 0.05
        self.first_stroke_timer = 0.5
        self.last_key_pressed = None

        self.start_ticks_txt = None
        self.first_click_txt = False
        self.second_tick_txt = False
        self.repeat_timer_txt = 0.05
        self.first_stroke_timer_txt = 0.5
        self.last_key_pressed_text = None

        self.valid_text_list = string.digits + string.ascii_letters + string.punctuation + " "

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
            for event in self.events_triggered:
                if event.type == self.TEXT_INPUT_EVENT_DOWN:
                    return event.key
        return None

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

    def handle_text_input_event_repeat(self, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            for event in self.events_triggered:
                if event.type == self.TEXT_INPUT_EVENT_DOWN:
                    last_key_pressed = event.key
                    if self.last_key_pressed_text != last_key_pressed:
                        self.start_ticks_txt = None
                        self.first_click_txt = False
                        self.second_tick_txt = False
                    self.last_key_pressed_text = last_key_pressed
                if event.type == self.TEXT_INPUT_EVENT_UP:
                    if event.key == self.last_key_pressed_text:
                        self.last_key_pressed_text = None

            print(self.last_key_pressed_text)
            if self.last_key_pressed_text is not None:
                if self.start_ticks_txt is None:
                    self.start_ticks_txt = pygame.time.get_ticks()
                elapsed_time = (pygame.time.get_ticks() - self.start_ticks_txt) / 1000
                if self.first_click_txt is False:
                    self.first_click_txt = True
                    return self.last_key_pressed_text
                if elapsed_time > self.first_stroke_timer_txt and self.second_tick_txt is False:
                    self.second_tick_txt = True
                    self.start_ticks_txt = None
                if elapsed_time > self.repeat_timer_txt and self.second_tick_txt:
                    self.start_ticks_txt = None
                    return self.last_key_pressed_text
                #elif self.last_key_pressed_text != event.key:
                    #print(11)
                    #return None
                else:
                    self.start_ticks_txt = None
                    self.first_click_txt = False
                    self.second_tick_txt = False
                    #self.last_key_pressed_text = None
                    return None

    #def handle_text_input_event_repeat(self, layer="layer_0"):
    #    if layer == Layer.get_layer() or layer == "layer_all":
    #        for event in self.events_triggered:
    #            if event.type == self.TEXT_INPUT_EVENT_DOWN:
    #                last_key_pressed = event.key
    #                if self.last_key_pressed_text != last_key_pressed:
    #                    self.start_ticks_txt = None
    #                    self.first_click_txt = False
    #                    self.second_tick_txt = False
    #                self.last_key_pressed_text = last_key_pressed
    #                if self.start_ticks_txt is None:
    #                    self.start_ticks_txt = pygame.time.get_ticks()
    #                elapsed_time = (pygame.time.get_ticks() - self.start_ticks_txt) / 1000
    #                if self.first_click_txt is False:
    #                    self.first_click_txt = True
    #                    return event.key
    #                if elapsed_time > self.first_stroke_timer_txt and self.second_tick_txt is False:
    #                    self.second_tick_txt = True
    #                    self.start_ticks_txt = None
    #                if elapsed_time > self.repeat_timer_txt and self.second_tick_txt:
    #                    self.start_ticks_txt = None
    #                    return event.key
    #            #elif self.last_key_pressed_text != event.key:
    #            #print(11)
    #            #return None
    #            else:
    #                print(11)
    #                self.start_ticks_txt = None
    #                self.first_click_txt = False
    #                self.second_tick_txt = False
    #                self.last_key_pressed_text = None
    #                return None

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
            if str(event.unicode) in self.valid_text_list:
                text_input_event = pygame.event.Event(self.TEXT_INPUT_EVENT_DOWN, {"type": "text_input_down", "key": str(event.unicode)})
                pygame.event.post(text_input_event)
        if event.type == pygame.KEYUP:
            if pygame.key.name(event.key) in self.valid_text_list:
                text_input_event = pygame.event.Event(self.TEXT_INPUT_EVENT_UP, {"type": "text_input_UP", "key": pygame.key.name(event.key)})
                pygame.event.post(text_input_event)

    def update(self):
        self.events_triggered = pygame.event.get()

        for event in self.events_triggered:
            self.register_buttons_pressed(event)
            self.register_keys_pressed(event)
            self.register_text_input_event(event)


events = Events()
