import globals


commands = []


class CommandInfo:
    name = None
    proc = None
    arg_count_min = None
    arg_count_max = None


def init_commands():
    add_command("ls", command_ls, 1, 16)
    add_command("quit", command_quit)


def run_command(command_string):

    command_array = command_string.split(" ")
    if not len(command_array): return

    command_name = command_array[0]
    non_command_arguments = command_array[1:]
    argument_count = len(non_command_arguments)

    for command in commands:
        if command_name == command.name:
            argument_string = "" if argument_count == 1 else "s"
            if argument_count < command.arg_count_min:
                print("Error: %s requires at least %s argument%s - %s given" % (command_name, command.arg_count_min, argument_string, argument_count))
                return
            command.proc(non_command_arguments)
            return
    print("Command %s - not known" % command_name)


def add_command(name, proc, arg_count_min=0, arg_count_max=0):
    info = CommandInfo()
    info.name = name
    info.proc = proc
    info.arg_count_min = arg_count_min
    info.arg_count_max = arg_count_max
    commands.append(info)


def command_output(command):
    from console import console
    console.add_to_histroy(command)


def command_ls(arguments):
    print("We called ls with arguments: %s" % arguments)
    #command_output("We called ls!!")


def command_quit(arguments):
    command_output("Quiting Flux")
    print("We called quit. existing flux!")
    globals.running = False



#init_commands()
#run_command("na")
#run_command("ls")
