import shell
import yaml


def init(session):
    global OS, SESSION
    SESSION = session
    OS = yaml.safe_load(open(SESSION["data"] + "os.yaml", "r", encoding="utf-8"))


def init_shell(api):
    # sync
    shell.sync(SESSION, OS)

    # sync APIs
    shell.api = api
    shell.allow_input = api["input-allow"]
    shell.forbid_input = api["input-forbid"]
    shell.print = api["print"]
    shell.input = api["input"]


def start_prepare():
    pass


def check_pass():
    pass


def start():
    global print, input

    import terminal

    terminal.api["process"] = shell.shell

    # APIs
    allow_input = terminal.api["input-allow"]
    forbid_input = terminal.api["input-forbid"]
    print = terminal.api["print"]
    input = terminal.api["input"]

    # init shell
    init_shell(terminal.api)

    # start shell
    shell.start()

    # start terminal
    terminal.api["mainloop"]()
