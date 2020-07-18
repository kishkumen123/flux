import pygame
from pygame import Surface
from entity_manager import EM
from sprite_groups import sprite_groups
from components import Transform, Sprite


class RenderSystem():

    @classmethod
    def update(cls, exclude=None):
        entities = EM.entities_of_component(Transform, Sprite)
        
        for e in entities:
            sprite = e.components[Sprite]
            transform = e.components[Transform]

            sprite.image = pygame.transform.scale(sprite.image, (transform.scale.x, transform.scale.y))
            sprite.rect = transform.position

        for group in sprite_groups.group_dict.values():
            group.update()

    @classmethod
    def draw(cls, screen, exclude=None):
        for group in sprite_groups.group_dict.values():
            group.draw(screen)


class ScaleSprite():

    @classmethod
    def update(self, dt):
        entities = EM.entities_of_component(Transform, Sprite)

        for e in entities:
            sprite = e.components[Sprite]
            transform = e.components[Transform]

            if "blue" in sprite.name:
                transform.scale.x += int(200 * dt)
                transform.scale.y += int(200 * dt)


class TranslateSprite():

    @classmethod
    def update(self, dt):
        entities = EM.entities_of_component(Transform, Sprite)

        for e in entities:
            transform = e.components[Transform]
            sprite = e.components[Sprite]
            if "blue" in sprite.name:
                transform.position.x += 100 * dt
