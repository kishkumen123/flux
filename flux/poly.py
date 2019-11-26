import globals
import pygame

from mouse import mouse
from events import events
from screen import Display


class Poly:

    def __init__(self, name, layer, color, points, surface, width=0):
        self.layer = layer
        self.name = name
        self.color = color
        self.points = list(points)
        self.width = width
        self.surface = surface
        self._editable = False
        self.rect = pygame.Rect((0,0,0,0))
        self.mouse_down = False
        self.pos_on_click = (0, 0)
        self.move_offset = None

    def get_rect(self):
        return self.rect

    def editable(self, value=True):
        self._editable = value

    def draw(self):
        if self.surface is None:
            self.surface = Display.fake_display

        self.rect = pygame.draw.polygon(self.surface, self.color, self.points, self.width)
        self.update()

    def intersects_point(self, rect):
        for i, point in enumerate(self.points):
            if rect.collidepoint(point[0], point[1]):
                return i

        return None

    def contains(self, rect):
        # this shit aint working right false positives retarded piece of garbage stanky ass shit
        return self.rect.contains(rect)

    def wireframe(self):
        self.width = 1

    def fill(self):
        self.width = 0

    def update(self):
        if globals.editor:
            if globals.get_selection() is not None:
                if globals.get_selection().name == self.name:
                    self.move_rect()
                    self.move_point()
                else:
                    self.move_offset = None

    def move_rect(self):
        if self.contains(mouse.get_rect()):
            if events.button_pressed("MONE") and not events.key_pressed("LSHIFT"):
                if self.move_offset is not None:
                    for i, _ in enumerate(self.points):
                        self.points[i] = (mouse.get_pos()[0] + self.move_offset[i][0], mouse.get_pos()[1] + self.move_offset[i][1])
                else:
                    self.move_offset = [(self.points[i][0] - mouse.get_pos()[0], self.points[i][1] - mouse.get_pos()[1]) for i, _ in enumerate(self.points)]
            else:
                self.move_offset = None

    def move_point(self):
        if events.button_pressed("MONE") and events.key_pressed("LSHIFT"):
            index = self.intersects_point(mouse.get_rect())
            if index is not None:
                if index is not None and pygame.mouse.get_pressed()[0]:
                    self.points[index] = mouse.get_pos()

    def __str__(self):
        return self.name
