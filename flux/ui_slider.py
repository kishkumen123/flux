import pygame
from screen import Display
from mouse import mouse
from events import events
from fmath import convert_num_range


class Slider:

    def __init__(self, name, panel, sl_range, size=None, color=(128, 0, 128), _round=False, starting_value=0, knob_width=20):
        self.name = name
        self.parent = panel.name
        self.size = size
        self.sl_range = sl_range
        self._round = _round
        self.color = color
        self.value = starting_value
        self.knob_width = knob_width

        self.font = pygame.font.SysFont('Consolas', 22)
        self.surface_value = self.font.render(str(self.value), True, (50, 50, 50))
        self.surface_name = self.font.render(self.name, True, (50, 50, 50))

        self.spacing_x = 20
        self.name_position_x = panel.position[0] + panel.padding[0]
        self.slider_position_x = self.name_position_x + self.surface_name.get_width() + self.spacing_x
        self.value_position_x = self.slider_position_x + self.size[0] + self.spacing_x

        if len(panel.components) == 0:
            self.world_position = [self.name_position_x, panel.position[1] + panel.padding[1]]
        else:
            panel_components = list(panel.components.items())
            self.world_position = [self.name_position_x, (panel.position[1] + panel.padding[1] + panel_components[-1][1].local_position[1] + panel_components[-1][1].size[1] + panel.spacing)]
        self.local_position = (self.world_position[0] - panel.position[0], self.world_position[1] - panel.position[1])
        self.left_bound = pygame.Rect((self.slider_position_x, self.world_position[1]), (2, size[1]))
        self.right_bound = pygame.Rect((self.slider_position_x + size[0], self.world_position[1]), (2, size[1]))
        self.bar = pygame.Rect((self.slider_position_x, self.world_position[1] + size[1]/2), (size[0], 2))
        self.knob_x = convert_num_range(self.sl_range, (self.slider_position_x, self.slider_position_x + self.size[0] - self.knob_width), starting_value)
        self.knob = pygame.Rect((self.knob_x, self.world_position[1]), (self.knob_width, size[1]))
        self.movable_knob = False
        self.calc_mouse_difference = False
        self.mouse_difference = 0

    def get_value(self):
        return self.value

    def draw(self):
        Display.fake_display.blit(self.surface_name, (self.name_position_x, self.world_position[1]))
        pygame.draw.rect(Display.fake_display, self.color, self.left_bound)
        pygame.draw.rect(Display.fake_display, self.color, self.right_bound)
        pygame.draw.rect(Display.fake_display, self.color, self.bar)
        pygame.draw.rect(Display.fake_display, self.color, self.knob)
        Display.fake_display.blit(self.surface_value, (self.value_position_x, self.world_position[1] - 5))

    def update(self):
        if events.button_pressed("MONE", "layer_0"):
            if mouse.get_rect().colliderect(self.knob):
                self.movable_knob = True
        else:
            self.movable_knob = False
            self.calc_diff = False

        if self.movable_knob:
            if not self.calc_mouse_difference:
                self.mouse_difference = self.knob_x - mouse.get_pos()[0]
                self.calc_mouse_difference = True
            self.knob_x = mouse.get_pos()[0] + self.mouse_difference
            if self.knob_x < self.slider_position_x:
                self.knob_x = self.slider_position_x
            if self.knob_x + 20 > self.slider_position_x + self.size[0]:
                self.knob_x = self.slider_position_x + self.size[0] - 20
            self.knob = pygame.Rect((self.knob_x, self.world_position[1]), (self.knob_width, self.size[1]))
            self.value = convert_num_range((self.slider_position_x, self.slider_position_x + self.size[0] - 20), self.sl_range, self.knob_x)
            if self._round:
                self.value = round(self.value)
                self.surface_value = self.font.render(str(self.value), True, (50, 50, 50))
            else:
                self.surface_value = self.font.render(str(round(self.value, 2)), True, (50, 50, 50))

