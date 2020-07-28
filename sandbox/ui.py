import pygame
import _globals

from pygame.locals import *
from controller import Controller
from fmath import v2, v4


class CANVAS_ID:
    _id=1

    def __new__(cls):
        result = CANVAS_ID._id
        CANVAS_ID._id += 1
        return result

class BUTTON_ID:
    _id=1

    def __new__(cls):
        result = BUTTON_ID._id
        BUTTON_ID._id += 1
        return result

class LABEL_ID:
    _id=1

    def __new__(cls):
        result = LABEL_ID._id
        LABEL_ID._id += 1
        return result

class TEXTINPUT_ID:
    _id=1

    def __new__(cls):
        result = TEXTINPUT_ID._id
        TEXTINPUT_ID._id += 1
        return result


class Canvas:

    def __init__(self, _id, rect, font_size, padding, spacing):
        self._id=_id
        self.rect=rect
        self.mask_rect=None
        self.font_size=font_size
        self.padding=padding
        self.spacing=spacing
        self.children=0
        self.counter=0
        self.move_offset=None
        self.side_offset=None


class UI:
    hot = 0
    active = 0
    interactive = 0
    screen=None
    text=""
    text_color_light= (184, 148, 103)
    text_color_dark = (111, 93, 70)
    canvases = {}


    @classmethod
    def reset_ids(cls, exclude_canvas=False):
        if not exclude_canvas:
            CANVAS_ID._id = 1
        BUTTON_ID._id = 1
        LABEL_ID._id = 1
        TEXTINPUT_ID._id = 1

    #TODO(Rafik): make sure to figure out how to fix 2 buttons overlapping on each other
    @classmethod
    def hot_active(cls, _id, rect):
        result = False

        if rect.collidepoint(pygame.mouse.get_pos()):
            UI.hot = _id

        if UI.active == _id and not Controller.m1:
            if rect.collidepoint(pygame.mouse.get_pos()):
                result = True
            UI.hot = 0
            UI.active = 0

        elif UI.hot == _id and Controller.m1:
            if UI.active == 0: 
                UI.active = _id

        return result

    @classmethod
    def interacted(cls, _id, rect, _type):

        if rect.collidepoint(pygame.mouse.get_pos()):
            UI.hot = _id

        #print(UI.active == _id)
        #print(Controller.m1)
        #print("active %s" % UI.active)
        #print("hot %s" % UI.hot)
        print(Controller.m1 is False and UI.active)
        if UI.active == _id and not Controller.m1:
            import pdb; pdb.set_trace()
            if rect.collidepoint(pygame.mouse.get_pos()) and _type is TEXTINPUT_ID:
                if UI.interactive != _id:
                    UI.text = ""
                    UI.interactive = _id
            else:
                UI.text = ""
                UI.interactive = 0
            UI.hot = 0
            UI.active = 0

        elif UI.hot == _id and Controller.m1:
            if UI.active == 0: 
                UI.active = _id

    @classmethod
    def register_canvas(cls, _id, rect, font_size, padding, spacing):
        UI.reset_ids(True)
        if UI.canvases.get(_id) is not None:
            UI.canvases[_id].children = 0
            UI.canvases[_id].counter = 0
            return
        c = Canvas(_id, rect, font_size, padding, spacing)
        c._id += 1
        c.mask_rect = pygame.Rect(rect.x + padding[0], rect.y + padding[2], rect.w - padding[1] - padding[0], rect.h - padding[3] - padding[2])
        UI.canvases[_id] = c

    @classmethod
    def increment_counter(cls, canvas):
        canvas.counter += 1
        if canvas.counter > canvas.children:
            canvas.counter = 0

    @classmethod
    def do_canvas(cls, _id, rect, font_size, padding=v4(0,0,0,0), spacing=v2(0,0)):
        UI.register_canvas(_id, rect, font_size, padding, spacing)
        canvas = UI.canvases.get(_id)
        mask_rect = pygame.Rect(canvas.rect.x + padding[0], canvas.rect.y + padding[2], canvas.rect.w - padding[1] - padding[0], canvas.rect.h - padding[3] - padding[2])
        UI.canvases[_id].mask_rect = mask_rect

        pygame.draw.rect(UI.screen, (184, 148, 103), UI.canvases[_id].rect, 4)
        pygame.draw.rect(UI.screen, (49, 49, 47), UI.canvases[_id].rect)
        return _id

    @classmethod
    def increment_children(cls, element_id, canvas_id):
        UI.canvases[canvas_id].children += 1

    @classmethod
    def do_button(cls, _id, text, font_size, canvas_id=None, padding=v4(0,0,0,0), spacing=v2(0,0)):
        UI.increment_children(_id, canvas_id)
        canvas = UI.canvases[canvas_id]
        rect = pygame.Rect(canvas.mask_rect.x, canvas.mask_rect.y + (30 * canvas.counter), canvas.mask_rect.w, 30)

        result = UI.hot_active(_id, rect)

        border = pygame.draw.rect(UI.screen, (111, 93, 70), rect, 4)
        button = pygame.draw.rect(UI.screen, (40, 38, 36), rect)

        text_surface = _globals.font.render(text, True, (111, 93, 70))
        center_height = rect.y + (rect.h/2 - text_surface.get_height()/2)
        UI.screen.blit(text_surface, (rect.x + 5, center_height))

        UI.increment_counter(canvas)
        return result

    @classmethod
    def do_label(cls, _id, text, font_size, canvas_id=None, padding=v4(0,0,0,0), spacing=v2(0,0)):
        UI.increment_children(_id, canvas_id)
        canvas = UI.canvases[canvas_id]

        rect = pygame.Rect(canvas.mask_rect.x, canvas.mask_rect.y + (30 * canvas.counter), canvas.mask_rect.w, 30)

        text_surface = _globals.font.render(text, True, (184, 148, 103))
        center_height = canvas.mask_rect.y + (rect.h/2 - text_surface.get_height()/2)
        UI.screen.blit(text_surface, (canvas.mask_rect.x + 5, center_height + (30 * canvas.counter) + 4))

        UI.increment_counter(canvas)
        return True

    @classmethod
    def do_textinput(cls, _id, font_size, _type, canvas_id=None, padding=v4(0,0,0,0), spacing=v2(0,0)):
        UI.increment_children(_id, canvas_id)
        canvas = UI.canvases[canvas_id]
        rect = pygame.Rect(canvas.mask_rect.x, canvas.mask_rect.y + (30 * canvas.counter), canvas.mask_rect.w, 30)

        UI.interacted(_id, rect, _type)
        if UI.interactive == _id:
            text_surface = _globals.font.render(UI.text, True, UI.text_color_light)
        else:
            text_surface = _globals.font.render(UI.text, True, UI.text_color_dark)

        border = pygame.draw.rect(UI.screen, (111, 93, 70), rect, 4)
        button = pygame.draw.rect(UI.screen, (40, 38, 36), rect)

        center_height = canvas.mask_rect.y + (rect.h/2 - text_surface.get_height()/2)
        UI.screen.blit(text_surface, (canvas.mask_rect.x + 5, center_height + (30 * canvas.counter) + 4))

        UI.increment_counter(canvas)
        return True
