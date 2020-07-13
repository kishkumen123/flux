# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import json

from collections import defaultdict
from flux import _globals
from flux.events import events
from flux.mouse import mouse
from flux.screen import Display
from flux.console import console
from flux.entity_manager import EM
from flux.commands import run_command
from flux.sprite_groups import sprite_groups

#from flux.poly import Poly
#from flux.grid_generator import GridGenerator
#from flux.ui import ui
#from flux.renderer import renderer


class Flux:

    def __init__(self, play_time=0, fps=60):
        self.fps = fps
        self.play_time = play_time
        self.clock = pygame.time.Clock()
        self._delta_time = 0
        self.miliseconds = 0
        self.display = None
        self._elapsed_time = 0
        #delete
        #self.ui = None
        #self.renderer = None
        self.frame_index = 1
        self.events = events
        self.mouse = None
        #delete
        self.decorated_functions = defaultdict(list)
        self.sprite_groups = None

        #self.register_components()
        #self.init_groups()
        #self.load_entities()

    def init(self):
        pygame.init()
        #self.ui = ui
        #self.renderer = renderer
        self.mouse = mouse
        self.sprite_groups = sprite_groups

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
        self._elapsed_time += self._delta_time

    def load_level(self, level):
        run_command("level " + str(level))

    @property
    def delta_time(self):
        return self._delta_time

    @property
    def elapsed_time(self):
        return self._elapsed_time

    def register_components(self, components):
        for c in components:
            EM.register_component(c)

    def init_groups(self, groups_json):
        with open(groups_json) as f:
            groups_data = json.load(f)

        for g in groups_data["groups"]:
            self.sprite_groups.create(g)

    def load_entities(self, entities_json):
        with open(entities_json) as f:
            data = json.load(f) 

        for e, d in data.items():
            components = []
            arguments = []
            for c in d["components"].keys():
                components.append(EM.components[c])
                arguments.append(d["components"][c])
            EM.create(components, arguments)

    #delete
    def get_poly_dict(self):
        return _globals.poly_dict

    #delete
    def draw_poly(self):
        for poly in _globals.poly_dict:
            poly.draw()

    #delete
    def create_poly(self, name, layer, color, points, surface=None, width=0):
        if surface is None:
            surface = self.display.fake_display

        poly = Poly(name, layer, color, points, surface, width)
        _globals.poly_dict.append(poly)

        return poly

    def generate_world(self, view_distance=2000, chunk_size=800, scale=10, octaves=2, persistence=0.3, lacunarity=4, seed=1, offset=(0, 0), color_height_map=None):
        self.grid_generator = GridGenerator(view_distance, chunk_size, scale, octaves, persistence, lacunarity, seed, offset, color_height_map)

        return self.grid_generator

    #delete
    def create_surface(self, size, color):
        surface = pygame.Surface(size).convert()
        surface.fill(color)
        return surface

    def quit(self):
        print("quit")
        pygame.quit()

    def is_running(self):
        return _globals.running

    def key_released(self, key, layer="layer_0"):
        return events.key_released(key, layer)

    def key_pressed(self, key, layer="layer_0"):
        return events.key_pressed(key, layer)

    def key_pressed_repeat(self, key, layer="layer_0"):
        return events.key_pressed_repeat(key, layer)

    def key_pressed_once(self, key, layer="layer_0"):
        return events.key_pressed_once(key, layer)

    def event_triggered(self, event, layer="layer_0"):
        return events.event_triggered(event, layer)

    def button_released(self, button, layer="layer_0"):
        return events.button_released(button, layer)

    def button_pressed(self, button, layer="layer_0"):
        return events.button_pressed(button, layer)

    def button_pressed_once(self, button, layer="layer_0"):
        return events.button_pressed_once(button, layer)


    # delete
    def update_sprite_mouse_movable(self):
        for group_name, functions in self.decorated_functions.items():
            for function in functions:
                function(mouse, self.renderer.get_group(group_name))

    def update(self):
        self.update_delta_time()
        events.update()

        console.update(self.delta_time)
        mouse.update()
        self.frame_index += 1

    def flush(self):
        events.flush()

    def kill(self):
        _globals.running = False
