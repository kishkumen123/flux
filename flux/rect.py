
import pygame


class Poly:

    def __init__(self, color, points, surface, width=0, fill=True):
        self.color = color
        self.points = list(points)
        self.fill = fill
        self.width = width
        self.surface = surface
        self._move_point_on_press = False

    def move_point_on_press(self, value=True):
        self._move_point_on_press = value

    def draw(self, rect=None):
        pygame.draw.polygon(self.surface, self.color, self.points, self.width)

        if self._move_point_on_press:
            index = self.intersects_rect(rect)

            if index is not None and pygame.mouse.get_pressed()[0]:
                self.points[index] = pygame.mouse.get_pos()

    def intersects_rect(self, rect):
        for i, point in enumerate(self.points):
            if rect.collidepoint(point[0], point[1]):
                return i

        return None

#    def move_point_on_press(self, rect):
#        index = self.intersects_rect(rect)
#
#        if index and pygame.mouse.get_pressed()[0]:
#            self.points[index] = pygame.mouse.get_pos()
#
