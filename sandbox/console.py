
import pygame
import string
from pygame.locals import * 
from enum import Enum

import math
import _globals

from fmath import v2lerp, v2, v2distance
from commands import init_commands, run_command, get_commands
from events import Events
from _globals import textinput_list


class CState(Enum):
    CLOSED = 0
    OPEN_SMALL = 0.3
    OPEN_BIG = 0.7


# TODO: REMEMBER TO OPTIMIZE THIS SO THAT IT ONLY DRAWS STUFF WHEN THINGS CHANGE LIKE INPUTING NEW HISTORY OR TYPING IN LETTERS
class Console:
    init_commands()

    def __init__(self, screen, font):
        self.state = CState.CLOSED
        self.screen = screen
        self.open_speed = 1000
        self.lerp_percent = 0

        self.current_position = v2(self.screen.get_width(),0)
        self.start_position = v2(self.screen.get_width(), 0)
        self.end_position = v2(self.screen.get_width(), 0)
        self.cursor_position = 5
        self.scroll_offset = 0
        self.cursor_index = 0
        self.history_index = None
        self.history_y_position = 0

        self.background_color = (39, 40, 34)
        self.textfield_color = (60, 61, 56)
        self.cursor_color = (231, 232, 226)
        self.history_color = (202, 202, 202)
        self.text_color = (202, 202, 202)
        self.tag_color = (255, 175, 0)
        self.autocomplete_color = (150, 150, 150)

        self.tag_text = "λ/> "
        self.text = ""
        self.mask_text = ""
        self.stored_text = ""
        self.autocomplete_text = ""
        self.autocomplete_from = get_commands()
        
        self.font = font
        self.tag_surface = self.font.render(self.tag_text, True, self.tag_color)

        self.event = None

    def is_open(self):
        return self.state != CState.CLOSED

    def handle_event(self, event):
        if event.type == TEXTINPUT:
            if event.text != "~" and event.text != "`":
                left = self.text[:self.cursor_index]
                right = self.text[self.cursor_index:]
                self.text = left + event.text + right
                self.mask_text = left + event.text 
                self.cursor_index += 1
                self.autocomplete_text = self.get_autocomplete_text(self.autocomplete_from)
                Events.consume(event)

        if event.type == KEYDOWN:
            if Events.key(event, K_ESCAPE):
                self.open(CState.CLOSED)
                pygame.key.set_repeat(0,0)
            if Events.key(event, K_BACKQUOTE):
                if self.state == CState.OPEN_SMALL:
                    self.open(CState.CLOSED)
                    pygame.key.set_repeat(0,0)
                else:
                    self.open(CState.OPEN_SMALL)
            if Events.key(event, K_BACKQUOTE, 1):
                if self.state == CState.OPEN_BIG:
                    self.open(CState.CLOSED)
                    pygame.key.set_repeat(0,0)
                else:
                    self.open(CState.OPEN_BIG)

            if Events.key(event, K_RETURN):
                if len(self.text) > 0:
                    run_command(self.text)
                    self.text = ""
                    self.mask_text = self.text
                    self.cursor_index = 0
                    self.stored_text = ""
                    self.history_index = None
                    self.autocomplete_text = ""
                    self.autocomplete_from = get_commands()

            if Events.key(event, K_BACKSPACE):
                if self.cursor_index > 0:
                    left = self.text[:self.cursor_index-1]
                    right = self.text[self.cursor_index:]
                    self.text = left + right
                    self.mask_text = left
                    self.autocomplete_text = self.get_autocomplete_text(self.autocomplete_from)
                    if self.cursor_index > 0:
                        self.cursor_index -= 1

            if Events.key(event, K_TAB):
                self.text = self.text + self.autocomplete_text
                self.mask_text = self.text
                self.cursor_index = len(self.text)
                self.autocomplete_text = self.get_autocomplete_text(self.autocomplete_from)

            if Events.key(event, K_r, 64):
                self.text = ""
                self.mask_text = ""
                self.cursor_index = len(self.text)
                self.autocomplete_text = ""
                self.autocomplete_from = _globals.history_input

            if Events.key(event, K_LEFT):
                self.mask_text = self.mask_text[:-1]
                if self.cursor_index > 0:
                    self.cursor_index -= 1
            if Events.key(event, K_RIGHT):
                self.mask_text = self.text[:len(self.mask_text) + 1]
                if self.cursor_index < len(self.text):
                    self.cursor_index += 1
                    
            if Events.key(event, K_HOME):
                self.mask_text = ""
                self.cursor_index = 0
            if Events.key(event, K_END):
                self.mask_text = self.text
                self.cursor_index = len(self.text)

            if Events.key(event, K_UP):
                if len(_globals.history_input):
                    if self.history_index is None:
                        self.history_index = 0
                        self.stored_text = self.text
                    elif self.history_index < len(_globals.history_input) - 1:
                        self.history_index += 1

                    self.text = _globals.history_input[self.history_index]
                    self.mask_text = self.text
                    self.cursor_index = len(self.text)
            if Events.key(event, K_DOWN):
                if self.history_index is not None:
                    if self.history_index > 0:
                        self.history_index -= 1
                        self.text = _globals.history_input[self.history_index]
                    elif self.history_index == 0:
                        self.history_index = None
                        self.text = self.stored_text

                    self.mask_text = self.text
                    self.cursor_index = len(self.text)


    # @incomplete- if i want to scroll in greater increments, the end of the scroll has the text that
    # much further down from the top of the screen and should stop at the edge of the top of the screen
    #if pygame.event.peek(MOUSEBUTTONDOWN):
        #event = pygame.event.get(MOUSEBUTTONDOWN)[0]
        if event.type == MOUSEBUTTONDOWN:
            if Events.button(event, 4):
                if self.history_y_position < 0:
                    self.scroll_offset += self.font.size(self.text)[1]
            if Events.button(event, 5):
                if self.scroll_offset != 0:
                    self.scroll_offset -= self.font.size(self.text)[1]

    def update_end_position(self):
        if self.state == CState.CLOSED:
            return CState.CLOSED.value * self.screen.get_height()
        elif self.state == CState.OPEN_SMALL:
            return CState.OPEN_SMALL.value * self.screen.get_height()
        elif self.state == CState.OPEN_BIG:
            return CState.OPEN_BIG.value * self.screen.get_height()

    def draw_history(self, console_rect):
        for i, text in enumerate(_globals.history_output):
            history_surface = self.font.render(text, True, self.history_color)
            self.history_y_position = (console_rect.h - self.font.size(text)[1] - (self.font.size(text)[1] * i) - 8) + self.scroll_offset
            if self.history_y_position < console_rect.h:
                self.screen.blit(history_surface, (5, self.history_y_position))

    # @incomplete- not working in alphabetical order but works well enough for now
    def get_autocomplete_text(self, autocomplete_from):
        if len(self.text) > 0:
            for auto in autocomplete_from:
                left = auto[:len(self.text)]
                right = auto[len(self.text):]
                if self.text == left and len(self.text) < len(auto):
                    return right

    def draw_everything(self):
        console_rect = pygame.draw.rect(self.screen, self.background_color, ((0, 0), (self.current_position.x, self.current_position.y)))
        self.draw_history(console_rect)
        textfield_rect = pygame.draw.rect(self.screen, self.textfield_color, ((0, console_rect.h), (self.screen.get_width(), 24)))
        text_surface = self.font.render(self.text, True, self.text_color)
        self.screen.blit(text_surface, (self.font.size(self.tag_text)[0], textfield_rect.y + 2))
        self.screen.blit(self.tag_surface, (2, textfield_rect.y + 2))
        cursor_x = self.cursor_position + self.font.size(self.mask_text)[0] + self.font.size(self.tag_text)[0]
        cursor_rect = pygame.draw.rect(self.screen, self.cursor_color, ((cursor_x - 5, textfield_rect.y + 1), (10, 20)))
        autocomplete_surface = self.font.render(self.autocomplete_text, True, self.autocomplete_color)
        self.screen.blit(autocomplete_surface, (self.font.size(self.tag_text)[0] + self.font.size(self.text)[0], textfield_rect.y + 2))

    def animate_console(self, lerp_distance, dt):
        if lerp_distance > 0 and self.lerp_percent < 1:
            self.lerp_percent += (self.open_speed / lerp_distance) * dt
            self.current_position = v2lerp(self.start_position, self.end_position, self.lerp_percent)

    def open(self, state):
        if self.state != state:
            self.lerp_percent = 0
            self.start_position = self.current_position
            self.state = state
            self.end_position.y = self.update_end_position()

    def update(self, dt):
        lerp_distance = v2distance(self.start_position, self.end_position)
        self.animate_console(lerp_distance, dt)

        if self.current_position.y > 0:
            self.draw_everything()
