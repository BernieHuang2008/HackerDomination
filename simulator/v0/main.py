SESSION = {
    "prof": {"name": "Hacker1@Empire", "addr": "222.248.208.208"},
    "dir": "/home/Hacker",
}


def init():
    pass


def start_prepare():
    pass


def check_pass():
    pass


def process(cmd):
    pass


def start():
    while not check_pass():
        print(
            f"\033[1;32m{SESSION['prof']['name']}\033[0m:\033[1;34m{SESSION['dir']}\033[0m$ ",
            end="",
        )
        cmd = input()
        process(cmd)


if __name__ == "__main__":
    init()
    start_prepare()
    start()
