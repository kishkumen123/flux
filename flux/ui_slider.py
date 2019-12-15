import pygame
from screen import Display
from mouse import mouse
from events import events
from fmath import convert_num_range


class Slider:

    def __init__(self, name, parent, world_position, sl_range, size=None, position=None, color=(128, 0, 128), round_int=False, starting_value=0):
        self.name = name
        self.parent = parent
        self.size = size
        self.sl_range = sl_range
        self.round_int = round_int
        self.world_position = world_position
        self.relative_position = position
        self.local_position = [a + self.relative_position[i] for i, a in enumerate(self.world_position)]
        self.color = color
        self.left_bound = pygame.Rect(self.local_position, (2, size[1]))
        self.right_bound = pygame.Rect((self.local_position[0] + size[0], self.local_position[1]), (2, size[1]))
        self.bar = pygame.Rect((self.local_position[0], self.local_position[1] + size[1]/2), (size[0], 2))
        self.value = starting_value
        self.knob_x = convert_num_range(self.sl_range, (self.local_position[0], self.local_position[0] + self.size[0] - 20), starting_value)
        self.knob = pygame.Rect((self.knob_x, self.local_position[1]), (20, size[1]))
        self.movable_knob = False
        self.calc_diff = False
        self.font = pygame.font.SysFont('Consolas', 22)
        self.difference = 0
        self.value_surface = self.font.render(str(self.value), True, (50, 50, 50))

    def draw(self):
        pygame.draw.rect(Display.fake_display, self.color, self.left_bound)
        pygame.draw.rect(Display.fake_display, self.color, self.right_bound)
        pygame.draw.rect(Display.fake_display, self.color, self.bar)
        pygame.draw.rect(Display.fake_display, self.color, self.knob)

    def update(self):
        if events.button_pressed("MONE", "layer_0"):
            if mouse.get_rect().colliderect(self.knob):
                self.movable_knob = True
        if events.button_released("MONE", "layer_0"):
            self.movable_knob = False

        if self.movable_knob:
            if not self.calc_diff:
                self.difference = self.knob_x - mouse.get_pos()[0]
                self.calc_diff = True
            self.knob_x = mouse.get_pos()[0] + self.difference
            if self.knob_x < self.local_position[0]:
                self.knob_x = self.local_position[0]
            if self.knob_x + 20 > self.local_position[0] + self.size[0]:
                self.knob_x = self.local_position[0] + self.size[0] - 20
            self.knob = pygame.Rect((self.knob_x, self.local_position[1]), (20, self.size[1]))
            self.value = convert_num_range((self.local_position[0], self.local_position[0] + self.size[0] - 20), self.sl_range, self.knob_x)
            if self.round_int:
                self.value = round(self.value)
                self.value_surface = self.font.render(str(self.value), True, (50, 50, 50))
            else:
                self.value_surface = self.font.render(str(round(self.value, 2)), True, (50, 50, 50))
        Display.fake_display.blit(self.value_surface, (self.local_position[0] + self.size[0] + 20, self.local_position[1] - 5))

