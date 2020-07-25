import pygame
import random

from entity_manager import EM
from controller import Controller
from entity_manager import EM, Properties, textures
from sprite_manager import SM


class RenderSystem():

    @classmethod
    def draw(cls, screen, exclude=None):
        entities = []

        for e in EM.entities.values():
            if e.property.Renderable:
                entities.append(e)
        sorted_entities = SM.sort(entities)

        for e in sorted_entities:
            e.sprite_rect.x = e.position[0]
            e.sprite_rect.y = e.position[1]
            e.sprite = pygame.transform.scale(e.sprite, (e.scale[0], e.scale[1]))
            screen.blit(e.sprite, (e.sprite_rect.x, e.sprite_rect.y))


class ScaleSprite():

    @classmethod
    def update(self, dt):
        for e in EM.entities.values():
            if 1 == e._id:
                e.scale[0] += int(200 * dt)
                e.scale[1] += int(200 * dt)


class TranslateSprite():

    @classmethod
    def update(self, dt):
        for e in EM.entities.values():
            if 1 == e._id:
                e.position[0] += 100 * dt


class MovePlayer():

    @classmethod
    def update(cls, dt):
        for e in EM.entities.values():
            if e.property.Movable:
                MovePlayer.move(e, 100, dt)
                
                if e.children:
                    for _id in e.children:
                        child_e = EM.get(_id)
                        MovePlayer.move(child_e, 100, dt)


    @classmethod
    def move(cls, e, amount, dt):
        if Controller.left:
            e.position[0] -= amount * dt
        if Controller.right:
            e.position[0] += amount * dt
        if Controller.up:
            e.position[1] -= amount * dt
        if Controller.down:
            e.position[1] += amount * dt


class MouseMoveSprite():
    found = False
    move_offset = None

    @classmethod
    def update(self):
        entities = []

        for e in EM.entities.values():
            if e.property.Renderable:
                entities.append(e)
        sorted_entities = SM.sort(entities)
        sorted_entities.reverse()

    
        for e in sorted_entities:
            if Controller.m1:
                if e.sprite_rect.collidepoint(pygame.mouse.get_pos()):
                    if e.move_offset is None and not MouseMoveSprite.found:
                        e.move_offset = (pygame.mouse.get_pos()[0] - e.position[0], pygame.mouse.get_pos()[1] - e.position[1])
                        if e.children:
                            for _id in e.children:
                                e_child = EM.get(_id)
                                e_child.move_offset = (pygame.mouse.get_pos()[0] - e_child.position[0], pygame.mouse.get_pos()[1] - e_child.position[1])
                        MouseMoveSprite.found = True
                        
                if e.move_offset:
                    e.position[0] = pygame.mouse.get_pos()[0] - e.move_offset[0]
                    e.position[1] = pygame.mouse.get_pos()[1] - e.move_offset[1]
                    if e.children:
                        for _id in e.children:
                            e_child = EM.get(_id)
                            e_child.position[0] = pygame.mouse.get_pos()[0] - e_child.move_offset[0]
                            e_child.position[1] = pygame.mouse.get_pos()[1] - e_child.move_offset[1]
            else:
                e.move_offset = None
                if e.children:
                    for _id in e.children:
                        e_child = EM.get(_id)
                        e_child.move_offset = None
                MouseMoveSprite.found = False


class ParticleSystem:

    @classmethod
    def update(self, screen, dt):
        if Controller.m3:
            EM.load_entity("entity_5")

        
        entities = list(EM.entities.values())
        for e in entities:
            if e.property.IsParticle:
                if e.circle_radius > 0:
                    e.position.x += e.velocity.x * dt
                    e.position.y += e.velocity.y * dt

                    e.velocity.y += 1000 * dt
                    if (e.circle_radius - 10*dt) > 0:
                        e.circle_radius -= 10 * dt
                    else:
                        e.circle_radius = 0

                    pygame.draw.circle(screen, e.circle_color, (int(e.position.x), int(e.position.y)), int(e.circle_radius))
                else:
                    EM.destroy(e._id)


class CS:
    player_sprite_rect = None
    colliders = []

    @classmethod
    def update(self, dt=0):
        CS.colliders.clear()
        #e_ids = EM.ids_of_component(Transform, Sprite)
        
        if CS.player_sprite_rect is None:
            for e in EM.entities.values():
                if e._id == 3:
                    CS.player_sprite_rect = e.sprite_rect

        for e in EM.entities.values():
            if e._id != 3 and e.property.Renderable:
                if CS.player_sprite_rect.colliderect(e.sprite_rect):
                    CS.colliders.append(e._id)

        #print(CS.colliders)
