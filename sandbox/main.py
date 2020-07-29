import sys
import pygame
import _globals
import string

from pygame.locals import *
from console import Console, CState
from entity_manager import EM, load_textures
from systems import RenderSystem, ScaleSprite, TranslateSprite, MovePlayer, CS, ParticleSystem, MouseMoveSprite, SelectSystem, UIMouseMove, UIResize
from controller import Controller
from ui import UI, CANVAS_ID, BUTTON_ID, LABEL_ID, TEXTINPUT_ID
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
#UI.interactive = 1


#load_textures("data/textures/*")
#EM.load_entities("data/entities/*")

#e_panel = EM.load_entity("entity_6", {"position":"position=v2(300,300)", "color":"color=(70,74,71)", "rect":"rect=pygame.Rect(300,300,250,400)", "group":"group=4", "layer":"layer=7", "children":"children=[100, 101]"})
#e_button = EM.load_entity("entity_button", {"position":"position=v2(310,310)", "color":"color=(74,109,145)", "rect":"rect=pygame.Rect(310,310,120,50)", "group":"group=4", "layer":"layer=7", "_id":"_id=100", "MouseMovable":"MouseMovable=0"})
#e_button = EM.load_entity("entity_button", {"position":"position=v2(310,370)", "color":"color=(74,109,145)", "rect":"rect=pygame.Rect(310,370,120,50)", "group":"group=4", "layer":"layer=7", "_id":"_id=101", "MouseMovable":"MouseMovable=0"})



pygame.key.set_repeat(0,0)
while _globals.running:
    Events.set(pygame.event.get())

    dt = clock.tick(fps) / 1000
    elapsed_time += dt

    # systems
    screen.fill((49, 48, 36))
    RenderSystem.draw(screen)
    #ScaleSprite.update(dt)
    #TranslateSprite.update(dt)
    MovePlayer.update(dt)
    MouseMoveSprite.update()
    ParticleSystem.update(screen, dt)
    CS.update()
    SelectSystem.update()
    UIMouseMove.update()
    UIResize.update()


    if not _globals.should_ignore_input:
        for event in Events():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            #handle_global_event(event)
            if console.is_open():
                console.handle_event(event)
            if _globals.editor:
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

            #if Events.type(event, MOUSEBUTTONDOWN):
            #    if Events.button(event, 1):
            #        Controller.m1 = True
            #if Events.type(event, MOUSEBUTTONUP):
            #    if Events.button(event, 1):
            #        Controller.m1 = False


    #if console.state == CState.CLOSED:
    #for event in pygame.event.get():
    #    if console.state != CState.CLOSED:
    #        console.read_events(event)
    #    elif UI.interactive:
    #        UI.read_events(event)
    #    else:

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

    #        if event.type == MOUSEBUTTONDOWN:
    #            if event.button == 1:
    #                Controller.m1 = True
    #            if event.button == 3:
    #                Controller.m3 = True
    #            if _globals.selection is not None:
    #                if event.button == 5 and Controller.alt:
    #                    if _globals.selection.layer > 0:
    #                        _globals.selection.layer -= 1
    #                    else:
    #                        _globals.selection.group -= 1
    #                        _globals.selection.layer = 9
    #                    for child_id in _globals.selection.children:
    #                        child = EM.get(child_id)
    #                        if child.layer > 0:
    #                            child.layer -= 1
    #                            if child.text is not None:
    #                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
    #                                child.text_surface = _globals.font.render(child.text, True, child.text_color)
    #                        else:
    #                            child = EM.get(child_id)
    #                            child.group -= 1
    #                            child.layer = 9
    #                            if child.text is not None:
    #                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
    #                                child.text_surface = _globals.font.render(child.text, True, child.text_color)

    #        if event.type == MOUSEBUTTONUP:
    #            if event.button == 1:
    #                Controller.m1 = False
    #            if event.button == 3:
    #                Controller.m3 = False
    #            if _globals.selection is not None:
    #                if event.button == 4 and Controller.alt:
    #                    if _globals.selection.layer < 9:
    #                        _globals.selection.layer += 1
    #                    else:
    #                        _globals.selection.group += 1
    #                        _globals.selection.layer = 0
    #                    for child_id in _globals.selection.children:
    #                        child = EM.get(child_id)
    #                        if child.layer < 9:
    #                            child.layer += 1
    #                            if child.text is not None:
    #                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
    #                                child.text_surface = _globals.font.render(child.text, True, child.text_color)
    #                        else:
    #                            child = EM.get(child_id)
    #                            child.group += 1
    #                            child.layer = 0
    #                            if child.text is not None:
    #                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
    #                                child.text_surface = _globals.font.render(child.text, True, child.text_color)


    #print(UI.interactive)
    print("hot %s" % UI.hot)
    print("active %s" % UI.active)
    UI.reset_ids()
    canvas_id = UI.do_canvas(CANVAS_ID(), pygame.Rect(300, 300, 250, 400), 18, padding=v4(10,10,10,10))
    if UI.do_button(BUTTON_ID(), "button17", 18, canvas_id):
        print("1")
    if UI.do_button(BUTTON_ID(), "button2", 18, canvas_id):
        print("2")
    UI.do_label(LABEL_ID(), "Label1", 18, canvas_id)
    UI.do_label(LABEL_ID(), "Label1", 18, canvas_id)
    if UI.do_button(BUTTON_ID(), "button3", 18, canvas_id):
        print("3")
    if UI.do_button(BUTTON_ID(), "button4", 18, canvas_id):
        print("4")
    if UI.do_button(BUTTON_ID(), "button5", 18, canvas_id):
        print("5")
    #UI.do_textinput(TEXTINPUT_ID(), 18, TEXTINPUT_ID, canvas_id)

    canvas_id = UI.do_canvas(CANVAS_ID(), pygame.Rect(1, 300, 250, 400), 18, padding=v4(10,10,10,10))
    if UI.do_button(BUTTON_ID(), "button1", 18, canvas_id):
        print("1")
    if UI.do_button(BUTTON_ID(), "button2", 18, canvas_id):
        print("2")
    if UI.do_button(BUTTON_ID(), "button3", 18, canvas_id):
        print("3")
    if UI.do_button(BUTTON_ID(), "button4", 18, canvas_id):
        print("4")
    if UI.do_button(BUTTON_ID(), "button5", 18, canvas_id):
        print("5")
    if UI.do_button(BUTTON_ID(), "button6", 18, canvas_id):
        print("6")
    UI.do_label(LABEL_ID(), "Label1", 18, canvas_id)
    if UI.do_button(BUTTON_ID(), "button6", 18, canvas_id):
        print("7")
    UI.do_label(LABEL_ID(), "Label1", 18, canvas_id)
    if UI.do_button(BUTTON_ID(), "button7", 18, canvas_id):
        print("8")

    console.update(dt)
    Events.clear()
    pygame.display.flip()
    pygame.display.set_caption(str(int(clock.get_fps())))

    if UI.hot_flag == 0:
        UI.hot = 0
    UI.hot_flag = 0
    # TODO(Rafik): think of a better way to keep track of frames, this might cause an issue if it hits max size of int
    #frame += 1
