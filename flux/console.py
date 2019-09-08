import pygame
from screen import Display
from layer import Layer
from events import events


class Console:

    def __init__(self):
        self.console_background = pygame.draw.rect(Display.fake_display, (49, 103, 250), (0, 0, 100, 0))
        self.console_textfield = pygame.draw.rect(Display.fake_display, (138, 201, 181), (0, 0, 100, 0))
        self.current_opennes = 0
        self.history = ["load level1", "debug on", "wireframe on"]
        self.open_dict = {"CLOSED": 0, "MIN": 0.3, "MAX": 0.8}

        self.open_amount = "MIN"
        self.y = 0

        self.layer = "layer_999"
        self.text = ""

    def calc_openess(self, amount):
        self.open_amount = amount
        ratio = self.open_dict[self.open_amount]
        return Display.y * ratio

    def update(self):
        font = pygame.font.Font('freesansbold.ttf', 14)

        if events.key_pressed("TAB", "layer_all") and events.key_pressed("LSHIFT", "layer_all"):
            self.y = self.calc_openess("MAX")
            Layer.set_layer("layer_999")

        if events.key_pressed_once("TAB", "layer_all") and not events.key_pressed("LSHIFT", "layer_all"):
            if self.open_amount == "MIN":
                self.y = self.calc_openess("CLOSED")
                Layer.set_layer("layer_0")
            else:
                self.y = self.calc_openess("MIN")
                Layer.set_layer("layer_999")

        if events.key_pressed_once("ESCAPE", "layer_999"):
            self.y = self.calc_openess("CLOSED")
            Layer.pop_layer()

        self.console_background = pygame.draw.rect(Display.fake_display, (49, 103, 250), (0, 0, Display.x, self.y))
        self.console_textfield = pygame.draw.rect(Display.fake_display, (30, 201, 181), (0, self.y - 20, Display.x, 20))

        key = events.handle_text_input_event("layer_999")
        if key:
            self.text += key
        if events.key_pressed_once("BACKSPACE", "layer_999"):
            self.text = self.text[:-1]
        if events.key_pressed_once("RETURN", "layer_999") and len(self.text):
            self.history.append(self.text)
            self.text = ""

        input_box = pygame.Rect(0, self.y - 20, Display.x, 20)
        txt_surface = font.render(self.text, True, (30, 30, 30))
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        Display.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(Display.fake_display, (30, 201, 181), input_box, 2)

        for i, value in enumerate(reversed(self.history)):
            text = font.render(value, True, (30, 30, 30))

            text_rect = text.get_rect()
            text_rect.x = 5
            text_rect.y = self.y - 40 - (20 * i)
            Display.blit_text(text, text_rect)


console = Console()
