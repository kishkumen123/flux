import sys
import pygame
import _globals
from pygame.locals import *
from console import Console, CState

from entity_manager import EM, load_entities, load_textures
from components import components_list
from systems import RenderSystem, ScaleSprite, TranslateSprite, MovePlayer, CS, ParticleSystem, MouseMoveSprite
from sprite_groups import sprite_groups
from controller import Controller
 

pygame.init()
 
fps = 250
clock = pygame.time.Clock()
frame = 0
elapsed_time = 0
 
width, height = 1024, 720
screen = pygame.display.set_mode((width, height))

pygame.font.init()
font = pygame.font.SysFont("consolas", 18)

console = Console(screen, font)


#register_components(components_list)
#init_groups("resources/data/groups.json")
load_entities("resources/data/entities/*")
load_textures("resources/data/textures/*")


while _globals.running:
    dt = clock.tick(fps) / 1000
    elapsed_time += dt

    screen.fill((0, 0, 0))
    RenderSystem.draw(screen)
    #MovePlayer.update(dt)
    #TranslateSprite.update(dt)
    ScaleSprite.update(dt)
    #CS.update()
    #ParticleSystem.update(screen, dt)
    #MouseMoveSprite.update()

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

            if event.type == KEYUP:
                if event.key == K_a:
                    Controller.left = False
                if event.key == K_d:
                    Controller.right = False
                if event.key == K_w:
                    Controller.up = False
                if event.key == K_s:
                    Controller.down = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    Controller.m1 = True
                if event.button == 3:
                    Controller.m3 = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    Controller.m1 = False
                if event.button == 3:
                    Controller.m3 = False


    console.update(dt)
    pygame.display.flip()
    pygame.display.set_caption(str(int(clock.get_fps())))
    # TODO: think of a better way to keep track of frames, this might cause an issue if it hits max size of int
    #frame += 1
