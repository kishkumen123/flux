import pygame
import globals

from screen import Display
from layer import Layer
from events import events
from commands import init_commands, run_command


class Console:
    init_commands()

    def __init__(self):
        self.console_background = pygame.draw.rect(Display.fake_display, (49, 103, 250), (0, 0, 100, 0))
        self.console_textfield = pygame.draw.rect(Display.fake_display, (60, 61, 56), (0, 0, 100, 0))
        self.cursor = pygame.draw.rect(Display.fake_display, (200, 200, 200), (0, 2, 15, 0))
        self.curser_position_y = 15
        self.curser_position_x = 5
        self.current_opennes = 0
        self.open_dict = {"CLOSED": 0, "MIN": 0.3, "MAX": 0.8}

        self.open_amount = "CLOSED"
        self.target_openess = 0
        self.y = 0

        self.layer = "layer_999"
        self.text = ""
        self.pause = False

    def calc_openess(self, amount):
        self.open_amount = amount
        ratio = self.open_dict[self.open_amount]
        self.target_openess = Display.y * ratio

    def add_to_history(self, command):
        globals.history.append(command)

    def animate_console(self, dt):
        if self.y > self.target_openess:
            self.y -= 1000 * dt
            if self.y < self.target_openess:
                self.y = self.target_openess

        if self.y < self.target_openess:
            self.y += 1000 * dt
            if self.y > self.target_openess:
                self.y = self.target_openess

    def update(self, dt):
        font = pygame.font.SysFont('Consolas', 18)

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

            key = events.handle_text_input_event("layer_999")
            if key:
                self.text += key
            if events.key_pressed_once("BACKSPACE", "layer_999"):
                self.text = self.text[:-1]
            if events.key_pressed_once("RETURN", "layer_999") and len(self.text):
                run_command(self.text)
                self.text = ""

            self.console_background = pygame.draw.rect(Display.fake_display, (39, 40, 34), (0, 0, Display.x, self.y))
            self.console_textfield = pygame.draw.rect(Display.fake_display, (60, 61, 56), (0, self.y - 22, Display.x, 22))

            txt_surface = font.render(self.text, True, (255, 175, 0))
            cursor_position_offset = self.curser_position_x + txt_surface.get_width()
            if globals.cursor_underscore:
                self.cursor = pygame.draw.rect(Display.fake_display, (200, 200, 200), (cursor_position_offset, self.y - 0, 8, 0))
            else:
                self.cursor = pygame.draw.rect(Display.fake_display, (200, 200, 200), (cursor_position_offset, self.y - 20, 10, 18))
            Display.fake_display.blit(txt_surface, (self.console_textfield.x + 5, self.console_textfield.y + 2))

            for i, value in enumerate(reversed(globals.history)):
                text = font.render(value, True, (255, 175, 0))

                text_rect = text.get_rect()
                text_rect.x = 5
                text_rect.y = self.y - 40 - (20 * i)
                Display.blit_text(text, text_rect)


console = Console()
