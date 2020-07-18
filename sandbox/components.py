import pygame

from fmath import Vector2
from sprite_groups import sprite_groups


class Sprite(pygame.sprite.Sprite):

    def __init__(self, image="", group="", layer=0):
        pygame.sprite.Sprite.__init__(self, sprite_groups.get_group(group))

        self.name = image.split(".")[0]
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self._layer = layer

    def __repr__(self):
        return "<Sprite - name: %s, layer: %s>" % (self.name, self._layer)

    def __str__(self):
        return "<Sprite - name: %s, layer: %s>" % (self.name, self._layer)


class Transform():
    def __init__(self, position=(0,0), scale=(1, 1)):
        self.position = Vector2(position)
        self.scale = Vector2(scale)


components_list = [
    Sprite, 
    Transform
]
