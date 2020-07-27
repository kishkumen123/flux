import pygame
import _globals

from pygame.locals import *
from controller import Controller
from fmath import v2, v4



class Canvas:

    def __init__(self):
        self._id=None
        self.rect=None
        self.mask_rect=None
        self.text=None
        self.font_size=None
        self.padding=None
        self.spacing=None
        self.children=0
        self.counter=0
        self.move_offset=None
        self.side_offset=None


class UI:
    hot = 0
    active = 0
    canvases = {}

    #TODO(Rafik): make sure to figure out how to fix 2 buttons overlapping on each other
    @classmethod
    def hot_active(cls, _id, rect):
        result = False

        if UI.active == _id and not Controller.m1:
            if rect.collidepoint(pygame.mouse.get_pos()):
                result = True
            UI.hot = 0
            UI.active = 0

        elif UI.hot == _id and Controller.m1:
            if UI.active == 0: 
                UI.active = _id

        if rect.collidepoint(pygame.mouse.get_pos()):
            UI.hot = _id

        return result

    @classmethod
    def register_canvas(cls, _id, rect, mask_rect, text, font_size, padding, spacing):
        if UI.canvases.get(_id) is not None:
            UI.canvases[_id].children = 0
            return
        c = Canvas()
        c._id = _id
        c.text = text
        c.font_size = font_size
        c.padding = padding
        c.spacing = spacing
        c.rect = rect
        c.mask_rect = mask_rect
        c.rect = rect
        c.mask_rect = mask_rect
        UI.canvases[_id] = c

    @classmethod
    def increment_counter(cls, canvas):
        canvas.counter += 1
        if canvas.counter > canvas.children:
            canvas.counter = 0

    @classmethod
    def do_canvas(cls, screen, _id, rect, text, font_size, padding=v4(0,0,0,0), spacing=v2(0,0)):
        canvas = UI.canvases.get(_id)
        if canvas:
            mask_rect = pygame.Rect(canvas.rect.x + padding[0], canvas.rect.y + padding[2], canvas.rect.w - padding[1] - padding[0], canvas.rect.h - padding[3] - padding[2])
            UI.canvases[_id].mask_rect = mask_rect
            #UI.register_canvas(_id, UI.canvases[_id].rect, mask_rect, text, font_size, padding, spacing)
        else:
            mask_rect = pygame.Rect(rect.x + padding[0], rect.y + padding[2], rect.w - padding[1] - padding[0], rect.h - padding[3] - padding[2])
        UI.register_canvas(_id, rect, mask_rect, text, font_size, padding, spacing)

        #mask_rect = pygame.Rect(rect.x + padding[0], rect.y + padding[2], rect.w - padding[1] - padding[0], rect.h - padding[3] - padding[2])
        #UI.register_canvas(_id, rect, mask_rect, text, font_size, padding, spacing)
        pygame.draw.rect(screen, (184, 148, 103), UI.canvases[_id].rect, 4)
        pygame.draw.rect(screen, (49, 49, 47), UI.canvases[_id].rect)
        return True

    @classmethod
    def register_canvas_element(cls, element_id, canvas_id):
        UI.canvases[canvas_id].children += 1

    @classmethod
    def do_button(cls, screen, _id, text, font_size, canvas_id=None, rect=pygame.Rect(0,0,0,0), padding=v4(0,0,0,0), spacing=v2(0,0)):
        UI.register_canvas_element(_id, canvas_id)
        canvas = UI.canvases[canvas_id]

        rect.x = canvas.mask_rect.x 
        rect.w = canvas.mask_rect.w
        rect.h = 30
        rect.y = canvas.mask_rect.y + (rect.h * canvas.counter)
        result = UI.hot_active(_id, rect)

        border = pygame.draw.rect(screen, (111, 93, 70), rect, 4)
        button = pygame.draw.rect(screen, (40, 38, 36), rect)

        text_surface = _globals.font.render(text, True, (111, 93, 70))
        center_height = rect.y + (rect.h/2 - text_surface.get_height()/2)
        screen.blit(text_surface, (rect.x + 5, center_height))

        UI.increment_counter(canvas)
        return result

    @classmethod
    def do_text(cls, screen, _id, text, font_size, canvas_id=None, rect=pygame.Rect(0,0,0,0), padding=v4(0,0,0,0), spacing=v2(0,0)):
        UI.register_canvas_element(_id, canvas_id)
        canvas = UI.canvases[canvas_id]

        rect.x = canvas.mask_rect.x 
        rect.w = canvas.mask_rect.w
        rect.h = 30
        rect.y = canvas.mask_rect.y + (rect.h * canvas.counter)

        text_surface = _globals.font.render(text, True, (184, 148, 103))
        center_height = canvas.mask_rect.y + (rect.h/2 - text_surface.get_height()/2)
        screen.blit(text_surface, (canvas.mask_rect.x + 5, center_height + (30 * canvas.counter) + 4))

        UI.increment_counter(canvas)

        return True
