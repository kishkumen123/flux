import pygame
from pygame import Surface
from flux.entity_manager import EM
from flux.sprite_groups import sprite_groups
from components import Transform, Sprite


class RenderSystem():

    @classmethod
    def update(cls, exclude=None):
        for group in sprite_groups.group_dict.values():
            group.update()

    @classmethod
    def draw(cls, screen, exclude=None):
        for group in sprite_groups.group_dict.values():
            group.draw(screen)


class SpritePosition():

    @classmethod
    def update(self):
        entities = EM.entities_of_component(Transform, Sprite)

        for e in entities:
            transform = e.components[Transform]
            sprite = e.components[Sprite]

            sprite.rect = transform.position


class TransformScaleSprite():

    @classmethod
    def update(self, dt):
        entities = EM.entities_of_component(Transform, Sprite)

        for e in entities:
            transform = e.components[Transform]
            sprite = e.components[Sprite]
            if "blue" in sprite.name:
                transform.translate(100 * dt, 0)
                sprite.scale(sprite.image.get_width() + int(200 * dt), sprite.image.get_height() + int(200 * dt))
