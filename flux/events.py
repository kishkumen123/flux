import pygame
import string
import sys

from flux.layer import layer
from flux import _globals


class Events:

    def __init__(self):
        self.keys = {name:pygame.__dict__[name] for name in dir(pygame) if "K_" in name}
        self.keys_held = set()
        self.keys_pressed = []
        self.keys_released = set()
        self.text_pressed = []
        self.buttons_held = set()
        self.buttons_pressed = set()
        self.buttons_released = set()

        self.mouse_buttons = {"M_ONE": 1, "M_TWO": 3, "M_MIDDLE": 2, "M_WHEELDOWN": 4, "M_WHEELUP": 5}
        self.text_list = string.digits + string.ascii_letters + string.punctuation + " space"
        self.text_list = self.text_list.replace("`", "")
        self.text_list = self.text_list.replace("~", "")

        self.text_delay_first = 0.4
        self.text_delay_second = 0.04

        self.key_ticks = pygame.time.get_ticks()
        self.key_ticks_started = False
        self.key_first_done = False
        self.last_key = ""

        self.text_ticks = pygame.time.get_ticks()
        self.ticks_started = False
        self.first_done = False
        self.last_text = ""


    def mouse_held(self, button_name, layer_name="layer_0"):
        if layer.current_layer_is(layer_name):
            button = self.mouse_buttons[button_name]
            return button in self.buttons_held
        return False

    def mouse_pressed(self, button_name, layer_name="layer_0"):
        if layer.current_layer_is(layer_name):
            button = self.mouse_buttons[button_name]
            if button in self.buttons_pressed:
                self.buttons_pressed.remove(button)
                return True
        return False

    def mouse_released(self, button_name, layer_name="layer_0"):
        if layer.current_layer_is(layer_name):
            button = self.mouse_buttons[button_name]
            return button in self.buttons_released
        return False

    def key_repeat(self, key_name,  _layer="layer_0"):
        if _layer == layer.get_layer() or _layer == "layer_all":
            key = self.keys.get(key_name)
            if len(self.keys_pressed):
                temp = self.keys_pressed[-1]
                if temp != self.last_key:
                    self.ticks_started = False
                    self.first_done = False
                self.last_key = temp

            if not self.key_ticks_started:
                self.key_ticks_started = True
                self.key_ticks = pygame.time.get_ticks()
                return self.last_key
            elif ((pygame.time.get_ticks() - self.key_ticks)/1000) > self.text_delay_first and not self.key_first_done:
                self.key_ticks = pygame.time.get_ticks()
                self.key_first_done = True
                return self.last_key
            elif ((pygame.time.get_ticks() - self.key_ticks)/1000) > self.text_delay_second and self.key_first_done:
                self.key_ticks = pygame.time.get_ticks()
                return self.last_key
        return None

    def key_held(self, key_name, layer_name="layer_0"):
        if layer.current_layer_is(layer_name):
            key = self.keys.get(key_name)
            return key in self.keys_held
        return False

    def key_pressed(self, key_name, layer_name="layer_0"):
        if layer.current_layer_is(layer_name):
            key = self.keys.get(key_name)
            if key in self.keys_pressed:
                self.keys_pressed.remove(key)
                return True
        return False

    def key_released(self, key_name, layer_name="layer_0"):
        if layer.current_layer_is(layer_name):
            key = self.keys.get(key_name)
            return key in self.keys_released
        return False

    def text_input(self, _layer="layer_0"):
        if _layer == layer.get_layer() or _layer == "layer_all":
            if len(self.text_pressed):
                text = self.text_pressed.pop()
                if text in self.text_list and text != "":
                    return text
        return None

    def text_input_repeat(self, _layer="layer_0"):
        if _layer == layer.get_layer() or _layer == "layer_all":
            if len(self.text_pressed):
                temp = self.text_pressed[-1]
                if temp != self.last_text:
                    self.ticks_started = False
                    self.first_done = False
                self.last_text = temp

            if self.last_text in self.text_list and self.last_text != "":
                if not self.ticks_started:
                    self.ticks_started = True
                    self.text_ticks = pygame.time.get_ticks()
                    return self.last_text
                elif ((pygame.time.get_ticks() - self.text_ticks)/1000) > self.text_delay_first and not self.first_done:
                    self.text_ticks = pygame.time.get_ticks()
                    self.first_done = True
                    return self.last_text
                elif ((pygame.time.get_ticks() - self.text_ticks)/1000) > self.text_delay_second and self.first_done:
                    self.text_ticks = pygame.time.get_ticks()
                    return self.last_text
        return None

    def update(self):
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.buttons_pressed.clear()
        self.buttons_released.clear()
        self.text_pressed.clear()

        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        _globals.running = False
        #        pygame.quit()
        #        sys.exit()

        #    # maybe this is callable from anywhere?
        #    # handle_text_event(event)
        #    # handle_key_event(event)
        #    # handle_mouse_event(event)

        #    # for handle_ in _global.events:
        #    #     handle_(event)

        #    if event.type == pygame.MOUSEBUTTONDOWN:
        #        self.buttons_held.add(event.button)
        #        self.buttons_pressed.add(event.button)
        #    if event.type == pygame.MOUSEBUTTONUP:
        #        self.buttons_held.remove(event.button)
        #        self.buttons_released.add(event.button)

        #    if event.type == pygame.KEYDOWN:
        #        self.text_pressed.append(event.unicode)
        #        self.keys_held.add(event.key)
        #        self.keys_pressed.append(event.key)
        #    if event.type == pygame.KEYUP:
        #        self.keys_held.remove(event.key)
        #        self.keys_released.add(event.key)
        #        if 1 not in pygame.key.get_pressed():
        #            self.last_text = ""


