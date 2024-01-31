"""
Supported commands:
cd, ls, cat, cp, mov, rm, cp, mkdir, echo, clear, exit
"""

import shlex
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
        f"\033[1;32m{SESSION['prof']['name']}@{SESSION['prof']['host']}\033[0m:\033[1;34m{SESSION['dir']}\033[0m$ ",
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


def parse(paras: str):
    """
    Parse parameters
    """
    flags = set()
    paras = shlex.split(paras)
    para = []
    for p in paras:
        if p.startswith("-"):
            for c in p[1:]:
                flags.add(c)
        else:
            para.append(p)
    return flags, para


def cmd_cd(paras: str):
    global SESSION
    bk_dir = SESSION["dir"]

    if paras == "" or paras == "~":
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
    if not fs.ispermitted(SESSION["dir"], "x", SESSION["prof"]["user"]):
        print("Permission denied.")
        SESSION["dir"] = bk_dir
        return

    # clean path
    SESSION["dir"] = fs.clean(SESSION["dir"])


def cmd_clear(paras: str):
    api["clear"]()


def cmd_exit(paras: str):
    api["exit"]()


def cmd_ls(paras: str):
    global SESSION

    # Parse para
    flags, paras = parse(paras)
    if len(paras) == 0:
        paras = ["."]

    target = paras[0]
    target = fs.join(SESSION["dir"], target)

    if not fs.access(target):
        print("No such file or directory.")
        return
    if not fs.isdir(target):
        print("Not a directory.")
        return
    if not fs.ispermitted(target, "x", SESSION["prof"]["user"]):
        print("Permission denied.")
        return

    target = fs.clean(target)

    fsdir = fs.access(SESSION["dir"])
    display = []
    for n, f in fsdir.content.items():
        # hidden files
        if n.startswith(".") and "a" not in flags:
            continue
        # 'l' flag
        if "l" in flags:
            display.append(
                [f.permission, f.owner, f.size, f.colorname(SESSION["prof"]["user"])]
            )
        else:
            display.append(f.colorname(SESSION["prof"]["user"]))

    # sort
    r = "r" in flags
    if "S" in flags:
        display.sort(key=lambda x: x[2], reverse=r)

    # print
    if "l" in flags:
        print(f"total {len(display)}")

        displayT = list(map(list, zip(*display)))
        maxlen = []
        for i in range(len(displayT)):
            maxlen.append(max(map(lambda x: len(str(x)), displayT[i])))

        for row in display:
            for i in range(len(row)):
                print(str(row[i]).ljust(maxlen[i]), end=" ")
            print()

    else:
        print(" ".join(display))


def cmd_cat(paras: str):
    global SESSION

    # Parse para
    flags, paras = parse(paras)
    if len(paras) == 0:
        print("cat: missing file operand")
        return
    elif len(paras) > 1:
        print("cat: too many arguments")
        return

    # get target file name
    target = paras[0]
    target = fs.join(SESSION["dir"], target)

    # check
    if not fs.access(target):
        print("No such file or directory.")
        return
    if not fs.ispermitted(target, "r", SESSION["prof"]["user"]):
        print("Permission denied.")
        return
    if not fs.isfile(target):
        print("Target not a file.")
        return

    # print content
    lines = fs.access(target).content.split("\n")

    if "s" in flags:
        for i in range(1, len(lines)):
            if lines[i] == "" and lines[i - 1] == "":
                lines[i] = None
        lines = list(filter(lambda x: x is not None, lines))

    if "b" in flags:
        nonblank = list(filter(lambda x: x != "", lines))
        max_num_len = len(str(len(nonblank)))
        for i in range(len(lines)):
            if lines[i] != "":
                lines[i] = str(i + 1).rjust(max_num_len) + "  " + lines[i]
            else:
                lines[i] = " " * (max_num_len + 2) + lines[i]

    elif "n" in flags:
        max_num_len = len(str(len(lines)))
        for i in range(len(lines)):
            lines[i] = str(i + 1).rjust(max_num_len) + "  " + lines[i]

    if "E" in flags:
        for i in range(len(lines)):
            lines[i] += "$"

    if "T" in flags:
        for i in range(len(lines)):
            lines[i] = lines[i].replace("\t", "^I")

    print("\n".join(lines))


commands = {
    "cd": cmd_cd,
    "clear": cmd_clear,
    "exit": cmd_exit,
    "ls": cmd_ls,
    "cat": cmd_cat,
}
