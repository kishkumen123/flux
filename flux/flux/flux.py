# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

from events import events
from mouse import Mouse
from screen import Display
from poly import Poly
from console import Console
from layer import Layer


class Flux:

    def __init__(self, play_time=0, fps=30):
        self.fps = fps
        self.play_time = play_time
        self.clock = pygame.time.Clock()
        self._delta_time = 0
        self.miliseconds = 0
        self.running = True
        self.display = None
        self._elapsed_time = 0
        self.poly = None

    def init(self):
        pygame.init()

    def init_display(self, resolution):
        self.display = Display
        self.display.init(resolution)

        return self.display

    def set_fps(self, fps):
        self.fps = fps

    def get_fps(self):
        return self.clock.get_fps()

    def update_delta_time(self):
        self._delta_time = self.clock.tick(self.fps)
        self._elapsed_time += self._delta_time / 1000.0

    @property
    def delta_time(self):
        return self._delta_time

    @property
    def elapsed_time(self):
        return self._elapsed_time

    def create_poly(self, color, points, surface=None, width=0):
        if surface is None:
            surface = self.display.fake_display
        return Poly(color, points, surface, width)

    def create_surface(self, size, color):
        surface = pygame.Surface(size).convert()
        surface.fill(color)
        return surface

    def quit(self):
        print("quit")
        pygame.quit()

    def is_running(self):
        return self.running

    def key_pressed(self, key, layer="layer_0"):
        return events.key_pressed(key, layer)

    def key_pressed_once(self, key, layer="layer_0"):
        return events.key_pressed_once(key, layer)

    #needs to be reimplemented
    #def event_active(self, event, layer=None):
        #return events.event_active(event, layer)

    def mousebutton_pressed(self, button):
        return Mouse.button_pressed(button)

    def update(self):
        self.update_delta_time()
        Console.update()
        print(Layer.get_layer())

        Mouse.update()
        events.update()

    def kill(self):
        self.running = False