events = Events()


#init
        #################
        #self.text_list = string.digits + string.ascii_letters + string.punctuation + " space"
        #self.text_list = self.text_list.replace("`", "")
        #self.text_list = self.text_list.replace("~", "")
	#####################################################
        ##self.m_keys = {"M_LEFT": 1, "M_RIGHT": 3, "M_MIDDLE": 2, "M_SCROLLDOWN": 4, "M_SCROLLUP": 5}
        #self.long_repeat_delay = 0.4
        #self.short_repeat_delay = 0.04
        #self.start_ticks = pygame.time.get_ticks()

        ##key press repeat
        #self.first_button_registered = False
        #self.first_delay_finished = False
        #self.repeat_delay = self.long_repeat_delay
        ##text input repeat
        #self.first_button_registered_txt = False
        #self.first_delay_finished_txt = False
        #self.repeat_delay_txt = self.long_repeat_delay

        #self.register_press_once = True
        ####################################################
        #self.keys_pressed = []
        #self.mouse_pressed = []
        #self.mouse_released = None
        #self.mouse_pressed_once = []
        #self.events_triggered = []
        #self.mouse_wheel_down = False
        #self.mouse_wheel_up = False

        #self.MONE = 1
        #self.MMIDDLE = 2
        #self.MTWO = 3
        ##delete
        #self.TEXT_INPUT_EVENT_DOWN = pygame.USEREVENT + 1
        #self.TEXT_INPUT_EVENT_UP = pygame.USEREVENT + 2

        ##delete
        #self.first_click = False
        #self.second_tick = False
        #self.repeat_timer = 0.04
        #self.first_stroke_timer = 0.4
        #self.last_key_pressed = None

        ##delete
        #self.start_ticks_txt = None
        #self.first_click_txt = False
        #self.second_tick_txt = False
        #self.repeat_timer_txt = 0.04
        #self.first_stroke_timer_txt = 0.4
        #self.last_key_pressed_txt = None
        ##delete


    #def assign_keys(self):
    #    for name in dir(pygame):
    #        if "K_" not in name:
    #            # TODO: look at this later and make sure its what you want to do
    #            constant = pygame.__dict__[name]
    #            if type(constant) == int:
    #                self.__dict__[name] = pygame.__dict__[name]

    ## this consumed the event and reeturns the unicode
    #def text_input(self, _layer="layer_0"):
    #    if _layer == layer.get_layer() or _layer == "layer_all":
    #        if len(self.keys_pressed):
    #            key_name = pygame.key.name(self.keys_pressed[-1])
    #            if key_name in self.text_list:
    #                return key_name

    #def text_input_repeat(self, _layer="layer_0"):
    #    if _layer == layer.get_layer() or _layer == "layer_all":
    #        #if self.event:
    #            #if self.event.unicode in self.text_list:
    #        if len(self.keys_pressed):
    #            key_name = pygame.key.name(self.keys_pressed[-1])
    #            if key_name in self.text_list:
    #                elapsed_time = (pygame.time.get_ticks() - self.start_ticks)/1000

    #                if not self.first_button_registered_txt:
    #                    self.first_button_registered_txt = True
    #                    self.start_ticks = pygame.time.get_ticks()
    #                    return key_name

    #                elif elapsed_time > self.repeat_delay_txt and self.first_button_registered_txt:
    #                    if not self.first_delay_finished_txt:
    #                        self.first_delay_finished_txt = True
    #                        self.repeat_delay_txt = self.short_repeat_delay
    #                    self.start_ticks = pygame.time.get_ticks()
    #                    return key_name

    ##TODO: this is responding slow, not sure why
    #def button_pressed_once(self, button, _layer="layer_0"):
    #    if _layer == layer.get_layer() or _layer == "layer_all":
    #        if self.m_event:
    #            if self.m_keys[button] == self.m_event.button:
    #                self.m_event = None
    #                return True

    #    return False

    ##TODO: need to do something about scrollwheel, its set to None immediately
    #def button_pressed(self, button, _layer="layer_0"):
    #    if _layer == layer.get_layer() or _layer == "layer_all":
    #        if self.m_event:
    #            return self.m_keys[button] == self.m_event.button

    #    return False

    ##TODO: havent even looked at this yet
    #def button_released(self, button, _layer="layer_0"):
    #    if _layer == layer.get_layer() or _layer == "layer_all":
    #        value = self.__dict__.get(button)
    #        if value == self.mouse_released:
    #            self.mouse_released = None
    #            return True

    #    return False

    ##TODO: QUIT isnt working cause this isnt being populated anymore. think of a better way to store those events
    #def event_triggered(self, event_name, _layer="layer_0"):
    #    if _layer == layer.get_layer() or _layer == "layer_all":
    #        value = self.__dict__.get(event_name)
    #        for event in self.events_triggered:
    #            if value == event.type:
    #                return True

    #    return False

    #def register_mouse_buttons_pressed(self, event):
    #    if event.type == pygame.MOUSEBUTTONDOWN:
    #        self.mouse_pressed.append(event.button)
    #        self.mouse_pressed_once.append(event.button)
    #        if event.button == 5:
    #            self.mouse_wheel_down = True
    #        if event.button == 4:
    #            self.mouse_wheel_up = True

    #    if event.type == pygame.MOUSEBUTTONUP:
    #        self.mouse_pressed.remove(event.button)
    #        self.mouse_released = event.button
    #        if event.button in self.mouse_pressed_once:
    #            self.mouse_pressed_once.remove(event.button)

    #def flush(self):
    #    self.mouse_released = None


    #def key_pressed(self, key, _layer="layer_0"):
    #    if _layer == layer.get_layer() or _layer == "layer_all":
    #        if self.keys[key] in self.keys_pressed:
    #            return True
    #    return False
    #def key_pressed_once(self, key, _layer="layer_0"):
    #    if _layer == layer.get_layer() or _layer == "layer_all":
    #        if self.keys[key] in self.keys_pressed and self.register_press_once:
    #            self.register_press_once = False
    #            return True
    #    return False
    #def key_released(self, key, _layer="layer_0"):
    #    if _layer == layer.get_layer() or _layer == "layer_all":
    #        if self.keys[key] in self.keys_released and self.register_release_once:
    #            self.keys_released.remove(self.keys[key])
    #            self.register_release_once = False
    #            return True
    #    return False


    #def key_pressed_repeat(self, key, _layer="layer_0"):
    #    if _layer == layer.get_layer() or _layer == "layer_all":
    #        if self.keys[key] in self.keys_pressed:
    #            elapsed_time = (pygame.time.get_ticks() - self.start_ticks)/1000

    #            if not self.first_button_registered:
    #                self.first_button_registered = True
    #                self.start_ticks = pygame.time.get_ticks()
    #                return True

    #            elif elapsed_time > self.repeat_delay and self.first_button_registered:
    #                if not self.first_delay_finished:
    #                    self.first_delay_finished = True
    #                    self.repeat_delay = self.short_repeat_delay
    #                self.start_ticks = pygame.time.get_ticks()
    #                return True


