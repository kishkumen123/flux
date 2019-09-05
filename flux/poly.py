import pygame
from mouse import Mouse
from events import events


class Poly:

    def __init__(self, color, points, surface, width=0):
        self.color = color
        self.points = list(points)
        self.width = width
        self.surface = surface
        self._editable = False
        self.rect = pygame.Rect((0,0,0,0))
        self.mouse_down = False
        self.pos_on_click = (0, 0)
        self.move_offset = None

    def editable(self, value=True):
        self._editable = value

    def draw(self):
        self.rect = pygame.draw.polygon(self.surface, self.color, self.points, self.width)
        self.update()

    def intersects_rect_point(self, rect):
        for i, point in enumerate(self.points):
            if rect.collidepoint(point[0], point[1]):
                return i

        return None

    def contains_rect(self, rect):
        # this shit aint working right false positives retarded piece of garbage stanky ass shit
        return self.rect.contains(rect)

    def wireframe(self):
        self.width = 1

    def fill(self):
        self.width = 0

    def update(self):
        self.move_rect()
        self.move_point()

    def move_rect(self):
        if self._editable:
            if self.contains_rect(Mouse.get_rect()):
                if events.button_pressed("MONE") and not events.key_pressed("LSHIFT"):
                    if self.move_offset is not None:
                        for i, _ in enumerate(self.points):
                            self.points[i] = (Mouse.get_pos()[0] + self.move_offset[i][0], Mouse.get_pos()[1] + self.move_offset[i][1])
                else:
                    self.move_offset = [(self.points[i][0] - Mouse.get_pos()[0], self.points[i][1] - Mouse.get_pos()[1]) for i, _ in enumerate(self.points)]

    def move_point(self):
        if self._editable:
            if events.button_pressed("MONE") and events.key_pressed("LSHIFT"):
                index = self.intersects_rect_point(Mouse.get_rect())
                if index is not None:
                    if index is not None and pygame.mouse.get_pressed()[0]:
                        self.points[index] = Mouse.get_pos()
