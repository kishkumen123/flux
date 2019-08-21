
import pygame


class Poly:

    def __init__(self, color, points, surface, width=0):
        self.color = color
        self.points = list(points)
        self.width = width
        self.surface = surface
        self._move_on_press = False
        self.rect = pygame.Rect((0,0,0,0))
        self.mouse_down = False
        self.pos_on_click = (0, 0)
        self.offset = None

    def move_on_press(self, value=True):
        self._move_on_press = value

    def draw(self, rect=None):
        self.rect = pygame.draw.polygon(self.surface, self.color, self.points, self.width)

        if self._move_on_press:
            if pygame.mouse.get_pressed()[0]:
                if self.mouse_down is False:
                    self.offset = [(self.points[i][0] - pygame.mouse.get_pos()[0], self.points[i][1] - pygame.mouse.get_pos()[1]) for i, _ in enumerate(self.points)]
                    self.mouse_down = True

                index = self.intersects_rect_point(rect)

                if self.contains_rect(rect) and self.offset is not None:
                    self.move_poly()

                elif index is not None:
                    self.move_point(index)
            else:
                self.mouse_down = False

    def move_poly(self):
        for i, _ in enumerate(self.points):
            self.points[i] = (pygame.mouse.get_pos()[0] + self.offset[i][0], pygame.mouse.get_pos()[1] + self.offset[i][1])

    def move_point(self, index):
        if index is not None and pygame.mouse.get_pressed()[0]:
            self.points[index] = pygame.mouse.get_pos()

    def intersects_rect_point(self, rect):
        for i, point in enumerate(self.points):
            if rect.collidepoint(point[0], point[1]):
                return i

        return None

    def contains_rect(self, rect):
        return self.rect.contains(rect)

    def wireframe(self):
        self.width = 1

    def fill(self):
        self.width = 0
