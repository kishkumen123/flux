import pygame
from enum import Enum
from flux import _globals
from flux.display import display
from flux.layer import layer
from flux.events import events
from flux.fmath import lerp2v, Vector2, v2distance
#from flux.mouse import mouse
#from flux.renderer import renderer
from flux.commands import init_commands, run_command, get_commands


class CState(Enum):
    CLOSED = 0
    OPEN_SMALL = 0.3
    OPEN_BIG = 0.7


class ConsoleActions():
    def __init__(self, c):
        self.c = c

    def close(self):
        self.c.state = CState.CLOSED
        self.c.lerp_percent = 0
        self.c.start_position = self.c.current_position
        self.c.end_position.y = self.c.update_end_position()
        layer.pop_layer()

    def open(self):
        self.c.lerp_percent = 0
        self.c.start_position = self.c.current_position

        if events.key_held("K_LSHIFT", "layer_all"):
            if self.c.state == CState.OPEN_BIG:
                self.c.state = CState.CLOSED
                layer.pop_layer()
            else:
                self.c.state = CState.OPEN_BIG
                layer.set_layer("layer_999")
        else:
            if self.c.state == CState.OPEN_SMALL:
                self.c.state = CState.CLOSED
                layer.pop_layer()
            else:
                self.c.state = CState.OPEN_SMALL
                layer.set_layer("layer_999")
        self.c.end_position.y = self.c.update_end_position()

    def update_text(self):
        #text = events.text_input("layer_999")
        text = events.text_input_repeat("layer_999")
        if text is not None:
            left = self.c.text[:self.c.cursor_index]
            right = self.c.text[self.c.cursor_index:]
            self.c.text = left + text + right
            self.c.mask_text = left + text
            self.c.cursor_index += 1

    def animate_open(self, dt):
        lerp_distance = v2distance(self.c.start_position, self.c.end_position)
        if lerp_distance > 0 and self.c.lerp_percent < 1:
            self.c.lerp_percent += (self.c.open_speed / lerp_distance) * dt
            self.c.current_position = lerp2v(self.c.start_position, self.c.end_position, self.c.lerp_percent)

    def run_command(self):
        if len(self.c.text) > 0:
            run_command(self.c.text)
            self.c.text = ""
            self.c.mask_text = self.c.text
            self.c.cursor_index = 0
            self.c.stored_text = ""
            self.c.history_index = None

    def scroll_down(self):
        if self.c.history_y_position < 0:
            self.c.scroll_offset += self.c.font.size(self.c.text)[1]

    def scroll_up(self):
        if self.c.scroll_offset != 0:
            self.c.scroll_offset -= self.c.font.size(self.c.text)[1]

    def backspace(self):
        if self.c.cursor_index > 0:
            left = self.c.text[:self.c.cursor_index-1]
            right = self.c.text[self.c.cursor_index:]
            self.c.text = left + right
            self.c.mask_text = left
            if self.c.cursor_index > 0:
                self.c.cursor_index -= 1

    def move_cursor_left(self):
        self.c.mask_text = self.c.mask_text[:-1]
        if self.c.cursor_index > 0:
            self.c.cursor_index -= 1

    def move_cursor_right(self):
        self.c.mask_text = self.c.text[:len(self.c.mask_text) + 1]
        if self.c.cursor_index < len(self.c.text):
            self.c.cursor_index += 1

    def move_cursor_to_home(self):
        self.c.mask_text = ""
        self.c.cursor_index = 0

    def move_cursor_to_end(self):
        self.c.mask_text = self.c.text
        self.c.cursor_index = len(self.c.text)

    def previous_history_entry(self):
        if len(_globals.history_input):
            if self.c.history_index is None:
                self.c.history_index = 0
                self.c.stored_text = self.c.text
            elif self.c.history_index < len(_globals.history_input) - 1:
                self.c.history_index += 1

            self.c.text = _globals.history_input[self.c.history_index]
            self.c.mask_text = self.c.text
            self.c.cursor_index = len(self.c.text)

    def next_history_entry(self):
        if self.c.history_index is not None:
            if self.c.history_index > 0:
                self.c.history_index -= 1
                self.c.text = _globals.history_input[self.c.history_index]
            elif self.c.history_index == 0:
                self.c.history_index = None
                self.c.text = self.c.stored_text

            self.c.mask_text = self.c.text
            self.c.cursor_index = len(self.c.text)


