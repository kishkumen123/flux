import pygame
from flux.screen import Display
from flux.mouse import mouse
from flux.events import events
from flux.fmath import convert_num_range
from flux.renderer import renderer


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

        self.panel_position = panel.position
        self.panel_padding = panel.padding
        self.panel_components = list(panel.components.items())
        self.panel_spacing = panel.spacing
        self.spacing_x = 20
        self.name_position_x = self.panel_position[0] + self.panel_padding[0]
        self.slider_position_x = self.name_position_x + self.surface_name.get_width() + self.spacing_x
        self.value_position_x = self.slider_position_x + self.size[0] + self.spacing_x

        if self.panel_components == 0:
            self.world_position = [self.name_position_x, self.panel_position[1] + self.panel_padding[1]]
        else:
            self.world_position = [self.name_position_x, (self.panel_position[1] + self.panel_padding[1] + self.panel_components[-1][1].local_position[1] + self.panel_components[-1][1].size[1] + self.panel_spacing)]
        self.local_position = (self.world_position[0] - self.panel_position[0], self.world_position[1] - self.panel_position[1])

        self.left_bound = pygame.Rect((self.slider_position_x, self.world_position[1]), (2, self.size[1]))
        self.right_bound = pygame.Rect((self.slider_position_x + self.size[0], self.world_position[1]), (2, self.size[1]))
        self.bar = pygame.Rect((self.slider_position_x, self.world_position[1] + self.size[1]/2), (self.size[0], 2))
        self.knob_x = convert_num_range(self.sl_range, (self.slider_position_x, self.slider_position_x + self.size[0] - self.knob_width), starting_value)
        self.knob = pygame.Rect((self.knob_x, self.world_position[1]), (self.knob_width, self.size[1]))

        self.movable_knob = False
        self.calc_mouse_difference = False
        self.mouse_difference = 0

    def get_value(self):
        return self.value

    def draw(self):
        name = renderer.draw_text(self.name, (self.name_position_x, self.world_position[1]), (50, 50, 50))
        left_bound = renderer.draw_quad((self.slider_position_x, self.world_position[1]), (2, self.size[1]), self.color)
        right_bound = renderer.draw_quad((self.slider_position_x + self.size[0], self.world_position[1]), (2, self.size[1]), self.color)
        bar = renderer.draw_quad((self.slider_position_x, self.world_position[1] + self.size[1]/2), (self.size[0], 2), self.color)
        knob = renderer.draw_quad((self.knob_x, self.world_position[1]), (self.knob_width, self.size[1]), self.color)
        value = renderer.draw_text(str(self.value), (self.value_position_x, self.world_position[1] - 5), (50, 50, 50))

    def update_ui_positions(self, panel_position):
        self.panel_position = panel_position

        self.name_position_x = self.panel_position[0] + self.panel_padding[0]
        self.slider_position_x = self.name_position_x + self.surface_name.get_width() + self.spacing_x
        self.value_position_x = self.slider_position_x + self.size[0] + self.spacing_x

        if self.panel_components == 0:
            self.world_position = [self.name_position_x, self.panel_position[1] + self.panel_padding[1]]
        else:
            self.world_position = [self.name_position_x, (self.panel_position[1] + self.panel_padding[1] + self.panel_components[-1][1].local_position[1] + self.panel_components[-1][1].size[1] + self.panel_spacing)]
        self.local_position = (self.world_position[0] - self.panel_position[0], self.world_position[1] - self.panel_position[1])

        self.left_bound = pygame.Rect((self.slider_position_x, self.world_position[1]), (2, self.size[1]))
        self.right_bound = pygame.Rect((self.slider_position_x + self.size[0], self.world_position[1]), (2, self.size[1]))
        self.bar = pygame.Rect((self.slider_position_x, self.world_position[1] + self.size[1] / 2), (self.size[0], 2))
        self.knob_x = convert_num_range(self.sl_range, (self.slider_position_x, self.slider_position_x + self.size[0] - self.knob_width), self.value)
        self.knob = pygame.Rect((self.knob_x, self.world_position[1]), (self.knob_width, self.size[1]))

    def update(self, panel_position):
        self.update_ui_positions(panel_position)

        if events.button_pressed("MONE", "layer_3"):
            if mouse.get_rect().colliderect(self.knob):
                self.movable_knob = True
        else:
            self.movable_knob = False
            self.calc_mouse_difference = False

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

