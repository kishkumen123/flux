import pygame

from flux.fmath import Vector2, load_image
from flux.sprite_groups import sprite_groups


#write code for easier operations like scale, rotate
class Sprite(pygame.sprite.Sprite):

    def __init__(self, image="", group="", layer=0, position=(0, 0)):
        self.name = image
        self.image, self.rect = load_image(image)
        pygame.sprite.Sprite.__init__(self, sprite_groups.get_group(group))
        self._layer = layer
        self.rect = position
        self.name = image.split(".")[0]
        self.render = True

    def scale(self, sizex, sizey):
        self.image = pygame.transform.scale(self.image, (sizex, sizey))

    def __repr__(self):
        return "<Sprite - name: %s, layer: %s>" % (self.name, self._layer)

    def __str(self):
        return "<Sprite - name: %s, layer: %s>" % (self.name, self._layer)


#write code for easier operations like trasnform
class Transform():
    def __init__(self, position=(0,0), scale=(1, 1)):
        self.position = Vector2(position)
        self.scale = Vector2(scale)

    def translate(self, x, y):
        self.position.x += x
        self.position.y += y


components_list = [
    Sprite, 
    Transform
]
