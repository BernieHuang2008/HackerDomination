import shell
import yaml

SESSION = {
    "prof": {"user": "guest", "name": "guest@PLee", "addr": "222.248.208.208"},
    "dir": "/home/guest",
    "game": {
        "city": "Empire ZERO, Ciry of the Sun",
    },
}

OS = yaml.safe_load(open("data/os.yaml", "r", encoding="utf-8"))


def init(*args):
    # sync
    shell.sync(SESSION, OS)

    # sync APIs
    shell.allow_input = args[0]
    shell.forbid_input = args[1]
    shell.print = args[2]
    shell.input = args[3]


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
    init(
        allow_input,
        forbid_input,
        print,
        input,
    )

    # start shell
    shell.start()

    # start terminal
    terminal.api["mainloop"]()


if __name__ == "__main__":
    start()
