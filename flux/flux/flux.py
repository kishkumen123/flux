# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

from events import Events
from key import Key
from screen import Display
from rect import Poly


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
        self.mouse_rect_color = (250, 0, 0)
        self._mouse_rect = pygame.Rect((0,0,0,0))
        self.poly = None
        self.keys_pressed = None
        self.events = None

    def init(self):
        pygame.init()
        self.keys_pressed = pygame.key.get_pressed()
        self.events = pygame.event.get()

    def init_display(self, resolution):
        self.display = Display(resolution)

        return self.display

    def set_fps(self, fps):
        self.fps = fps

    def get_fps(self):
        return self.clock.get_fps()

    def update_delta_time(self):
        self._delta_time = self.clock.tick(self.fps)
        self._elapsed_time += self._delta_time / 1000.0

    def mouse_radius(self):
        rect = pygame.draw.circle(self.display.fake_display, (250, 0, 0), self.mouse_pos, 5, 0)
        if rect.collidepoint(200, 200):
            print(True)
        else:
            print(False)

    @property
    def mouse_pos(self):
        return pygame.mouse.get_pos()

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

    @property
    def mouse_rect(self):
        return self._mouse_rect

    def key_pressed(self, key):
        key_value = Key.__dict__[key]
        return self.keys_pressed[key_value]

    def event_active(self, event):
        event_value = Events.__dict__[event]
        event_types = [event.type for event in self.events]
        return event_value in event_types

    def update(self):
        self.update_delta_time()
        self._mouse_rect = pygame.draw.circle(self.display.fake_display, (250, 0, 0), self.mouse_pos, 5, 0)
        self.keys_pressed = pygame.key.get_pressed()
        self.events = pygame.event.get()

    def kill(self):
        self.running = False
