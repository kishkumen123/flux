# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

from flux import _globals
from flux.events import events
from flux.mouse import mouse
from flux.screen import Display
from flux.poly import Poly
from flux.console import console
from flux.commands import run_command
from flux.grid_generator import GridGenerator
from flux.ui import ui


class Flux:

    def __init__(self, play_time=0, fps=60):
        self.fps = fps
        self.play_time = play_time
        self.clock = pygame.time.Clock()
        self._delta_time = 0
        self.miliseconds = 0
        self.display = None
        self._elapsed_time = 0
        self.ui = None
        self.frame_index = 1
        self.events = events

    def init(self):
        pygame.init()
        run_command("level one")
        self.ui = ui

    def init_display(self, resolution):
        self.display = Display
        self.display.init(resolution)

        return self.display

    def set_fps(self, fps):
        self.fps = fps

    def get_fps(self):
        return self.clock.get_fps()

    def update_delta_time(self):
        self._delta_time = self.clock.tick(self.fps) / 1000
        self._elapsed_time += self._delta_time / 1000.0

    @property
    def delta_time(self):
        return self._delta_time

    @property
    def elapsed_time(self):
        return self._elapsed_time

    def get_poly_dict(self):
        return _globals.poly_dict

    def draw_poly(self):
        for poly in _globals.poly_dict:
            poly.draw()

    def create_poly(self, name, layer, color, points, surface=None, width=0):
        if surface is None:
            surface = self.display.fake_display

        poly = Poly(name, layer, color, points, surface, width)
        _globals.poly_dict.append(poly)

        return poly

    def generate_world(self, view_distance=2000, chunk_size=800, scale=10, octaves=2, persistence=0.3, lacunarity=4, seed=1, offset=(0, 0), color_height_map=None):
        self.grid_generator = GridGenerator(view_distance, chunk_size, scale, octaves, persistence, lacunarity, seed, offset, color_height_map)

        return self.grid_generator

    def create_surface(self, size, color):
        surface = pygame.Surface(size).convert()
        surface.fill(color)
        return surface

    def quit(self):
        print("quit")
        pygame.quit()

    def is_running(self):
        return _globals.running

    def key_pressed(self, key, layer="layer_0"):
        return events.key_pressed(key, layer)

    def key_pressed_once(self, key, layer="layer_0"):
        return events.key_pressed_once(key, layer)

    def event_triggered(self, event, layer="layer_0"):
        return events.event_triggered(event, layer)

    def mousebutton_pressed(self, button, layer="layer_0"):
        return mouse.button_pressed(button, layer)

    def update(self):
        self.update_delta_time()
        events.update()
        self.ui.update()
        mouse.update()

        console.update(self.delta_time)

        _globals.draw()
        self.frame_index += 1

    def flush(self):
        events.flush()

    def kill(self):
        _globals.running = False
