import pygame
import globals

from screen import Display
from layer import Layer
from events import events
from mouse import Mouse
from commands import init_commands, run_command


class Console:
    init_commands()

    def __init__(self):
        self.console_background = pygame.draw.rect(Display.fake_display, (49, 103, 250), (0, 0, 100, 0))
        self.console_textfield = pygame.draw.rect(Display.fake_display, (60, 61, 56), (0, 0, 100, 0))
        self.cursor = pygame.draw.rect(Display.fake_display, (200, 200, 200), (0, 2, 15, 0))
        self.cursor_position_y = 15
        self.cursor_position_x = 5
        self.current_opennes = 0
        self.open_dict = {"CLOSED": 0, "MIN": 0.3, "MAX": 0.8}
        self.history_length = len(globals.history_input)
        self.history_index = None
        self.text = ""
        self.stored_text = self.text
        self.cursor_length = len(self.text)
        self.cursor_index = None
        self.scrollable = False

        self.open_amount = "CLOSED"
        self.target_openess = 0
        self.y = 0

        self.layer = "layer_999"
        self.pause = False
        self.mouse_wheel_offset = 0

    def calc_openess(self, amount):
        self.open_amount = amount
        ratio = self.open_dict[self.open_amount]
        self.target_openess = Display.y * ratio

    def animate_console(self, dt):
        if self.y > self.target_openess:
            self.y -= 1000 * dt
            if self.y < self.target_openess:
                self.y = self.target_openess

        if self.y < self.target_openess:
            self.y += 1000 * dt
            if self.y > self.target_openess:
                self.y = self.target_openess

    def draw_background(self):
        self.console_background = pygame.draw.rect(Display.fake_display, (39, 40, 34), (0, 0, Display.x, self.y))

    def draw_textfield(self):
        self.console_textfield = pygame.draw.rect(Display.fake_display, (60, 61, 56), (0, self.y - 22, Display.x, 22))

    def draw_cursor(self, txt_surface):
        self.cursor_length = len(self.text)
        sub_amount = self.cursor_length if self.cursor_length == self.cursor_index or self.cursor_index is None else self.cursor_index
        cursor_position_offset = self.cursor_position_x + txt_surface.get_width() - (10 * (self.cursor_length - sub_amount))
        if globals.cursor_underscore:
            self.cursor = pygame.draw.rect(Display.fake_display, (200, 200, 200), (cursor_position_offset, self.y - 0, 8, 0))
        else:
            self.cursor = pygame.draw.rect(Display.fake_display, (200, 200, 200), (cursor_position_offset, self.y - 20, 10, 18))

    def draw_history(self, font):
        for i, value in enumerate(reversed(globals.history_output)):
            text = font.render(value, True, (255, 175, 0))

            text_rect = text.get_rect()
            text_rect.x = 5
            text_rect.y = self.y - 40 - (20 * i) + self.mouse_wheel_offset
            if text_rect.y < 0:
                self.scrollable = True
            else:
                self.scrollable = False
            if text_rect.y < self.y - 20:
                Display.blit_text(text, text_rect)

    def add_text_at_cursor(self, key):
        left = self.text[:self.cursor_index]
        right = self.text[self.cursor_index:]
        self.text = left + key + right
        if self.cursor_index is not None and self.cursor_index >= 0:
            self.cursor_index += 1
        else:
            self.cursor_index = 1

    def remove_text_at_cursor(self):
        if self.cursor_index is not None and self.cursor_index > 0:
            left = self.text[:self.cursor_index-1]
            right = self.text[self.cursor_index:]
            self.text = left + right

            if self.cursor_index > 0:
                self.cursor_index -= 1

    def run_command(self, text):
        run_command(text)
        self.text = ""
        self.history_index = None
        self.cursor_index = None

    def update(self, dt):
        font = pygame.font.SysFont('Consolas', 18)
        self.history_length = len(globals.history_input)
        self.cursor_length = len(self.text)

        if events.key_pressed("TAB", "layer_all") and events.key_pressed("LSHIFT", "layer_all"):
            if self.open_amount == "MAX":
                self.calc_openess("CLOSED")
                Layer.pop_layer()
            else:
                self.calc_openess("MAX")
                Layer.set_layer("layer_999")

        if events.key_pressed_once("TAB", "layer_all") and not events.key_pressed("LSHIFT", "layer_all"):
            if self.open_amount == "MIN":
                self.calc_openess("CLOSED")
                Layer.pop_layer()
            else:
                self.calc_openess("MIN")
                Layer.set_layer("layer_999")

        self.animate_console(dt)
        if self.y > 0:

            if Mouse.get_pos()[1] < self.y:
                if events.mouse_wheel_down:
                    if self.mouse_wheel_offset != 0:
                        self.mouse_wheel_offset -= 20
                if events.mouse_wheel_up:
                    if self.scrollable:
                        self.mouse_wheel_offset += 20

            key = events.handle_text_input_event_repeat("layer_999")
            if key:
                self.add_text_at_cursor(key)
            if events.key_pressed_repeat("BACKSPACE", "layer_999"):
                self.remove_text_at_cursor()
            if events.key_pressed_once("RETURN", "layer_999") and len(self.text):
                self.run_command(self.text)

            if events.key_pressed_repeat("LEFT", "layer_999"):
                if self.cursor_index is None:
                    self.cursor_index = self.cursor_length
                if self.cursor_index > 0:
                    self.cursor_index -= 1
            if events.key_pressed_repeat("RIGHT", "layer_999"):
                if self.cursor_index is not None:
                    if self.cursor_index < self.cursor_length:
                        self.cursor_index += 1
                    if self.cursor_index == self.cursor_length:
                        self.cursor_index = None

            if events.key_pressed_once("UP", "layer_999"):
                if self.history_index is None:
                    self.history_index = self.history_length
                    self.stored_text = self.text
                if self.history_index > 0:
                    self.history_index -= 1
                if len(globals.history_input):
                    self.text = globals.history_input[self.history_index]
                    self.cursor_length = len(self.text)
                    self.cursor_index = self.cursor_length
            if events.key_pressed_once("DOWN", "layer_999"):
                if self.history_index is not None:
                    self.history_index += 1
                    if self.history_index >= self.history_length:
                        self.history_index = None
                        self.text = self.stored_text
                        self.stored_text = ""
                    else:
                        self.text = globals.history_input[self.history_index]
                    self.cursor_length = len(self.text)
                    self.cursor_index = self.cursor_length

            if events.key_pressed_once("HOME", "layer_999"):
                self.cursor_index = 0
            if events.key_pressed_once("END", "layer_999"):
                self.cursor_index = self.cursor_length

            txt_surface = font.render(self.text, True, (255, 175, 0))

            self.draw_background()
            self.draw_textfield()
            self.draw_cursor(txt_surface)
            self.draw_history(font)

            Display.fake_display.blit(txt_surface, (self.console_textfield.x + 5, self.console_textfield.y + 2))


console = Console()
