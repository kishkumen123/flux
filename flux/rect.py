import pygame


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

    def draw(self, rect=None):
        self.rect = pygame.draw.polygon(self.surface, self.color, self.points, self.width)
        self.update(rect)

    def move_poly(self):
        for i, _ in enumerate(self.points):
            self.points[i] = (pygame.mouse.get_pos()[0] + self.move_offset[i][0], pygame.mouse.get_pos()[1] + self.move_offset[i][1])

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

    def update(self, rect):
        self.move_rect(rect)
        self.move_point(rect)

    def move_rect(self, rect):
        if self._editable:
            keys = pygame.key.get_pressed()
            if pygame.mouse.get_pressed()[0] and not keys[pygame.K_LSHIFT]:
                if self.mouse_down is False:
                    self.move_offset = [(self.points[i][0] - pygame.mouse.get_pos()[0], self.points[i][1] - pygame.mouse.get_pos()[1]) for i, _ in enumerate(self.points)]
                    self.mouse_down = True

                if self.contains_rect(rect) and self.move_offset is not None:
                    self.move_poly()
            else:
                self.mouse_down = False

    def move_point(self, rect):
        if self._editable:
            keys = pygame.key.get_pressed()
            if pygame.mouse.get_pressed()[0] and keys[pygame.K_LSHIFT]:
                index = self.intersects_rect_point(rect)
                if index is not None:
                    if index is not None and pygame.mouse.get_pressed()[0]:
                        self.points[index] = pygame.mouse.get_pos()
