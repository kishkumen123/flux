import pygame
import random

from fmath import Vector2
from sprite_groups import sprite_groups


class Sprite:
    def __init__(self, image=0, group=0, layer=0):
        self.image = pygame.image.load(image)
        self.name = image.split(".")[0]
        self.rect = self.image.get_rect()
        self.group = group
        self.layer = layer
        

class Transform():
    def __init__(self, position=(0,0), scale=(1, 1)):
        self.position = Vector2(position)
        self.scale = Vector2(scale)
        self.move_offset = None


class Particle():
    def __init__(self, alive_time=0, velocity=(0,0), radius=(1,1)):
        self.alive_time = alive_time
        self.velocity = Vector2((random.randint(-velocity[0], velocity[0]), velocity[1]))
        self.radius = random.randint(radius[0], radius[1])


components_list = [
    Sprite, 
    Transform,
    Particle
]
