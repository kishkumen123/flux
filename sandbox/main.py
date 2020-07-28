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


pygame.init()

fps = 250
clock = pygame.time.Clock()
frame = 0
elapsed_time = 0

width, height = 1280, 960
screen = pygame.display.set_mode((width, height))


console = Console(screen, _globals.font)
UI.screen = screen
UI.interactive = 1


#load_textures("data/textures/*")
#EM.load_entities("data/entities/*")

#e_panel = EM.load_entity("entity_6", {"position":"position=v2(300,300)", "color":"color=(70,74,71)", "rect":"rect=pygame.Rect(300,300,250,400)", "group":"group=4", "layer":"layer=7", "children":"children=[100, 101]"})
#e_button = EM.load_entity("entity_button", {"position":"position=v2(310,310)", "color":"color=(74,109,145)", "rect":"rect=pygame.Rect(310,310,120,50)", "group":"group=4", "layer":"layer=7", "_id":"_id=100", "MouseMovable":"MouseMovable=0"})
#e_button = EM.load_entity("entity_button", {"position":"position=v2(310,370)", "color":"color=(74,109,145)", "rect":"rect=pygame.Rect(310,370,120,50)", "group":"group=4", "layer":"layer=7", "_id":"_id=101", "MouseMovable":"MouseMovable=0"})


while _globals.running:
    text = ""
    #if _globals.selection is not None:
    #    print("name: %s - group: %s - layer: %s" % (_globals.selection.name, _globals.selection.group, _globals.selection.layer))
    #else:
    #    print(None)
    dt = clock.tick(fps) / 1000
    elapsed_time += dt

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

    if pygame.event.peek(QUIT):
        pygame.quit()
        sys.exit(0)

    

    if console.state == CState.CLOSED:
        for event in pygame.event.get():
            if UI.interactive:
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        UI.interactive = 0
                    if event.key == K_RETURN:
                        UI.interactive = 0
                    if event.key == K_BACKSPACE:
                        UI.text = UI.text[:-1]
                    textinput_list = string.digits + string.ascii_letters + string.punctuation + " "
                    textinput_list = textinput_list.replace("`", "")
                    textinput_list = textinput_list.replace("~", "")
                    if event.unicode in textinput_list and event.unicode != "":
                        UI.text += event.unicode
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

            else:
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
                    if event.key == K_LSHIFT:
                        Controller.shift = True

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
                    if event.key == K_LSHIFT:
                        Controller.shift = False

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
                                    if child.text is not None:
                                        child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
                                        child.text_surface = _globals.font.render(child.text, True, child.text_color)
                                else:
                                    child = EM.get(child_id)
                                    child.group -= 1
                                    child.layer = 9
                                    if child.text is not None:
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
                                    if child.text is not None:
                                        child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
                                        child.text_surface = _globals.font.render(child.text, True, child.text_color)
                                else:
                                    child = EM.get(child_id)
                                    child.group += 1
                                    child.layer = 0
                                    if child.text is not None:
                                        child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
                                        child.text_surface = _globals.font.render(child.text, True, child.text_color)


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
    UI.do_textinput(TEXTINPUT_ID(), 18, TEXTINPUT_ID, canvas_id)

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
    pygame.display.flip()
    pygame.display.set_caption(str(int(clock.get_fps())))
    # TODO(Rafik): think of a better way to keep track of frames, this might cause an issue if it hits max size of int
    #frame += 1
