"""
Supported commands:
cd, ls, cat, cp, mov, rm, cp, mkdir, echo, clear, exit
"""

import filesys as fs

def sync(session, os):
    """
    sync session and os
    """
    # sync os
    global OS
    OS = os

    # sync session
    global SESSION
    SESSION = session


def ask():
    print(
        f"\033[1;32m{SESSION['prof']['name']}\033[0m:\033[1;34m{SESSION['dir']}\033[0m$ ",
        end="",
    )
    allow_input()


def start():
    # sync with submodules
    fs.sync(SESSION, OS)

    # init submodules
    fs.init()

    # Start Shell interface
    ask()


def shell(cmd: str):
    global SESSION, OS
    
    # split command
    cmd = cmd.split(" ")
    command = cmd[0]
    paras = " ".join(cmd[1:])

    # check command
    if command in commands:
        commands[command](paras)

    # Last, ask for next command
    ask()


def cmd_cd(paras: str):
    global SESSION
    bk_dir = SESSION["dir"]

    if paras == "":
        SESSION["dir"] = "/home/" + SESSION["prof"]["user"]

    elif paras == "..":
        fsdir = fs.access(SESSION["dir"])
        if fsdir.parent == None:
            print("No parent found.")
            return
        SESSION["dir"] = fs.getpath(fsdir.parent)

    elif paras.startswith("/"):
        if not fs.access(paras):
            print("No such file or directory.")
            return
        SESSION["dir"] = paras

    else:
        abpath = fs.join(SESSION["dir"], paras)
        if not fs.access(abpath):
            print("No such file or directory.")
            return
        SESSION["dir"] = abpath

    # check is folder
    if not fs.isdir(SESSION["dir"]):
        print("Not a directory.")
        SESSION["dir"] = bk_dir
        return

    # check permission
    if not fs.permited(SESSION["dir"], "x", SESSION["prof"]["user"]):
        print("Permission denied.")
        SESSION["dir"] = bk_dir
        return

    # clean path
    SESSION["dir"] = fs.clean(SESSION["dir"])


commands = {
    "cd": cmd_cd,
}