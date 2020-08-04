import pygame
import _globals

from pygame.locals import *
from fmath import v2, v4
from events import Events
from controller import Controller
from _globals import textinput_list


class UIID:
    _id=1

    def __new__(cls):
        result = cls._id
        cls._id += 1
        return result

class DUIID:
    _id=1

    def __new__(cls):
        result = cls._id
        cls._id += 1
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
        self.size_y=30
        self.move_offset=None
        self.side_offset=None
        self.right_offset=None
        self.bottom_offset=None
        self.stored_text = {}
        self.selected_element = None


class UI:
    hot = 0
    active = 0
    hot_flag = 0
    interactive = 0
    valid_input=False
    cc_id=None
    screen=None

    text_color_bright= (184, 148, 103)
    text_color_dim = (111, 93, 70)
    color_red = (139, 45, 21)

    canvases = {}
    text_dict = {}

    align_amount = None
    align_counter = None
    align_width = None

    @classmethod
    def get_canvas(cls, _id):
        return cls.canvases[_id]

    @classmethod
    def handle_event(cls, event):
        text = cls.text_dict.get(cls.interactive)

        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                text = text[:-1]
                cls.text_dict[cls.interactive] = text
                Events.consume(event)

        if event.type == TEXTINPUT:
            text += event.text
            cls.text_dict[cls.interactive] = text
            Events.consume(event)

    @classmethod
    def reset_ids(cls):
        UIID._id = 1
        DUIID._id = 1
        cls.cc_id = None

    #TODO(Rafik): make sure to figure out how to fix 2 buttons overlapping on each other
    @classmethod
    def hot_active(cls, _id, rect):
        result = False

        #if _id == 3:
            #print("hot flag %s" % cls.hot_flag)
        if rect.collidepoint(pygame.mouse.get_pos()):
            #if _id == 3:
                #print("YES")
            UI.hot = _id
            UI.hot_flag = 1
        #else:
            #if _id == 3:
                #print("NOT")

        if UI.active == _id:
            print(1)
            for event in Events():
                print(2)
                if event.type == MOUSEBUTTONUP and not Controller.shift:
                    print(3)
                    if event.button == 1:
                        print(4)
                        #import pdb; pdb.set_trace()
                        if rect.collidepoint(pygame.mouse.get_pos()):
                            print(5)
                            result = True
                        UI.hot = 0
                        UI.hot_flag = 0
                        UI.active = 0
                        Events.consume(event)

        elif UI.hot == _id:
            for event in Events():
                if event.type == MOUSEBUTTONDOWN and not Controller.shift:
                    if event.button == 1:
                        if UI.active == 0: 
                            UI.active = _id
                            Events.consume(event)
        return result

    @classmethod
    def register_canvas(cls, _id, rect, font_size, padding, spacing):
        cls.cc_id = _id

        if UI.canvases.get(_id) is None:
            c = Canvas(_id, rect, font_size, padding, spacing)
            c._id += 1
            c.mask_rect = pygame.Rect(rect.x + padding[0], rect.y + padding[2], rect.w - padding[1] - padding[0], rect.h - padding[3] - padding[2])
            UI.canvases[_id] = c
        else:	
            UI.canvases[_id].children = 0
            UI.canvases[_id].counter = 0

    @classmethod
    def increment_counter(cls, canvas):
        canvas.counter += 1
        if canvas.counter > canvas.children:
            canvas.counter = 0

    @classmethod
    def increment_children(cls, _id):
        UI.canvases[_id].children += 1
        cls.adjust_canvas(_id)

    @classmethod
    def adjust_canvas(cls, _id):
        canvas = cls.canvases[_id]
        cls.canvases[_id].rect.h = (canvas.children * canvas.size_y) + canvas.padding[0] + canvas.padding[2]

    @classmethod
    def do_canvas(cls, _id, rect, font_size, padding=v4(0,0,0,0), spacing=v2(0,0)):
        UI.register_canvas(_id, rect, font_size, padding, spacing)
        canvas = UI.canvases.get(_id)
        UI.canvases[_id].mask_rect = pygame.Rect(canvas.rect.x + padding[0], canvas.rect.y + padding[2], canvas.rect.w - padding[1] - padding[0], canvas.rect.h - padding[3] - padding[2])

        border = pygame.draw.rect(UI.screen, (184, 148, 103), UI.canvases[_id].rect, 4)
        canvas = pygame.draw.rect(UI.screen, (49, 49, 47), UI.canvases[_id].rect)
        #mask = pygame.draw.rect(UI.screen, UI.text_color_dim, UI.canvases[_id].mask_rect)
        return _id

    @classmethod
    def do_button(cls, _id, text, font_size, tab=False, align=None):
        UI.increment_children(cls.cc_id)
        canvas = UI.canvases[cls.cc_id]
        rect = pygame.Rect(canvas.mask_rect.x, canvas.mask_rect.y + (canvas.size_y * canvas.counter), canvas.mask_rect.w, canvas.size_y)

        print(_id)
        result = UI.hot_active(_id, rect)


        #if text == 4:
            #print(result)
        if result:
            if tab:
                canvas.selected_element = _id

        if UI.active == _id or canvas.selected_element == _id:
            border = pygame.draw.rect(UI.screen, UI.text_color_bright, rect, 4)
            text_surface = _globals.font.render(str(text), True, UI.text_color_bright)
        else:
            border = pygame.draw.rect(UI.screen, UI.text_color_dim, rect, 4)
            text_surface = _globals.font.render(str(text), True, UI.text_color_dim)
        button = pygame.draw.rect(UI.screen, (40, 38, 36), rect)

        center_width = rect.x + (rect.w/2 - text_surface.get_width()/2)
        center_height = rect.y + (rect.h/2 - text_surface.get_height()/2)
        UI.screen.blit(text_surface, (center_width, center_height))

        if align is None:
            UI.increment_counter(canvas)
        return result

    @classmethod
    def do_label(cls, _id, text, font_size):
        UI.increment_children(cls.cc_id)
        canvas = UI.canvases[cls.cc_id]

        rect = pygame.Rect(canvas.mask_rect.x, canvas.mask_rect.y + (canvas.size_y * canvas.counter), canvas.mask_rect.w, canvas.size_y)

        text_surface = _globals.font.render(str(text), True, (184, 148, 103))
        center_height = canvas.mask_rect.y + (rect.h/2 - text_surface.get_height()/2)
        UI.screen.blit(text_surface, (canvas.mask_rect.x + 5, center_height + (canvas.size_y * canvas.counter) + 4))

        UI.increment_counter(canvas)
        return True

    @classmethod
    def do_textinput(cls, _id, font_size, _text="", align=None):
        UI.increment_children(cls.cc_id)
        canvas = UI.canvases[cls.cc_id]
        if align:
            cls.align_amount = align
            cls.align_counter = 0
            cls.align_width = canvas.mask_rect.w / align

        if cls.align_amount:
            rect = pygame.Rect(canvas.mask_rect.x + cls.align_counter * cls.align_width, canvas.mask_rect.y + (canvas.size_y * canvas.counter), cls.align_width - 10, canvas.size_y)
        else:
            rect = pygame.Rect(canvas.mask_rect.x, canvas.mask_rect.y + (canvas.size_y * canvas.counter), canvas.mask_rect.w, canvas.size_y)

        if _id not in cls.text_dict.keys():
            cls.text_dict[_id] = _text
        text = cls.text_dict[_id]

        result = UI.hot_active(_id, rect)
        if result:
            UI.interactive = _id

        if UI.interactive == _id:
            cls.valid_input = True
            text_surface = _globals.font.render(text, True, UI.text_color_bright)
            border = pygame.draw.rect(UI.screen, UI.text_color_bright, rect, 4)
        else:
            text_surface = _globals.font.render(text, True, UI.text_color_dim)
            border = pygame.draw.rect(UI.screen, UI.text_color_dim, rect, 4)
        button = pygame.draw.rect(UI.screen, (40, 38, 36), rect)

        center_height = canvas.mask_rect.y + (rect.h/2 - text_surface.get_height()/2)
        if cls.align_amount:
            UI.screen.blit(text_surface, (canvas.mask_rect.x + 5 + cls.align_counter * cls.align_width, center_height + (canvas.size_y * canvas.counter)))

            cls.align_counter += 1
            if cls.align_counter == cls.align_amount:
                cls.align_amount = None
                cls.align_counter = None
                cls.align_width = None

        else:
            UI.screen.blit(text_surface, (canvas.mask_rect.x + 5, center_height + (canvas.size_y * canvas.counter)))

        UI.text_dict[_id] = text
        if not cls.align_amount:
            UI.increment_counter(canvas)
        return True

    @classmethod
    def do_param(cls, _id, font_size, value, align=None):
        UI.increment_children(cls.cc_id)
        canvas = UI.canvases[cls.cc_id]
        if align:
            cls.align_amount = align
            cls.align_counter = 0
            cls.align_width = canvas.mask_rect.w / align

        if cls.align_amount:
            rect = pygame.Rect(canvas.mask_rect.x + cls.align_counter * cls.align_width, canvas.mask_rect.y + (canvas.size_y * canvas.counter), cls.align_width - 10, canvas.size_y)
        else:
            rect = pygame.Rect(canvas.mask_rect.x, canvas.mask_rect.y + (canvas.size_y * canvas.counter), canvas.mask_rect.w, canvas.size_y)

        text = ""
        value_type = type(value)
        color = UI.text_color_dim

        result = UI.hot_active(_id, rect)
        if result:
            if not UI.interactive:
                UI.interactive = _id
            if UI.interactive and cls.valid_input:
                UI.interactive = _id

        if UI.interactive == _id:
            if _id not in cls.text_dict.keys():
                text = str(value)
                cls.text_dict[_id] = text
            else:
                text = cls.text_dict[_id]

            try:
                value_type(text)
                color = UI.text_color_bright
                cls.valid_input = True
            except:
                color = UI.color_red
                cls.valid_input = False

            text_surface = _globals.font.render(text, True, color)
        else:
            if _id in cls.text_dict.keys():
                value = value_type(cls.text_dict[_id])
                del cls.text_dict[_id]
            color = UI.text_color_dim
            text_surface = _globals.font.render(str(value), True, color)

        border = pygame.draw.rect(UI.screen, color, rect, 4)
        button = pygame.draw.rect(UI.screen, (40, 38, 36), rect)

        center_height = canvas.mask_rect.y + (rect.h/2 - text_surface.get_height()/2)
        if cls.align_amount:
            UI.screen.blit(text_surface, (canvas.mask_rect.x + 5 + cls.align_counter * cls.align_width, center_height + (canvas.size_y * canvas.counter)))

            cls.align_counter += 1
            if cls.align_counter == cls.align_amount:
                cls.align_amount = None
                cls.align_counter = None
                cls.align_width = None

        else:
            UI.screen.blit(text_surface, (canvas.mask_rect.x + 5, center_height + (canvas.size_y * canvas.counter)))

        if not cls.align_amount:
            UI.increment_counter(canvas)
        return value
