import sys
import pygame
import _globals
import string

from pygame.locals import *
from console import Console, CState
from entity_manager import EM, load_textures
from systems import RenderSystem, ScaleSprite, TranslateSprite, MovePlayer, CS, ParticleSystem, MouseMoveSprite, SelectSystem, UIMouseMove, UIResize
from controller import Controller
from ui import UI, UIID
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
            #handle_global_event(event)
            if console.is_open():
                console.handle_event(event)
            elif UI.interactive:
                UI.handle_event(event)
            else:
                if Events.type(event, KEYDOWN):
                    if Events.key(event, K_ESCAPE):
                        pygame.quit()
                        sys.exit(0)

                    if Events.key(event, K_BACKQUOTE):
                        console.open(CState.OPEN_SMALL)
                        pygame.key.set_repeat(400,40)
                    if Events.key(event, K_BACKQUOTE, 1):
                        pygame.key.set_repeat(400,40)
                        console.open(CState.OPEN_BIG)
                    #dont consume, only here to set controller because pygame fails to add a mod to their mouse events
                    if event.key == K_LSHIFT:
                        Controller.shift = True
                if Events.type(event, KEYUP):
                    #dont consume, only here to set controller because pygame fails to add a mod to their mouse events
                    if event.key == K_LSHIFT:
                        Controller.shift = False

            #if Events.type(event, MOUSEBUTTONDOWN):
            #    if Events.button(event, 1):
            #        Controller.m1 = True
            #if Events.type(event, MOUSEBUTTONUP):
            #    if Events.button(event, 1):
            #        Controller.m1 = False

    #            if event.key == K_a:
    #                Controller.left = True
    #            if event.key == K_d:
    #                Controller.right = True
    #            if event.key == K_w:
    #                Controller.up = True
    #            if event.key == K_s:
    #                Controller.down = True
    #            if event.key == K_LALT:
    #                Controller.alt = True
    #            if event.key == K_LSHIFT:
    #                Controller.shift = True

    #        if event.type == KEYUP:
    #            if event.key == K_a:
    #                Controller.left = False
    #            if event.key == K_d:
    #                Controller.right = False
    #            if event.key == K_w:
    #                Controller.up = False
    #            if event.key == K_s:
    #                Controller.down = False
    #            if event.key == K_LALT:
    #                Controller.alt = False
    #            if event.key == K_LSHIFT:
    #                Controller.shift = False


    #canvas_id = UI.do_canvas(UIID(), pygame.Rect(300, 300, 250, 400), 18, padding=v4(10,10,10,10))
    #if UI.do_button(UIID(), "button17", 18, canvas_id):
    #    print("1")
    #if UI.do_button(UIID(), "button2", 18, canvas_id):
    #    print("2")
    #UI.do_label(UIID(), "Label1", 18, canvas_id)
    #UI.do_label(UIID(), "Label1", 18, canvas_id)
    #if UI.do_button(UIID(), "button3", 18, canvas_id):
    #    print("3")
    #if UI.do_button(UIID(), "button4", 18, canvas_id):
    #    print("4")
    #if UI.do_button(UIID(), "button5", 18, canvas_id):
    #    print("5")
    #UI.do_textinput(UIID(), 18, canvas_id)
    #UI.do_textinput(UIID(), 18, canvas_id)
    #UI.do_textinput(UIID(), 18, canvas_id)
    #UI.do_textinput(UIID(), 18, canvas_id)

    #import pdb; pdb.set_trace()
    canvas_id = UI.do_canvas(UIID(), pygame.Rect(300, 300, 250, 400), 18, padding=v4(10,10,10,10))
    print(len(EM.entities.values()))
    for e in EM.entities.values():
        if UI.do_button(UIID(), e._id, 18, canvas_id, tab=True):
            print(e._id)

    canvas = UI.get_canvas(canvas_id)
    if canvas.selected_element is not None:
        e = EM.get(canvas.selected_element)
        _globals.selection = e

    canvas_id = UI.do_canvas(UIID(), pygame.Rect(1, 300, 250, 400), 18, padding=v4(10,10,10,10))
    if _globals.selection:
        for label, value in _globals.selection.__dict__.items():
            if label == "sprite_source":
                UI.do_label(UIID(), value, 18, canvas_id)
            if label == "position":
                UI.do_label(UIID(), label, 18, canvas_id)
                _globals.selection.__dict__[label].x = UI.do_param(UIID(), 18, value[0], canvas_id, align=2)
                _globals.selection.__dict__[label].y = UI.do_param(UIID(), 18, value[1], canvas_id)
            if label == "scale":
                UI.do_label(UIID(), label, 18, canvas_id)
                _globals.selection.__dict__[label].x = UI.do_param(UIID(), 18, value[0], canvas_id, align=2)
                _globals.selection.__dict__[label].y = UI.do_param(UIID(), 18, value[1], canvas_id)

    #UI.do_label(UIID(), "Name", 18, canvas_id)
    #UI.do_label(UIID(), "Position", 18, canvas_id)
    #UI.do_textinput(UIID(), 18, canvas_id, "100", align=3)
    #UI.do_textinput(UIID(), 18, canvas_id, "200")
    #UI.do_textinput(UIID(), 18, canvas_id, "300")
    #UI.do_label(UIID(), "Velocity", 18, canvas_id)
    #UI.do_textinput(UIID(), 18, canvas_id, "10", align=3)
    #UI.do_textinput(UIID(), 18, canvas_id, "50")
    #UI.do_textinput(UIID(), 18, canvas_id, "20")
    #UI.do_label(UIID(), "Scale", 18, canvas_id)
    #UI.do_textinput(UIID(), 18, canvas_id, "10", align=2)
    #UI.do_textinput(UIID(), 18, canvas_id, "20")

    #canvas_id = UI.do_canvas(UIID(), pygame.Rect(500, 100, 250, 400), 18, padding=v4(10,10,10,10))
    #if _globals.selection is not None:
    #    for item in _globals.selection.__dict__.items():
    #        UI.do_button(UIID(), str(item), 18, canvas_id)

    if UI.hot_flag == 0:
        UI.hot = 0
    UI.hot_flag = 0
    UI.reset_ids()

    #ScaleSprite.update(dt)
    #TranslateSprite.update(dt)
    #MovePlayer.update(dt)
    #ParticleSystem.update(screen, dt)
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
