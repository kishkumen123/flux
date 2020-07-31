import pygame
import string


pygame.font.init()

running = True
history_output = ["Welcome to the Console!", "I like banana caramel milk shakes - (>:;)", "loooooooooooooooooooooooooooooooooooooooooooolcicles", "1", "2", "3", "4", "5", "6", "7", "asd", "rf", "qweq", "1", "2", "3", "4", "5", "6", "7", "asd", "rf", "qweq", "1", "2", "3", "4", "5", "6", "7", "asd", "rf", "qweq"]
history_input = []
editor = 1
selection = None
font = pygame.font.SysFont("consolas", 18)

should_ignore_input = 0

# @incomplete- this needs to go away once we make textinput events
textinput_list = string.digits + string.ascii_letters + string.punctuation + " "
textinput_list = textinput_list.replace("`", "")
textinput_list = textinput_list.replace("~", "")
