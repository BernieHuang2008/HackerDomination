import shell
import yaml

SESSION = {
    "prof": {"user": "guest", "name": "guest@PLee", "addr": "222.248.208.208"},
    "dir": "/home/guest",
    "game": {
        "city": "Empire ZERO, Ciry of the Sun",
    },
}

OS = yaml.safe_load(open("simulator/v0/data/os.yaml", "r", encoding="utf-8"))


def init(api):
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
    init(terminal.api)

    # start shell
    shell.start()

    # start terminal
    terminal.api["mainloop"]()


if __name__ == "__main__":
    start()
