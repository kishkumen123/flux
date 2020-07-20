import pygame
import random

from pygame import Surface
from entity_manager import EM
from sprite_groups import sprite_groups
from components import Transform, Sprite, Particle
from controller import Controller
from entity_manager import EM
from sprite_manager import SM


class RenderSystem():

    @classmethod
    def update(cls, exclude=None):
        e_ids = EM.ids_of_component(Transform, Sprite)
        
        for _id in e_ids:
            sprite = EM.entities[_id].components[Sprite]
            transform = EM.entities[_id].components[Transform]

            sprite.image = pygame.transform.scale(sprite.image, (transform.scale.x, transform.scale.y))
            sprite.rect.x = transform.position.x
            sprite.rect.y = transform.position.y

    @classmethod
    def draw(cls, screen, exclude=None):
        entities = EM.entities_of_component(Transform, Sprite)
        sorted_entities = SM.sort(entities)

        for e in sorted_entities:
            sprite = e.components[Sprite]
            transform = e.components[Transform]
            screen.blit(sprite.image, (transform.position.x, transform.position.y))


class ScaleSprite():

    @classmethod
    def update(self, dt):
        e_ids = EM.ids_of_component(Transform, Sprite)

        for _id in e_ids:
            sprite = EM.entities[_id].components[Sprite]
            transform = EM.entities[_id].components[Transform]

            if "blue" in sprite.name:
                transform.scale.x += int(200 * dt)
                transform.scale.y += int(200 * dt)


class TranslateSprite():

    @classmethod
    def update(self, dt):
        e_ids = EM.ids_of_component(Transform, Sprite)

        for _id in e_ids:
            transform = EM.entities[_id].components[Transform]
            sprite = EM.entities[_id].components[Sprite]
            if "blue" in sprite.name:
                transform.position.x += 100 * dt


class MovePlayer():

    @classmethod
    def update(self, dt):
        e_ids = EM.ids_of_component(Transform, Sprite)

        for _id in e_ids:
            transform = EM.entities[_id].components[Transform]
            sprite = EM.entities[_id].components[Sprite]

            if "white" in sprite.name:
                if Controller.left:
                    transform.position.x -= 100 * dt
                if Controller.right:
                    transform.position.x += 100 * dt
                if Controller.up:
                    transform.position.y -= 100 * dt
                if Controller.down:
                    transform.position.y += 100 * dt


class MouseMoveSprite():
    found = False

    @classmethod
    def update(self):
        entities = EM.entities_of_component(Transform, Sprite)

        sorted_entities = SM.sort(entities)
        sorted_entities.reverse()

        for e in sorted_entities:
            transform = e.components[Transform]
            sprite = e.components[Sprite]

            if Controller.m1:
                if sprite.rect.collidepoint(pygame.mouse.get_pos()):

                    if transform.move_offset is None and not MouseMoveSprite.found:
                        transform.move_offset = (pygame.mouse.get_pos()[0] - transform.position.x, pygame.mouse.get_pos()[1] - transform.position.y)
                        MouseMoveSprite.found = True
                        
                if transform.move_offset:
                    transform.position.x = pygame.mouse.get_pos()[0] - transform.move_offset[0]
                    transform.position.y = pygame.mouse.get_pos()[1] - transform.move_offset[1]
            else:
                transform.move_offset = None
                MouseMoveSprite.found = False


class ParticleSystem:

    @classmethod
    def update(self, screen, dt):
        if Controller.m3:
            mx, my = pygame.mouse.get_pos()
            EM.create([Transform, Particle], [{"position": [random.randint(mx-50, mx+50), random.randint(my-50, my+50)], "scale": [20, 20]}, {"alive_time": 10, "velocity": [100, -200], "radius": [8, 16]}])

        e_ids = EM.ids_of_component(Transform, Particle)
        
        for _id in e_ids:
            transform = EM.entities[_id].components[Transform]
            particle = EM.entities[_id].components[Particle]

            if particle.radius > 0:
                transform.position.x += particle.velocity.x * dt
                transform.position.y += particle.velocity.y * dt

                #particle.velocity.y += 1000 * dt
                particle.radius -= 10 * dt
                pygame.draw.circle(screen, (255, 255, 255), (int(transform.position.x), int(transform.position.y)), int(particle.radius))
            else:
                EM.destroy(_id)


class CS:
    player_sprite = None
    colliders = []

    @classmethod
    def update(self, dt=0):
        CS.colliders.clear()
        e_ids = EM.ids_of_component(Transform, Sprite)
        
        if not CS.player_sprite:
            for _id in e_ids:
                sprite = EM.entities[_id].components[Sprite]
                if "white" in sprite.name:
                    CS.player_sprite = sprite

        for _id in e_ids:
            transform = EM.entities[_id].components[Transform]
            sprite = EM.entities[_id].components[Sprite]
            if sprite != CS.player_sprite:
                if CS.player_sprite.rect.colliderect(sprite.rect):
                    CS.colliders.append(sprite.name)

        #print(CS.colliders)
