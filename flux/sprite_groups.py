import pygame


class SpriteGroups():

    def __init__(self):
        self.group_dict = {}

    def get_group(self, name):
        return self.group_dict[name]

    def create(self, name):
        self.group_dict[name] = pygame.sprite.LayeredUpdates()

    def flush(self):
        self.group_dict = {}

sprite_groups = SpriteGroups()
