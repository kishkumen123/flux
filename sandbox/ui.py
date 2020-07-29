import pygame
import _globals

from pygame.locals import *
from fmath import v2, v4
from events import Events


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
        self.stored_text = {}


class UI:
    hot = 0
    active = 0
    hot_flag = 0
    ihot = 0
    iactive = 0
    interactive = 0
    screen=None
    text_input=""
    text_color_light= (184, 148, 103)
    text_color_dark = (111, 93, 70)
    canvases = {}
    event = None

    @classmethod
    def handle_event(cls, event):
        pass

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
            UI.hot_flag = 1

        if UI.active == _id and Events.mbutton_up(1):
            if rect.collidepoint(pygame.mouse.get_pos()):
                result = True
            UI.hot = 0
            UI.hot_flag = 0
            UI.active = 0

        elif UI.hot == _id and Events.mbutton_down(1):
            if UI.active == 0: 
                UI.active = _id

        return result

    @classmethod
    def mouse_up(cls):
        for event in Events():
            if Events.type(event, MOUSEBUTTONUP):
                if Events.button(event, 1):
                    return True
        return False

    @classmethod
    def mouse_down(cls):
        for event in Events():
            if Events.type(event, MOUSEBUTTONDOWN):
                if Events.button(event, 1):
                    return True
        return False

    @classmethod
    def ihot_active(cls, _id, rect, _type):

        if rect.collidepoint(pygame.mouse.get_pos()):
            UI.ihot = _id

        if UI.iactive == _id and cls.mouse_up():
            if rect.collidepoint(pygame.mouse.get_pos()) and _type is TEXTINPUT_ID:
                if UI.interactive != _id:
                    #UI.text = ""
                    UI.interactive = _id
            else:
                #UI.text = ""
                UI.interactive = 0
            UI.ihot = 0
            UI.iactive = 0

        elif UI.ihot == _id and cls.mouse_down():
            if UI.iactive == 0: 
                UI.iactive = _id

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
    def increment_children(cls, element_id, canvas_id):
        UI.canvases[canvas_id].children += 1

    @classmethod
    def do_canvas(cls, _id, rect, font_size, padding=v4(0,0,0,0), spacing=v2(0,0)):
        UI.register_canvas(_id, rect, font_size, padding, spacing)
        canvas = UI.canvases.get(_id)
        UI.canvases[_id].mask_rect = pygame.Rect(canvas.rect.x + padding[0], canvas.rect.y + padding[2], canvas.rect.w - padding[1] - padding[0], canvas.rect.h - padding[3] - padding[2])

        pygame.draw.rect(UI.screen, (184, 148, 103), UI.canvases[_id].rect, 4)
        pygame.draw.rect(UI.screen, (49, 49, 47), UI.canvases[_id].rect)
        return _id

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

        UI.ihot_active(_id, rect, _type)

        #if UI.interactive == _id:
        #if self.event is not None:
        #    if self.event.type == KEYDOWN:
        #        if event.key == K_ESCAPE:
        #            UI.interactive = 0
        #        if event.key == K_RETURN:
        #            UI.interactive = 0
        #        if event.key == K_BACKSPACE:
        #            UI.text = UI.text[:-1]
        #        textinput_list = string.digits + string.ascii_letters + string.punctuation + " "
        #        textinput_list = textinput_list.replace("`", "")
        #        textinput_list = textinput_list.replace("~", "")
        #        if event.unicode in textinput_list and event.unicode != "":
        #            UI.text_input = event.unicode

        #if UI.interactive == 0:
        #    if canvas.stored_text.get(_id):
        #        text = canvas.stored_text[_id]
        #    else:
        #        text = ""

        #if UI.interactive == _id:
        #    canvas.stored_text[_id] += UI.text_input
        #    text_surface = _globals.font.render(canvas.stored_text[_id], True, UI.text_color_light)
        #else:
        #    text_surface = _globals.font.render(canvas.stored_text[_id], True, UI.text_color_dark)

        border = pygame.draw.rect(UI.screen, (111, 93, 70), rect, 4)
        button = pygame.draw.rect(UI.screen, (40, 38, 36), rect)

        center_height = canvas.mask_rect.y + (rect.h/2 - text_surface.get_height()/2)
        UI.screen.blit(text_surface, (canvas.mask_rect.x + 5, center_height + (30 * canvas.counter) + 4))

        UI.increment_counter(canvas)
        return True
