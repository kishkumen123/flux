import globals

commands = []


class CommandInfo:
    tooltip = ""
    name = None
    proc = None
    arg_count_min = None
    arg_count_max = None


def init_commands():
    add_command("ls", command_ls, 1, 1, "doesnt do anything usefull")
    add_command("quit", command_quit, tooltip="quit the engine")
    add_command("clear", command_clear, tooltip="clears console history")
    add_command("help", command_help, 0, 1, tooltip="lists all commands")


def run_command(command_string):

    command_array = list(filter(None, command_string.split(" ")))
    if not len(command_array): return

    command_name = command_array[0]
    non_command_arguments = command_array[1:]
    argument_count = len(non_command_arguments)
    command_input(command_string)

    for command in commands:
        if command_name == command.name:

            if argument_count < command.arg_count_min or argument_count > command.arg_count_max:
                min_string = "" if command.arg_count_min == 1 else "s"
                max_string = "" if command.arg_count_max == 1 else "s"
                if command.arg_count_min == command.arg_count_max:
                    command_output("Error: %s requires exactly %s argument%s - %s given" % (command_name, command.arg_count_min, min_string, argument_count))
                    return
                command_output("Error: %s requires at least %s argument%s and at most %s argument%s - %s given" % (command_name, command.arg_count_min, min_string, command.arg_count_max, max_string, argument_count))
                return

            command.proc(non_command_arguments)
            return
    command_output("Command [%s] not known" % command_name)


def add_command(name, proc, arg_count_min=0, arg_count_max=0, tooltip=""):
    info = CommandInfo()
    info.name = name
    info.proc = proc
    info.arg_count_min = arg_count_min
    info.arg_count_max = arg_count_max
    info.tooltip = tooltip
    commands.append(info)


def command_output(command):
    globals.history_output.append(command)


def command_input(command):
    globals.history_input.append(command)


def command_a(arguments):
    command_output("We called a with arguments: %s" % arguments)


def command_b(arguments):
    command_output("We called b with arguments: %s" % arguments)


def command_c(arguments):
    command_output("We called c with arguments: %s" % arguments)


def command_ls(arguments):
    command_output("We called ls with arguments: %s" % arguments)
    command_output("We called ls!!")


def command_clear(arguments):
    globals.history_output = []
    command_output("history cleared!")


def command_quit(arguments):
    command_output("We called quit. existing flux!")
    globals.running = False


def command_help(arguments):
    if arguments:
        found = False
        for command in commands:
            if command.name == arguments[0]:
                command_output(command.name + " - " + command.tooltip)
                found = True

        if not found:
            command_output(str(arguments[0]) + " - Unkown command")
    else:
        for command in commands:
            command_output(command.name + " - " + command.tooltip)


# TODO: logs to console
def log():
    pass
