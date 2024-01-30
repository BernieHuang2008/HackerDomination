OS = {}


def sync(session, os):
    """
    sync session and os
    """
    # sync os
    global OS
    OS = os


def supercode(c):
    """
    supercode
    """
    code = c[3:-3]
    code = code.replace(" ", "")

    fields = code.split(":")

    if fields[0] == "FILE":
        return open("data/files/" + fields[1], "r", encoding="utf-8").read()


class File:
    def __init__(self, name, data, parent):
        # default
        default = {"owner": "system", "permission": "rwx------", "content": {}}
        default.update(data)
        data = default

        self.name = name
        self.owner = data["owner"]
        self.permission = data["permission"]
        self.content = self._content(data["content"])
        self.parent = parent

    def _content(self, c):
        """
        process content
        """
        if c.startswith("__!"):
            return supercode(c)

        return c


class Folder:
    def __init__(self, name, data, parent):
        # default
        default = {"owner": "system", "permission": "rwx------", "content": {}}
        default.update(data)
        data = default

        self.name = name
        self.owner = data["owner"]
        self.permission = data["permission"]
        self.content = self._content(data["content"])
        self.parent = parent

        # init ls table
        self.ls = [
            {
                "name": n,
                "owner": self.owner,
                "permission": c.permission,
                "type": type(c).__name__,
            }
            for n, c in self.content.items()
        ]

    def _content(self, c):
        """
        process content
        """
        for name, data in c.items():
            c[name] = Auto(name, data, self)

        return c


def Auto(name, data, parent):
    if type(data) != dict:
        pass
    if data["type"] == "file":
        return File(name, data, parent)
    elif data["type"] == "dir":
        return Folder(name, data, parent)


def init():
    global root
    fs = OS["filesystem"]
    root = Folder("root", {"content": fs}, None)
    root.parent = root  # special case

    for name, data in fs.items():
        fs[name] = Auto(name, data, root)


def access(path):
    if path[0] != "/":
        raise Exception("path must be absolute")
    else:
        path = path.strip("/")  # by the way, also remove '/' at the end
    path = path.split("/")

    curr = root

    for name in path:
        name = name.strip()

        if name == "..":
            curr = curr.parent
            continue

        if name not in curr.content:
            raise Exception("path not exist")

        curr = curr.content[name]

    return curr


def getpath(obj):
    if obj == root:
        return "/"
    else:
        return join(getpath(obj.parent), obj.name)


def join(*args):
    return "/".join(args).replace("//", "/")


def clean(path):
    return getpath(access(path))


def isdir(path):
    return type(access(path)).__name__ == "Folder"


def ispermited(path, mode, user):
    obj = access(path)

    # not support group
    if obj.owner == user:
        return all(m in obj.permission[0:3] for m in mode)
    else:
        return all(m in obj.permission[6:9] for m in mode)
