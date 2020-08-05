import pygame
import random
import _globals

from pygame.locals import *
from entity_manager import EM
from controller import Controller
from entity_manager import EM, textures
from sprite_manager import SM
from ui import UI
from events import Events



class UIMouseMove():
    found = False
    canvas = None

    @classmethod
    def update(cls):
        entities = []

        for c in UI.canvases.values():
            entities.append(c)
        sorted_canvases = SM.sort_ui(entities)
        sorted_canvases.reverse()

        for event in Events():
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if cls.canvas is not None:
                        cls.canvas.move_offset = None
                        cls.canvas = None
                        cls.found = False
                        Events.consume(event)

        for event in Events():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and not Controller.shift:
                    for c in sorted_canvases:
                        if c.rect.collidepoint(pygame.mouse.get_pos()):
                            if c.move_offset is None and not cls.found:
                                UIMouseMove.found = True
                                c.move_offset = (pygame.mouse.get_pos()[0] - c.rect.x, pygame.mouse.get_pos()[1] - c.rect.y)
                                cls.canvas = c
                                Events.consume(event)

        if cls.canvas is not None:
            cls.canvas.rect.x = pygame.mouse.get_pos()[0] - cls.canvas.move_offset[0]
            cls.canvas.rect.y = pygame.mouse.get_pos()[1] - cls.canvas.move_offset[1]


class UIResize():
    found = False
    side = []
    c = None

    @classmethod
    def update(cls):
        entities = []

        for c in UI.canvases.values():
            entities.append(c)
        sorted_canvases = SM.sort_ui(entities)
        sorted_canvases.reverse()


        for event in Events():
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if cls.c is not None:
                        cls.c.side_offset = None
                        cls.c.right_offset = None
                        cls.c.bottom_offset = None
                        cls.side = []
                        cls.found = False
                        cls.c = None

        for event in Events():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and Controller.shift:
                    for c in sorted_canvases:
                        if c.rect.collidepoint(pygame.mouse.get_pos()):
                            if c.side_offset is None and not UIResize.found:
                                UIResize.found = True
                                c.side_offset = (pygame.mouse.get_pos()[0] - c.rect.x, pygame.mouse.get_pos()[1] - c.rect.y)
                                c.right_offset = (c.rect.x + c.rect.w) - pygame.mouse.get_pos()[0]
                                c.bottom_offset = (c.rect.y + c.rect.h) - pygame.mouse.get_pos()[1]

                                cls.c = c

                                distances = [
                                    ("left", abs(c.rect.x - pygame.mouse.get_pos()[0])), 
                                    ("right", abs(c.rect.x + c.rect.w - pygame.mouse.get_pos()[0])), 
                                    ("top", abs(c.rect.y - pygame.mouse.get_pos()[1])), 
                                    ("bottom", abs(c.rect.y + c.rect.h - pygame.mouse.get_pos()[1]))
                                ]
                                distances.sort(key = lambda x: x[1])
                                if distances[0][1] < 15 and distances[1][1] < 15:
                                    UIResize.side.append(distances[0][0])
                                    UIResize.side.append(distances[1][0])
                                else:
                                    UIResize.side.append(distances[0][0])

        if cls.c is not None:
            for i, _ in enumerate(UIResize.side):
                if UIResize.side[i] == "left":
                    x = pygame.mouse.get_pos()[0] - cls.c.side_offset[0]
                    cls.c.rect.w -= x - cls.c.rect.x
                    cls.c.rect.x = x
                if UIResize.side[i] == "right":
                    cls.c.rect.w = (pygame.mouse.get_pos()[0] - cls.c.rect.x) + cls.c.right_offset
                if UIResize.side[i] == "top":
                    y = pygame.mouse.get_pos()[1] - cls.c.side_offset[1]
                    cls.c.rect.h -= y - cls.c.rect.y
                    cls.c.rect.y = y
                if UIResize.side[i] == "bottom":
                    new_h = (pygame.mouse.get_pos()[1] - cls.c.rect.y) + cls.c.bottom_offset
                    cls.c.rect.h = new_h



class RenderSystem():

    @classmethod
    def draw(cls, screen, exclude=None):
        entities = []

        for e in EM.entities.values():
            if e.Renderable:
                entities.append(e)
        sorted_entities = SM.sort_sprites(entities)

        for e in sorted_entities:
            e.rect.x = e.position[0]
            e.rect.y = e.position[1]
            e.sprite = pygame.transform.scale(e.sprite, (e.scale[0], e.scale[1]))
            e.rect = pygame.Rect(e.rect.x, e.rect.y, e.sprite.get_rect().w, e.sprite.get_rect().h)
            screen.blit(e.sprite, (e.rect.x, e.rect.y))


