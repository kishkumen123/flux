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

    def get(self):
        return pygame.event.get()

    def QUIT(self, event):
        return event.type == pygame.QUIT

    def KEYDOWN(self, event):
        return event.type == pygame.KEYDOWN

    def RESIZE(self, event):
        return event.type == pygame.VIDEORESIZE
