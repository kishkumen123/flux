import sys
import pygame
import _globals

from pygame.locals import *
from console import Console, CState
from entity_manager import EM, load_textures
from systems import RenderSystem, ScaleSprite, TranslateSprite, MovePlayer, CS, ParticleSystem, MouseMoveSprite, SelectSystem
from controller import Controller
 

pygame.init()
 
fps = 250
clock = pygame.time.Clock()
frame = 0
elapsed_time = 0
 
width, height = 1024, 720
screen = pygame.display.set_mode((width, height))


console = Console(screen, _globals.font)


load_textures("data/textures/*")
EM.load_entities("data/entities/*")
e_panel = EM.load_entity("entity_6", {"position":"position=v2(300,300)", "color":"color=(70,74,71)", "rect":"rect=pygame.Rect(300,300,250,400)", "group":"group=4", "layer":"layer=7", "children":"children=[100, 101]"})
e_button = EM.load_entity("entity_button", {"position":"position=v2(310,310)", "color":"color=(74,109,145)", "rect":"rect=pygame.Rect(310,310,120,50)", "group":"group=5", "layer":"layer=3", "_id":"_id=100", "MouseMovable":"MouseMovable=0"})
e_button = EM.load_entity("entity_button", {"position":"position=v2(310,370)", "color":"color=(74,109,145)", "rect":"rect=pygame.Rect(310,370,120,50)", "group":"group=5", "layer":"layer=2", "_id":"_id=101", "MouseMovable":"MouseMovable=0"})


while _globals.running:
    #if _globals.selection is not None:
    #    print("name: %s - group: %s - layer: %s" % (_globals.selection.name, _globals.selection.group, _globals.selection.layer))
    #else:
    #    print(None)
    dt = clock.tick(fps) / 1000
    elapsed_time += dt

    screen.fill((0, 0, 0))
    RenderSystem.draw(screen)
    #ScaleSprite.update(dt)
    #TranslateSprite.update(dt)
    MovePlayer.update(dt)
    MouseMoveSprite.update()
    ParticleSystem.update(screen, dt)
    CS.update()
    SelectSystem.update()

    if pygame.event.peek(QUIT):
        pygame.quit()
        sys.exit(0)

    if console.state == CState.CLOSED:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == K_BACKQUOTE and not event.mod:
                    console.open(CState.OPEN_SMALL)
                if event.key == K_BACKQUOTE and event.mod == 1:
                    console.open(CState.OPEN_BIG)

                if event.key == K_a:
                    Controller.left = True
                if event.key == K_d:
                    Controller.right = True
                if event.key == K_w:
                    Controller.up = True
                if event.key == K_s:
                    Controller.down = True
                if event.key == K_LALT:
                    Controller.alt = True

            if event.type == KEYUP:
                if event.key == K_a:
                    Controller.left = False
                if event.key == K_d:
                    Controller.right = False
                if event.key == K_w:
                    Controller.up = False
                if event.key == K_s:
                    Controller.down = False
                if event.key == K_LALT:
                    Controller.alt = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    Controller.m1 = True
                if event.button == 3:
                    Controller.m3 = True
                if _globals.selection is not None:
                    if event.button == 5 and Controller.alt:
                        if _globals.selection.layer > 0:
                            _globals.selection.layer -= 1
                        else:
                            _globals.selection.group -= 1
                            _globals.selection.layer = 9
                        for child_id in _globals.selection.children:
                            child = EM.get(child_id)
                            if child.layer > 0:
                                child.layer -= 1
                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
                                child.text_surface = _globals.font.render(child.text, True, child.text_color)
                            else:
                                child = EM.get(child_id)
                                child.group -= 1
                                child.layer = 9
                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
                                child.text_surface = _globals.font.render(child.text, True, child.text_color)

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    Controller.m1 = False
                if event.button == 3:
                    Controller.m3 = False
                if _globals.selection is not None:
                    if event.button == 4 and Controller.alt:
                        if _globals.selection.layer < 9:
                            _globals.selection.layer += 1
                        else:
                            _globals.selection.group += 1
                            _globals.selection.layer = 0
                        for child_id in _globals.selection.children:
                            child = EM.get(child_id)
                            if child.layer < 9:
                                child.layer += 1
                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
                                child.text_surface = _globals.font.render(child.text, True, child.text_color)
                            else:
                                child = EM.get(child_id)
                                child.group += 1
                                child.layer = 0
                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
                                child.text_surface = _globals.font.render(child.text, True, child.text_color)


    console.update(dt)
    pygame.display.flip()
    pygame.display.set_caption(str(int(clock.get_fps())))
    # TODO: think of a better way to keep track of frames, this might cause an issue if it hits max size of int
    #frame += 1
