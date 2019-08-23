import pygame


class Events:
    QUIT = pygame.QUIT
    ACTIVEEVENT = pygame.ACTIVEEVENT
    KEYDOWN = pygame.KEYDOWN
    KEYUP = pygame.KEYUP
    MOUSEMOTION = pygame.MOUSEMOTION
    MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
    MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
    JOYAXISMOTION = pygame.JOYAXISMOTION
    JOYBALLMOTION = pygame.JOYBALLMOTION
    JOYHATMOTION = pygame.JOYHATMOTION
    JOYBUTTONUP = pygame.JOYBUTTONUP
    JOYBUTTONDOWN = pygame.JOYBUTTONDOWN
    VIDEORESIZE = pygame.VIDEORESIZE
    VIDEOEXPOSE = pygame.VIDEOEXPOSE
    USEREVENT = pygame.USEREVENT

    EVENTS = []

    @classmethod
    def event_active(cls, event):
        event_value = cls.__dict__[event]
        event_dict = {event.type: event for event in cls.EVENTS}
        return event_dict.get(event_value)

    @classmethod
    def get_events(cls):
        return cls.EVENTS

    @classmethod
    def update(cls):
        cls.EVENTS = pygame.event.get()