# TODO: REMEMBER TO OPTIMIZE THIS SO THAT IT ONLY DRAWS STUFF WHEN THINGS CHANGE LIKE INPUTING NEW HISTORY OR TYPING IN LETTERS
class C:
    init_commands()

    """
    left to do -
        console
        - tab auto complete
        - ctrl r search input history

        events
        - text repeat
    """

    def __init__(self):
        self.actions = ConsoleActions(self)

        self.state = CState.CLOSED
        self.open_speed = 1000
        self.lerp_percent = 0

        self.current_position = Vector2((display.x,0))
        self.start_position = Vector2((display.x,0))
        self.end_position = Vector2((display.x,0))
        self.cursor_position = 5
        self.cursor_index = 0
        self.history_index = None

        self.background_color = (39, 40, 34)
        self.textfield_color = (60, 61, 56)
        self.cursor_color = (231, 232, 226)
        self.history_color = (202, 202, 202)
        self.text_color = (202, 202, 202)
        self.tag_color = (255, 175, 0)
        self.scroll_offset = 0
        self.history_y_position = 0

        self.tag_text = "λ/> "
        self.text = ""
        self.mask_text = ""
        self.stored_text = ""
        self.history_input = []

        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", 18)
        self.tag_surface = self.font.render(self.tag_text, True, self.tag_color)

    def update_end_position(self):
        if self.state == CState.CLOSED:
            return CState.CLOSED.value * display.y
        elif self.state == CState.OPEN_SMALL:
            return CState.OPEN_SMALL.value * display.y
        elif self.state == CState.OPEN_BIG:
            return CState.OPEN_BIG.value * display.y

    def draw_history(self, console_rect):
        for i, text in enumerate(_globals.history_output):
            history_surface = self.font.render(text, True, self.history_color)
            self.history_y_position = (console_rect.h - self.font.size(text)[1] - (self.font.size(text)[1] * i) - 8) + self.scroll_offset
            if self.history_y_position < console_rect.h:
                display.window.blit(history_surface, (5, self.history_y_position))

    def draw_all(self):
        console_rect = pygame.draw.rect(display.window, self.background_color, ((0, 0), self.current_position))
        self.draw_history(console_rect)
        textfield_rect = pygame.draw.rect(display.window, self.textfield_color, ((0, console_rect.h), (display.x, 24)))
        text_surface = self.font.render(self.text, True, self.text_color)
        display.window.blit(text_surface, (self.font.size(self.tag_text)[0], textfield_rect.y + 2))
        display.window.blit(self.tag_surface, (2, textfield_rect.y + 2))
        cursor_x = self.cursor_position + self.font.size(self.mask_text)[0] + self.font.size(self.tag_text)[0]
        cursor_rect = pygame.draw.rect(display.window, self.cursor_color, ((cursor_x - 5, textfield_rect.y + 1), Vector2((10, 20))))
        return console_rect

    def update(self, dt):
        if events.key_pressed("K_ESCAPE", "layer_999"):
            self.actions.close()

        if events.key_pressed("K_BACKQUOTE", "layer_all"):
            self.actions.open()

        if self.current_position.y > 0:
            console_rect = self.draw_all()

            if console_rect.collidepoint(pygame.mouse.get_pos()):
                if events.mouse_pressed("M_WHEELDOWN", "layer_999"):
                    self.actions.scroll_down()
                if events.mouse_pressed("M_WHEELUP", "layer_999"):
                    self.actions.scroll_up()

            if events.key_pressed("K_RETURN", "layer_999"):
                self.actions.run_command()

            if events.key_pressed("K_BACKSPACE", "layer_999"):
                self.actions.backspace()

            if events.key_pressed("K_LEFT", "layer_999"):
                self.actions.move_cursor_left()
            if events.key_pressed("K_RIGHT", "layer_999"):
                self.actions.move_cursor_right()

            if events.key_pressed("K_HOME", "layer_999"):
                self.actions.move_cursor_to_home()
            if events.key_pressed("K_END", "layer_999"):
                self.actions.move_cursor_to_end()

            if events.key_pressed("K_UP", "layer_999"):
                self.actions.previous_history_entry()
            if events.key_pressed("K_DOWN", "layer_999"):
                self.actions.next_history_entry()

        self.actions.update_text()
        self.actions.animate_open(dt)


