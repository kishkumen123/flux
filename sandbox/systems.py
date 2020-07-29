import pygame
import random
import _globals

from entity_manager import EM
from controller import Controller
from entity_manager import EM, Properties, textures
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

        #print(UI.hot)

        #if Events.mbutton_down(1) and not Controller.shift and not UI.hot:
        if Events.mbutton_up(1):
            if cls.canvas is not None:
                cls.canvas.move_offset = None
                cls.canvas = None
                cls.found = False

        if Events.mbutton_down(1) and not UI.hot:
            print("OK")
            for c in sorted_canvases:
                if c.rect.collidepoint(pygame.mouse.get_pos()):
                    if c.move_offset is None and not cls.found:
                        UIMouseMove.found = True
                        c.move_offset = (pygame.mouse.get_pos()[0] - c.rect.x, pygame.mouse.get_pos()[1] - c.rect.y)
                        cls.canvas = c

                #if c.move_offset and e.property.MouseMovable:
        #else:
            #if cls.canvas is not None:
                #cls.canvas.move_offset = None
                #UIMouseMove.found = False

        if cls.canvas is not None:
            cls.canvas.rect.x = pygame.mouse.get_pos()[0] - cls.canvas.move_offset[0]
            cls.canvas.rect.y = pygame.mouse.get_pos()[1] - cls.canvas.move_offset[1]


class UIResize():
    found = False
    side = []

    @classmethod
    def update(self):
        entities = []

        for c in UI.canvases.values():
            entities.append(c)
        sorted_canvases = SM.sort_ui(entities)
        sorted_canvases.reverse()


        for c in sorted_canvases:
            if Controller.m1 and Controller.shift:
                if c.rect.collidepoint(pygame.mouse.get_pos()):
                    if c.side_offset is None and not UIResize.found:
                        UIResize.found = True
                        c.side_offset = (pygame.mouse.get_pos()[0] - c.rect.x, pygame.mouse.get_pos()[1] - c.rect.y)
                        c.right_offset = (c.rect.x + c.rect.w) - pygame.mouse.get_pos()[0]
                        c.bottom_offset = (c.rect.y + c.rect.h) - pygame.mouse.get_pos()[1]

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

                #if c.side_offset and e.property.MouseMovable:
                if c.side_offset:
                    for i, _ in enumerate(UIResize.side):
                        if UIResize.side[i] == "left":
                            x = pygame.mouse.get_pos()[0] - c.side_offset[0]
                            c.rect.w -= x - c.rect.x
                            c.rect.x = x
                        if UIResize.side[i] == "right":
                            c.rect.w = (pygame.mouse.get_pos()[0] - c.rect.x) + c.right_offset
                        if UIResize.side[i] == "top":
                            y = pygame.mouse.get_pos()[1] - c.side_offset[1]
                            c.rect.h -= y - c.rect.y
                            c.rect.y = y
                        if UIResize.side[i] == "bottom":
                            c.rect.h = (pygame.mouse.get_pos()[1] - c.rect.y) + c.bottom_offset

                    #c.rect.y = pygame.mouse.get_pos()[1] - c.side_offset[1]
            else:
                c.side_offset = None
                UIResize.side = []
                UIResize.found = False



class RenderSystem():

    @classmethod
    def draw(cls, screen, exclude=None):
        entities = []

        for e in EM.entities.values():
            if e.property.Renderable:
                entities.append(e)
        sorted_entities = SM.sort_sprites(entities)

        for e in sorted_entities:
            e.rect.x = e.position[0]
            e.rect.y = e.position[1]
            if e.property.UIPanel:
                pygame.draw.rect(screen, e.color, e.rect)
            elif e.property.UIButton:
                pygame.draw.rect(screen, e.color, e.rect)
                screen.blit(e.text_surface, (e.position.x, e.position.y))
            else:
                e.sprite = pygame.transform.scale(e.sprite, (e.scale[0], e.scale[1]))
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
            if e.property.Movable:
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

    @classmethod
    def update(self):
        entities = []

        for e in EM.entities.values():
            if e.property.Renderable:
                entities.append(e)
        sorted_entities = SM.sort_sprites(entities)
        sorted_entities.reverse()


        for e in sorted_entities:
            if Controller.m1:
                if e.rect.collidepoint(pygame.mouse.get_pos()):
                    if e.move_offset is None and not MouseMoveSprite.found:
                        MouseMoveSprite.found = True
                        e.move_offset = (pygame.mouse.get_pos()[0] - e.position[0], pygame.mouse.get_pos()[1] - e.position[1])
                        if e.children:
                            for _id in e.children:
                                e_child = EM.get(_id)
                                e_child.move_offset = (pygame.mouse.get_pos()[0] - e_child.position[0], pygame.mouse.get_pos()[1] - e_child.position[1])

                if e.move_offset and e.property.MouseMovable:
                    e.position.x = pygame.mouse.get_pos()[0] - e.move_offset[0]
                    e.position.y = pygame.mouse.get_pos()[1] - e.move_offset[1]
                    if e.children:
                        for _id in e.children:
                            e_child = EM.get(_id)
                            e_child.position.x = pygame.mouse.get_pos()[0] - e_child.move_offset[0]
                            e_child.position.y = pygame.mouse.get_pos()[1] - e_child.move_offset[1]
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
            EM.load_entity("entity_5", {})


        entities = list(EM.entities.values())
        for e in entities:
            if e.property.IsParticle:
                if e.circle_radius > 0:
                    e.position.x += e.velocity.x * dt
                    e.position.y += e.velocity.y * dt

                    #e.velocity.y += 1000 * dt
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
            if e._id != 3 and e.property.Renderable:
                if CS.player_sprite_rect.colliderect(e.rect):
                    CS.colliders.append(e._id)

        #print(CS.colliders)

class SelectSystem:
    selected = False

    @classmethod
    def update(cls):
        entities = []

        for e in EM.entities.values():
            if e.property.Renderable:
                entities.append(e)
        sorted_entities = SM.sort_sprites(entities)
        sorted_entities.reverse()

        for e in sorted_entities:
            if Controller.m1 and not SelectSystem.selected:
                if e.rect.collidepoint(pygame.mouse.get_pos()):
                    _globals.selection = e
                    SelectSystem.selected = True
                    break
        if Controller.m1 is False:
            SelectSystem.selected = False