#update
        #self.mouse_wheel_down = False
        #self.mouse_wheel_up = False


                #if event.key in self.keys_pressed_once:
                    #self.keys_pressed_once.remove(event.key)

            # IMPORTANT FIX THAT NEEDS TO BE DONE, FLUSH MOUSE_RELEASED AT SOME POINT (i think this was fixed? not sure)
        #    self.register_mouse_buttons_pressed(event)

        #    #TODO: this probably also needs to change from self.m_event = None to event to capture the up event im pretty sure
        #    if event.type == pygame.MOUSEBUTTONDOWN:
        #        self.m_event = event
        #        #print(event)
        #    if event.type == pygame.MOUSEBUTTONUP:
        #        #print(event)
        #        self.m_event = None
        #
        #    if event.type == pygame.KEYDOWN:
        #        self.keys_pressed.append(event.key)
        #        self.event = event
        #    if event.type == pygame.KEYUP:
        #        self.keys_pressed.remove(event.key)
        #        self.event = None

        #if self.last_event != self.event:
        #    self.first_button_registered = False
        #    self.first_delay_finished = False
        #    self.repeat_delay = self.long_repeat_delay
        #    self.first_button_registered_txt = False
        #    self.first_delay_finished_txt = False
        #    self.repeat_delay_txt = self.long_repeat_delay
        #    self.register_press_once = True
        ##print("keys_pressed: %s" % self.keys_pressed)
        ##print("keys_released: %s" % self.keys_released)

        #self.last_event = self.event
        #print(self.first_button_registered_txt)