c = C()

class Console:
    #init_commands()

    def __init__(self):
        self.text = ""
        self.cursor_position_y = 15
        self.cursor_position_x = 5
        self.cursor_max = len(self.text)
        self.cursor_index = 0
        self.cursor_color = (200, 200, 200)
        self.current_opennes = 0
        self.open_dict = {"CLOSED": 0, "MIN": 0.3, "MAX": 0.8}
        self.history_length = len(_globals.history_input)
        self.history_index = None
        self.stored_text = self.text
        self.scrollable = False
        self.search_history = False

        self.open_amount = "CLOSED"
        self.target_openess = 0
        self.y = 0

        self.layer = "layer_999"
        self.pause = False
        self.mouse_wheel_offset = 0
        self.autocomplete_text = ""
        self.letter_rect = renderer.text_rect("A", (0, 0, 0))

    def set_openess(self, amount):
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
        renderer.draw_quad((0, 0), (Display.x, self.y), (39, 40, 34))

    def draw_textfield(self):
        renderer.draw_quad((0, self.y - 22), (Display.x, 22), (60, 61, 56))

    def draw_text(self):
        renderer.draw_text(self.text, (5, self.y - 20), (255, 175, 0))

    def draw_autocomplete_suggestion(self):
        autocomplete_difference = self.autocomplete_text[len(self.text):]
        renderer.draw_text(autocomplete_difference, (5 + self.cursor_max * self.letter_rect.width, self.y - 20), (120, 80, 0))

    def draw_cursor(self):
        cursor_position = 5 + self.cursor_index * self.letter_rect.width
        if _globals.cursor_underscored:
            renderer.draw_quad((cursor_position, self.y), (8, 0), self.cursor_color)
        else:
            renderer.draw_quad((cursor_position, self.y - 20), (10, 18), self.cursor_color)

    def draw_history(self):
        for i, text in enumerate(reversed(_globals.history_output)):
            text_rect = renderer.text_rect(text, (255, 175, 0))
            text_rect.x = 5
            text_rect.y = self.y - 45 - (20 * i) + self.mouse_wheel_offset
            if text_rect.y < 0:
                self.scrollable = True
            else:
                self.scrollable = False
            if text_rect.y < self.y - 20:
                renderer.draw_text(text, text_rect, (255, 175, 0))

    def add_text_at_cursor(self, key):
        left = self.text[:self.cursor_index]
        right = self.text[self.cursor_index:]
        self.text = left + key + right
        if self.cursor_index >= 0:
            self.cursor_index += 1
        else:
            self.cursor_index = 1

    def remove_text_at_cursor(self):
        if self.cursor_index > 0:
            left = self.text[:self.cursor_index-1]
            right = self.text[self.cursor_index:]
            self.text = left + right

            if self.cursor_index > 0:
                self.cursor_index -= 1

    def run_command(self, text):
        run_command(text)
        self.text = ""
        self.history_index = None
        self.cursor_index = 0

    def autocomplete_input_history(self):
        self.cursor_color = (200, 50, 50)
        commands_found = []
        for command in _globals.history_input:
            found = False
            for index, letter in enumerate(self.text):
                if index < len(command):
                    if letter == command[index]:
                        found = True
                    else:
                        found = False
                        break

            if not found:
                if command in commands_found:
                    commands_found.remove(command)
                continue
            if found and command not in commands_found:
                commands_found.append(command)
            elif command in commands_found:
                commands_found.remove(command)

        if len(self.text) > 0 and len(commands_found) > 0:
            commands_found.sort()
            self.autocomplete_text = commands_found[0]
        else:
            self.autocomplete_text = ""

    def autcomplete_known_commands(self):
        self.cursor_color = (200, 200, 200)
        commands_found = []
        for command in get_commands():
            found = False
            for index, letter in enumerate(self.text):
                if len(self.text) <= len(command.name):
                    if letter == command.name[index]:
                        found = True
                    else:
                        found = False
                        break

            if found and command.name not in commands_found:
                commands_found.append(command.name)
            elif command.name in commands_found:
                commands_found.remove(command.name)

        if len(self.text) > 0 and len(commands_found) > 0:
            commands_found.sort()
            self.autocomplete_text = commands_found[0]
        else:
            self.autocomplete_text = ""

    def update(self, dt):
        #self.history_length = len(_globals.history_input)

        #if events.key_pressed_once("K_ESCAPE", "layer_999"):
        #    self.set_openess("CLOSED")
        #    layer.pop_layer()

        #if events.key_pressed_once("K_BACKQUOTE", "layer_all") and events.key_pressed("K_LSHIFT", "layer_all"):
        #    if self.open_amount == "MAX":
        #        self.set_openess("CLOSED")
        #        layer.pop_layer()
        #    else:
        #        self.set_openess("MAX")
        #        layer.set_layer("layer_999")

        #if events.key_pressed_once("K_BACKQUOTE", "layer_all") and not events.key_pressed("K_LSHIFT", "layer_all"):
        #    if self.open_amount == "MIN":
        #        self.set_openess("CLOSED")
        #        layer.pop_layer()
        #    else:
        #        self.set_openess("MIN")
        #        layer.set_layer("layer_999")

        #self.animate_console(dt)
        if self.y > 0:
            if mouse.get_pos()[1] < self.y:
                if events.mouse_wheel_down:
                    if self.mouse_wheel_offset != 0:
                        self.mouse_wheel_offset -= 20
                if events.mouse_wheel_up:
                    if self.scrollable:
                        self.mouse_wheel_offset += 20

            #key = events.text_input_repeat("layer_999")
            #key = events.text_input("layer_999")
            #if key and key != "`":
            #    self.add_text_at_cursor(key)

            #if events.key_pressed_repeat("K_BACKSPACE", "layer_999"):
                #self.remove_text_at_cursor()

            #if events.key_pressed_once("K_RETURN", "layer_999") and len(self.text):
            #    self.search_history = False
            #    run_command(self.text)
            #    self.text = ""
            #    self.history_index = None
            #    self.cursor_index = 0

            #if events.key_pressed_repeat("K_LEFT", "layer_999"):
                #if self.cursor_index > 0:
                    #self.cursor_index -= 1
            #if events.key_pressed_repeat("K_RIGHT", "layer_999"):
                #if self.cursor_index < self.cursor_max:
                    #self.cursor_index += 1

            #if events.key_pressed_once("K_UP", "layer_999"):
            #    if self.history_index is None:
            #        self.history_index = self.history_length
            #        self.stored_text = self.text
            #    if self.history_index > 0:
            #        self.history_index -= 1
            #    if len(_globals.history_input):
            #        self.text = _globals.history_input[self.history_index]
            #        self.cursor_max = len(self.text)
            #        self.cursor_index = self.cursor_max
            #if events.key_pressed_once("K_DOWN", "layer_999"):
            #    if self.history_index is not None:
            #        self.history_index += 1
            #        if self.history_index >= self.history_length:
            #            self.history_index = None
            #            self.text = self.stored_text
            #            self.stored_text = ""
            #        else:
            #            self.text = _globals.history_input[self.history_index]
            #        self.cursor_max = len(self.text)
            #        self.cursor_index = self.cursor_max

            #if events.key_pressed_once("K_HOME", "layer_999"):
            #    self.cursor_index = 0
            #if events.key_pressed_once("K_END", "layer_999"):
                self.cursor_index = self.cursor_max
            if events.key_pressed_once("K_TAB", "layer_999"):
                self.text = self.autocomplete_text
                self.cursor_index = len(self.text)
            if events.key_pressed("K_LCTRL", "layer_all") and events.key_pressed_once("K_r", "layer_all"):
                self.search_history = True

            if self.search_history:
                self.autocomplete_input_history()
            else:
                self.autcomplete_known_commands()

            self.cursor_max = len(self.text)

            #self.draw_background()
            #self.draw_textfield()
            #self.draw_history()
            #self.draw_text()
            #self.draw_autocomplete_suggestion()
            #self.draw_cursor()


#console = Console()
