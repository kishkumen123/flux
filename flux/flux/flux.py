# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import globals

from events import events
from mouse import mouse
from screen import Display
from poly import Poly
from console import console
from commands import run_command
from grid_generator import GridGenerator
from ui import ui


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
        return globals.poly_dict

    def draw_poly(self):
        for poly in globals.poly_dict:
            poly.draw()

    def create_poly(self, name, layer, color, points, surface=None, width=0):
        if surface is None:
            surface = self.display.fake_display

        poly = Poly(name, layer, color, points, surface, width)
        globals.poly_dict.append(poly)

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
        return globals.running

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
        self.ui.update()
        console.update(self.delta_time)

        mouse.update()
        events.update()

    def kill(self):
        globals.running = False
