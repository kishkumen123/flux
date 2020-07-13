import pygame
import string

from flux.layer import layer
from flux import _globals


class Events:

    def __init__(self):
        self.keys = {name:pygame.__dict__[name] for name in dir(pygame) if "K_" in name}
        self.keys_held = []
        self.keys_released = set()
        self.keys_pressed_once = set()

    def key_held(self, key_name, _layer="layer_0"):
        if _layer == layer.get_layer() or _layer == "layer_all":
            key = self.keys.get(key_name)
            return key in self.keys_held
        return False

    def key_pressed(self, key_name, _layer="layer_0"):
        if _layer == layer.get_layer() or _layer == "layer_all":
            if self.key_held(key_name):
                key = self.keys.get(key_name)
                return key in self.keys_pressed_once
        return False

    def key_released(self, key_name, _layer="layer_0"):
        if _layer == layer.get_layer() or _layer == "layer_all":
            key = self.keys.get(key_name)
            return key in self.keys_released
        return False

    def update(self):
        self.keys_released = set()
        self.keys_pressed_once = set()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _globals.running = False

            if event.type == pygame.KEYDOWN:
                self.keys_held.append(event.key)
                self.keys_pressed_once.add(event.key)
            if event.type == pygame.KEYUP:
                self.keys_held.remove(event.key)
                self.keys_released.add(event.key)


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
