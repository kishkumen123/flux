import sys
import pygame
import _globals
import string

from pygame.locals import *
from console import Console, CState
from entity_manager import EM, load_textures
from systems import RenderSystem, ScaleSprite, TranslateSprite, MovePlayer, CS, ParticleSystem, MouseMoveSprite, SelectSystem, UIMouseMove, UIResize
from controller import Controller
from ui import UI, UIID, DUIID
from fmath import v2, v4
from events import Events


pygame.init()

fps = 250
clock = pygame.time.Clock()
frame = 0
elapsed_time = 0

width, height = 1280, 960
screen = pygame.display.set_mode((width, height))


console = Console(screen, _globals.font)
UI.screen = screen

load_textures("data/textures/*")
EM.load_entities("data/entities/*")


pygame.key.set_repeat(0,0)
while _globals.running:
    Events.set(pygame.event.get())

    dt = clock.tick(fps) / 1000
    elapsed_time += dt
    screen.fill((49, 48, 36))
    RenderSystem.draw(screen)

    if not _globals.should_ignore_input:
        for event in Events():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if console.is_open():
                pygame.key.set_repeat(400,40)
                console.handle_event(event)
            elif UI.interactive:
                pygame.key.set_repeat(400,40)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if UI.valid_input:
                            UI.interactive = 0 
                            Events.consume(event)
                    if event.key == K_RETURN:
                        if UI.valid_input:
                            UI.interactive = 0 
                            Events.consume(event)
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:
                        if not UI.hot and UI.valid_input:
                            UI.interactive = 0
                            #Events.consume(event)
                UI.handle_event(event)

            else:
                if Events.type(event, KEYDOWN):
                    if Events.key(event, K_ESCAPE):
                        pygame.quit()
                        sys.exit(0)

                    if Events.key(event, K_BACKQUOTE):
                        console.open(CState.OPEN_SMALL)
                    if Events.key(event, K_BACKQUOTE, 1):
                        console.open(CState.OPEN_BIG)

                #dont consume, only here to set controller because pygame fails to add a mod to their mouse events
                    if event.key == K_LSHIFT:
                        Controller.shift = True
                if Events.type(event, KEYUP):
                    if event.key == K_LSHIFT:
                        Controller.shift = False

    UI.do_canvas(UIID(), pygame.Rect(0, 0, 250, 400), 18, padding=v4(10,10,10,10))
    UI.do_label(UIID(), "Hot - %s" % str(UI.hot), 18)
    UI.do_label(UIID(), "Active - %s" % str(UI.active), 18)
    UI.do_label(UIID(), "Interactive - %s" % str(UI.interactive), 18)

    UI.do_canvas(UIID(), pygame.Rect(300, 300, 250, 400), 18, padding=v4(10,10,10,10))
    UI.do_label(UIID(), "Entities", 18)
    UI.do_textinput(DUIID(), 18, "")
    for e in EM.entities.values():
        if UI.do_button(DUIID(), e._id, 18, tab=True):
            _globals.selection = e

    UI.do_canvas(UIID(), pygame.Rect(1, 300, 250, 400), 18, padding=v4(10,10,10,10))
    UI.do_label(UIID(), "Data", 18)
    if _globals.selection:
        UI.do_label(UIID(), "_____________", 18)
        for label, value in _globals.selection.__dict__.items():
            if label == "sprite_source":
                UI.do_label(UIID(), value, 18)
            if label == "position":
                UI.do_label(UIID(), label, 18)
                _globals.selection.__dict__[label].x = UI.do_param(UIID(), 18, value[0], align=2)
                _globals.selection.__dict__[label].y = UI.do_param(UIID(), 18, value[1])
            if label == "scale":
                UI.do_label(UIID(), label, 18)
                _globals.selection.__dict__[label].x = UI.do_param(UIID(), 18, value[0], align=2)
                _globals.selection.__dict__[label].y = UI.do_param(UIID(), 18, value[1])


    if UI.hot_flag == 0:
        UI.hot = 0
    UI.hot_flag = 0
    UI.reset_ids()

    #ScaleSprite.update(dt)
    #TranslateSprite.update(dt)
    #MovePlayer.update(dt)
    ParticleSystem.update(screen, dt)
    #CS.update()
    SelectSystem.update()
    UIResize.update()
    UIMouseMove.update()
    MouseMoveSprite.update()
    console.update(dt)

    Events.clear()
    pygame.display.flip()
    pygame.display.set_caption(str(int(clock.get_fps())))
    # TODO(Rafik): think of a better way to keep track of frames, this might cause an issue if it hits max size of int
    #frame += 1