class ScaleSprite():

    @classmethod
    def update(self, dt):
        for e in EM.entities.values():
            if 1 == e._id:
                e.scale.x += int(200 * dt)
                e.scale.y += int(200 * dt)


class TranslateSprite():

    @classmethod
    def update(self, dt):
        for e in EM.entities.values():
            if 1 == e._id:
                e.position.x += 100 * dt


class MovePlayer():

    @classmethod
    def update(cls, dt):
        for e in EM.entities.values():
            if e.Movable:
                MovePlayer.move(e, 100, dt)

                if e.children:
                    for _id in e.children:
                        child_e = EM.get(_id)
                        MovePlayer.move(child_e, 100, dt)


    @classmethod
    def move(cls, e, amount, dt):
        if Controller.left:
            e.position.x -= amount * dt
        if Controller.right:
            e.position.x += amount * dt
        if Controller.up:
            e.position.y -= amount * dt
        if Controller.down:
            e.position.y += amount * dt


class MouseMoveSprite():
    found = False
    e = None

    @classmethod
    def update(cls):
        entities = []

        for e in EM.entities.values():
            if e.Renderable:
                entities.append(e)
        sorted_entities = SM.sort_sprites(entities)
        sorted_entities.reverse()

        for event in Events():
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if cls.e is not None:
                        cls.e.move_offset = None
                        if e.children:
                            for _id in e.children:
                                e_child = EM.get(_id)
                                e_child.move_offset = None
                        cls.e = None
                        cls.found = False
                        Events.consume(event)

        #TODO(Rafik): this children itteration seems odd. i think i need to do this in the draw call once, not everywhere
        for event in Events():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and not Controller.shift:
                    for e in sorted_entities:
                        if e.rect.collidepoint(pygame.mouse.get_pos()):
                            if e.move_offset is None and not cls.found:
                                MouseMoveSprite.found = True
                                e.move_offset = (pygame.mouse.get_pos()[0] - e.position[0], pygame.mouse.get_pos()[1] - e.position[1])
                                if e.children:
                                    for _id in e.children:
                                        e_child = EM.get(_id)
                                        e_child.move_offset = (pygame.mouse.get_pos()[0] - e_child.position[0], pygame.mouse.get_pos()[1] - e_child.position[1])
                                cls.e = e
                                Events.consume(event)

        if cls.e is not None and cls.e.MouseMovable:
            cls.e.position.x = pygame.mouse.get_pos()[0] - cls.e.move_offset[0]
            cls.e.position.y = pygame.mouse.get_pos()[1] - cls.e.move_offset[1]
            if e.children:
                for _id in cls.e.children:
                    e_child = EM.get(_id)
                    e_child.position.x = pygame.mouse.get_pos()[0] - e_child.move_offset[0]
                    e_child.position.y = pygame.mouse.get_pos()[1] - e_child.move_offset[1]


class ParticleSystem:
    m1_down = False

    @classmethod
    def update(cls, screen, dt):
        for event in Events():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    cls.m1_down = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 3:
                    cls.m1_down = False

        if cls.m1_down:
            EM.load_entity("entity_5", {})


        entities = list(EM.entities.values())
        for e in entities:
            if e.IsParticle:
                if e.circle_radius > 0:
                    e.position.x += e.velocity.x * dt
                    e.position.y += e.velocity.y * dt

                    e.velocity.y += 1000 * dt
                    if (e.circle_radius - 10*dt) > 0:
                        e.circle_radius -= 10 * dt
                    else:
                        e.circle_radius = 0

                    #TODO:(Rafik) i wonder if this should be drawing here, and should be adding a drawable rect to the entitiy, and     then have it be drawn in the draw method
                    pygame.draw.circle(screen, e.circle_color, (int(e.position.x), int(e.position.y)), int(e.circle_radius))
                else:
                    EM.destroy(e._id)


class CS:
    player_sprite_rect = None
    colliders = []

    @classmethod
    def update(self, dt=0):
        CS.colliders.clear()

        if CS.player_sprite_rect is None:
            for e in EM.entities.values():
                if e._id == 3:
                    CS.player_sprite_rect = e.rect

        for e in EM.entities.values():
            if e._id != 3 and e.Renderable:
                if CS.player_sprite_rect.colliderect(e.rect):
                    CS.colliders.append(e._id)

        #print(CS.colliders)

class SelectSystem:
    selected = False

    @classmethod
    def update(cls):
        entities = []

        for e in EM.entities.values():
            if e.Renderable:
                entities.append(e)
        sorted_entities = SM.sort_sprites(entities)
        sorted_entities.reverse()

        for event in Events():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    cls.selected = False
                    for e in sorted_entities:
                        if e.rect.collidepoint(pygame.mouse.get_pos()):
                            _globals.selection = e
                            cls.selected = True
                            break
                    #if not cls.selected:
                        #_globals.selection = None
                        #cls.selected = False
