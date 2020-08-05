import _globals
import os
from entity_manager import EM

commands = {}


class CommandInfo:
    tooltip = ""
    name = None
    proc = None
    arg_count_min = None
    arg_count_max = None

    def __getitem__(cls, index):
        return cls.name[index]

    def __len__(cls):
        return len(cls.name)


def init_commands():
    add_command("edit",     command_editor,           tooltip="enables/disables editor mode")
    add_command("save",     command_save,       tooltip="saves the current level to the folder it was loaded from")
    add_command("new_save", command_new_save, 1, 1, tooltip="saves a new level to a new specified folder")
    add_command("load",     command_load,  1, 1, tooltip="load an existing level")
    add_command("quit",     command_quit,             tooltip="quit the engine")
    add_command("exit",     command_quit,             tooltip="quit the engine")
    add_command("clear",    command_clear,            tooltip="clears console history")
    add_command("help",     command_help,       0, 1, tooltip="lists all commands")


def add_command(name, proc, arg_count_min=0, arg_count_max=0, tooltip=""):
    info = CommandInfo()
    info.name = name
    info.proc = proc
    info.arg_count_min = arg_count_min
    info.arg_count_max = arg_count_max
    info.tooltip = tooltip
    commands[str(name)] = info


def get_commands():
    return commands.values()


def get_command_names():
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


def command_output(command):
    _globals.history_output.insert(0, str(command))


def command_input(command):
    _globals.history_input.insert(0, command)


def command_ls(arguments):
    command_output("We called ls with arguments: %s" % arguments)
    command_output("We called ls!!")


def command_clear(arguments):
    _globals.history_output = []
    command_output("history cleared!")


def command_quit(arguments):
    command_output("We called quit. existing!")
    _globals.running = False


def command_editor(arguments):
    if len(arguments) == 0:
        command_output("\"editor\" = \"%s\"" % _globals.editor)
    elif arguments[0] == "0" or arguments[0] == "1":
        _globals.editor = int(arguments[0])
        command_output("\"editor\" = \"%s\"" % _globals.editor)
    else:
        command_output("invalid arguments. 0 or 1")

def command_new_save(arguments):
    path = "data/levels/"
    if arguments:
        path += str(arguments[0])
        dir_path = os.path.normpath(os.path.join(os.getcwd(), path))
        if os.path.isdir(dir_path):
            command_output("level dir %s already exists, use save" % arguments[0])
        else:
            os.mkdir(dir_path)
            for ent in EM.entities.values():
                data = ""
                items = list(ent.__dict__.items())
                for i in items:
                    if i[0] == "_id":
                        continue
                    if i[0] == "sprite":
                        data += "%s=%s\n" % (i[0], "textures[e.sprite_source]")
                    elif i[0] == "rect":
                        data += "%s=%s\n" % (i[0], "e.sprite.get_rect()")
                    elif isinstance(i[1], str):
                        data += "%s=\"%s\"\n" % (i[0], i[1])
                    else:
                        data += "%s=%s\n" % (i[0], i[1])

                file_name = "entity_%s" % ent.__dict__["_id"]
                with open(os.path.join(dir_path, file_name), "w") as f:
                    f.write(data)

            command_output("new save %s" % arguments[0])
    else:
        command_output("invalid number of arguments. Expected 1.")

def command_save(arguments):
    path = "data/levels/"
    if arguments:
        command_output("invalid number of arguments. Expected 0.")
    else:
        path += _globals.level_loaded
        dir_path = os.path.normpath(os.path.join(os.getcwd(), path))
        for ent in EM.entities.values():
            data = ""
            items = list(ent.__dict__.items())
            for i in items:
                if i[0] == "_id":
                    continue
                if i[0] == "sprite":
                    data += "%s=%s\n" % (i[0], "textures[e.sprite_source]")
                elif i[0] == "rect":
                    data += "%s=%s\n" % (i[0], "e.sprite.get_rect()")
                elif isinstance(i[1], str):
                    data += "%s=\"%s\"\n" % (i[0], i[1])
                else:
                    data += "%s=%s\n" % (i[0], i[1])

            file_name = "entity_%s" % ent.__dict__["_id"]
            with open(os.path.join(dir_path, file_name), "w") as f:
                f.write(data)

        command_output("saved %s" % _globals.level_loaded)

def command_load(arguments):
    path = "data/levels/"
    if arguments:
        path += str(arguments[0])
        dir_path = os.path.normpath(os.path.join(os.getcwd(), path))
        if _globals.level_loaded == arguments[0]:
            command_output("level %s already loaded!" % arguments[0])
        elif os.path.isdir(dir_path):
            EM.load_entities(path + "/*")
            _globals.level_loaded = arguments[0]
        else:
            command_output("path %s does not exists" % arguments[0])
    else:
        command_output("invalid number of arguments. Expected 1.")

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
