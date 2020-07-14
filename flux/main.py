# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import json
import sys

from flux import _globals
from flux.events import events
from flux.display import display
from flux.entity_manager import EM
from flux.sprite_groups import sprite_groups
from flux.console import c
#from flux.console import console
#from flux.commands import run_command


class Flux:

    def __init__(self, fps=60):
        self.fps = fps
        self.clock = pygame.time.Clock()
        self._dt = 0
        self._elapsed_time = 0
        self.frame_index = 1
        self.events = events
        self.sprite_groups = None
        self.sprite_groups = sprite_groups

    def init(self):
        pygame.init()

    def get_display(self):
        return display.window

    def set_fps(self, _fps):
        self.fps = _fps

    def get_fps(self):
        return self.clock.get_fps()

    def update_dt(self):
        self._dt = self.clock.tick(self.fps) / 1000
        self._elapsed_time += self._dt

    def dt(self):
        return self._dt

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

    def key_held(self, key, layer="layer_0"):
        return events.key_held(key, layer)

    def key_pressed(self, key, layer="layer_0"):
        return events.key_pressed(key, layer)

    def key_released(self, key, layer="layer_0"):
        return events.key_released(key, layer)

    def text_input(self, layer="layer_0"):
        return events.text_input(layer)

    def flip(self):
        pygame.display.flip()

    def quit(self):
        print("quit")
        _globals.running = False
        pygame.quit()
        sys.exit(0)

    def is_running(self):
        return _globals.running

    def update(self):
        self.update_dt()
        events.update()

        #console.update(self._dt)
        c.update(self._dt)
        self.frame_index += 1

    def kill(self):
        _globals.running = False
