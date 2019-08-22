import pygame
from events import Events
from screen import Display


class Mouse:

    MOUSEMOTION = pygame.MOUSEMOTION
    MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
    MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
    MOUSEBUTTON = {
        1: False,
        3: False,
        2: False,
    }

    EVENTS = []

    Rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)

    @classmethod
    def get_pos(cls):
        return pygame.mouse.get_pos()

    @classmethod
    def get_rect(cls):
        return cls.Rect

    @classmethod
    def event_active(cls, event):
        event_value = cls.__dict__[event]
        event_dict = {event.type: event for event in cls.EVENTS}
        return event_dict.get(event_value)

    @classmethod
    def button_pressed(cls, button):
        mappings = {"MONE": 1, "MTWO": 3, "MMIDDLE": 2}
        return cls.__dict__["MOUSEBUTTON"][mappings[button]]

    @classmethod
    def update(cls):
        cls.EVENTS = Events.get_events()

        event = cls.event_active("MOUSEBUTTONDOWN")
        if event:
            cls.MOUSEBUTTON[event.button] = True

        event = cls.event_active("MOUSEBUTTONUP")
        if event:
            cls.MOUSEBUTTON[event.button] = False

        cls.Rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)
