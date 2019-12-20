import json
import os

from flux import _globals
from flux.poly import Poly

commands = {}


class CommandInfo:
    tooltip = ""
    name = None
    proc = None
    arg_count_min = None
    arg_count_max = None


def init_commands():
    add_command("editor", command_editor, tooltip="enables/disables editor mode")
    add_command("save_level", command_save_level, 1, 1, tooltip="saves the current level to a file")
    add_command("new_level", command_new_level, tooltip="creates a blank new level")
    add_command("level", command_level, 1, 1, tooltip="loads level")
    add_command("quit", command_quit, tooltip="quit the engine")
    add_command("exit", command_quit, tooltip="quit the engine")
    add_command("clear", command_clear, tooltip="clears console history")
    add_command("help", command_help, 0, 1, tooltip="lists all commands")
    add_command("cursor_underscored", command_cursor_underscored, 1, 1, tooltip="changes whether the cursor is underscored or full (0, 1)")
    add_command("selection_data", command_selection_data, tooltip="shows selection data")


def get_commands():
    return commands.values()


def get_commands_names():
    return commands.keys()


def get_command(command_name):
    if command_name in commands.keys():
        return commands[command_name]

    return None


def run_command(command_string):
    command_array = list(filter(None, command_string.split(" ")))
    if not len(command_array):
        return

    command_name = command_array[0]
    command_arguments = command_array[1:]
    command_input(command_string)

    command = get_command(command_name)
    if command is not None:
        command.proc(command_arguments)
    else:
        command_output("Uknown command \"%s\"" % command_name)


def add_command(name, proc, arg_count_min=0, arg_count_max=0, tooltip=""):
    info = CommandInfo()
    info.name = name
    info.proc = proc
    info.arg_count_min = arg_count_min
    info.arg_count_max = arg_count_max
    info.tooltip = tooltip
    commands[str(name)] = info


def command_output(command):
    _globals.history_output.append(str(command))


def command_input(command):
    _globals.history_input.append(command)


def command_ls(arguments):
    command_output("We called ls with arguments: %s" % arguments)
    command_output("We called ls!!")


def command_clear(arguments):
    _globals.history_output = []
    command_output("history cleared!")


def command_quit(arguments):
    command_output("We called quit. existing flux!")
    _globals.running = False


def command_editor(arguments):
    if len(arguments) == 0:
        command_output("\"editor\" = \"%s\"" % _globals.editor)
    elif arguments[0] == "0" or arguments[0] == "1":
        _globals.editor = int(arguments[0])
        command_output("\"editor\" = \"%s\"" % _globals.editor)
    else:
        command_output("invalid arguments. 0 or 1")


def command_cursor_underscored(arguments):
    if len(arguments) == 0:
        command_output("\"cursor_underscored\" = \"%s\"" % _globals.cursor_underscored)
    elif arguments[0] == "0" or arguments[0] == "1":
        _globals.cursor_underscored = int(arguments[0])
        command_output("\"cursor_underscored\" = \"%s\"" % _globals.cursor_underscored)
    else:
        command_output("invalid arguments. 0 or 1")


def command_selection_data(arguments):
    if len(arguments) == 0:
        if _globals.get_selection() is not None:
            command_output("\"selection_data\" = \"%s\"" % _globals.get_selection().points)
        else:
            command_output("No selection found")
    else:
        command_output("command takes 0 arguments")


def command_save_level(arguments):
    if len(arguments) == 1:
        path = os.path.join(os.getcwd(), "levels", str(arguments[0]))

        data = {"poly": []}
        with open(path, "w") as f:
            for poly in _globals.poly_dict:
                poly_data = {"name": poly.name, "layer": poly.layer, "color": poly.color, "points": poly.points, "width": poly.width}
                data["poly"].append(poly_data)
            #figure out how to indent but not indent lists
            json.dump(data, f)
    else:
        command_output("command takes 1 argument of filename")


def command_level(arguments):
    if len(arguments) == 1:
        path = os.path.join(os.getcwd(), "levels", str(arguments[0]))

        if os.path.exists(path):
            _globals.poly_dict = []
            _globals.selection = None
            with open(path, "r") as f:
                data = json.load(f)
                for obj in data["poly"]:
                    poly = Poly(obj["name"], obj["layer"], obj["color"], obj["points"], None, obj["width"])
                    _globals.poly_dict.append(poly)
        else:
            command_output("filename %s does not exist" % str(arguments[0]))
    else:
        command_output("command takes 1 argument of filename")


def command_new_level(arguments):
    if len(arguments) == 0:
        _globals.poly_dict = []
        _globals.selection = None
        _globals.selection_list = []
    else:
        command_output("command takes 0 argument of filename")


def command_help(arguments):
    if arguments:
        command = get_command(arguments[0])
        if command is not None:
            command_output(command.name + " - " + command.tooltip)
        else:
            command_output(str(arguments[0]) + " - Unkown command")
    else:
        for command in get_commands():
            command_output(command.name + " - " + command.tooltip)
