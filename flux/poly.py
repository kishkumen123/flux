import pygame

from flux._globals import editor
from flux.screen import Display
from flux.renderer import renderer


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

        self.rect = renderer.draw_poly(self.points, self.color, self.width)
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
        if editor:
            pass
        else:
            pass

    def __str__(self):
        return self.name
