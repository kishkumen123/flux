import sys
import pygame
import _globals
from pygame.locals import *
from console import C, CState

from entity_manager import EM, register_components, init_groups, load_entities
from components import components_list
from systems import RenderSystem, ScaleSprite, TranslateSprite
from sprite_groups import sprite_groups
 
pygame.init()
 
fps = 120
clock = pygame.time.Clock()
frame = 0
elapsed_time = 0
 
width, height = 1024, 720
screen = pygame.display.set_mode((width, height))

pygame.font.init()
font = pygame.font.SysFont("consolas", 18)

c = C(screen, font)


register_components(components_list)
init_groups("resources/data/groups.json")
load_entities("resources/data/entities.json")

while _globals.running:
    dt = clock.tick(fps) / 1000
    elapsed_time += dt

    screen.fill((0, 0, 0))
    RenderSystem.update()
    RenderSystem.draw(screen)
    TranslateSprite.update(dt)
    ScaleSprite.update(dt)

    if pygame.event.peek(QUIT):
        pygame.quit()
        sys.exit(0)

    if c.state == CState.CLOSED:
        if pygame.event.peek(KEYDOWN):
            event = pygame.event.get(pygame.KEYDOWN)[0]
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            if event.key == K_BACKQUOTE and not event.mod:
                c.open(CState.OPEN_SMALL)
            if event.key == K_BACKQUOTE and event.mod:
                c.open(CState.OPEN_BIG)

    c.update(dt)
    pygame.event.get()
    pygame.display.flip()
    # TODO: think of a better way to keep track of frames, this might cause an issue if it hits max size of int
    #frame += 1
