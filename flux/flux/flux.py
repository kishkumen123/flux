# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

from events import Events
from key import Key
from screen import Display


class Flux:

    def __init__(self, play_time=0, fps=30):
        self.fps = fps
        self.play_time = play_time
        self.clock = pygame.time.Clock()
        self._delta_time = 0
        self.miliseconds = 0
        self.running = True
        self.display = None
        self.events = Events()
        self.key = Key()
        self._elapsed_time = 0

    def init(self):
        pygame.init()

    def init_display(self, resolution):
        return Display(resolution)

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

    def create_surface(self, size, color):
        surface = pygame.Surface(size).convert()
        surface.fill(color)
        return surface

    def quit(self):
        print("quit")
        pygame.quit()

    def is_running(self):
        self.update_delta_time()
        return self.running

    def kill(self):
        self.running = False
