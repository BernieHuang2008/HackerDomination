SESSION = {
    "prof": {"name": "Hacker1@Empire", "addr": "222.248.208.208"},
    "dir": "/home/Hacker",
    "game": {
        "city": "Empire ZERO, Ciry of the Sun",
    },
}


def init():
    pass


def start_prepare():
    pass


def check_pass():
    pass


def shell(cmd):
    print(f"Command: {cmd}")



def start():
    global print, input

    import terminal
    terminal.api["process"] = shell

    # APIs
    allow_input = terminal.api["input-allow"]
    forbid_input = terminal.api["input-forbid"]
    print = terminal.api["print"]
    input = terminal.api["input"]

    # Start Asking
    print(
        f"\033[1;32m{SESSION['prof']['name']}\033[0m:\033[1;34m{SESSION['dir']}\033[0m$ ",
        end="",
    )
    allow_input()

    terminal.api["mainloop"]()


if __name__ == "__main__":
    init()
    start_prepare()
    start()
