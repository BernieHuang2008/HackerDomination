OS = {}


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


def supercode(c):
    """
    supercode
    """
    code = c[3:-3]
    code = code.replace(" ", "")

    fields = code.split(":")

    if fields[0] == "FILE":
        return open(
            SESSION["data"] + "files/" + fields[1], "r", encoding="utf-8"
        ).read()


class FSBasicObject:
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
        self.size = 0

    def colorname(self, user):
        LS_COLORS = "rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36"
        LS_COLORS = dict(
            tuple(color.split("=")) for color in LS_COLORS.strip().split(":")
        )

        for rule in LS_COLORS:
            if self.match(rule, user):
                return f"\033[{LS_COLORS[rule]}m{self.name}\033[0m"

    def match(self, rule, user):
        """
        check if self matches the LS_COLORS rule
        """
        if rule.startswith("*."):
            return self.name.endswith(rule[1:])
        elif rule == "di":
            return type(self).__name__ == "Folder"
        elif rule == "ex":
            return ispermitted(getpath(self), "x", user)
        elif rule == "ow":
            return ispermitted(getpath(self), "w", user)
        else:
            return False


class File(FSBasicObject):
    def __init__(self, name, data, parent):
        super().__init__(name, data, parent)

        self.size = len(self.content)

    def _content(self, c):
        """
        process content
        """
        if c.startswith("__!"):
            return supercode(c)

        return c


class Folder(FSBasicObject):
    def __init__(self, name, data, parent):
        super().__init__(name, data, parent)

        self.size = sum([c.size for c in self.content.values()])

    def _content(self, c):
        """
        process content
        """
        for name, data in c.items():
            c[name] = Auto(name, data, self)

        return c


def Auto(name, data, parent):
    if data["type"] == "file":
        return File(name, data, parent)
    elif data["type"] == "dir":
        return Folder(name, data, parent)


def init():
    global root
    fs = OS["filesystem"]
    root = Folder("/", {"content": fs}, None)
    root.parent = root  # special case


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
            return False  # Exception("path not exist")

        curr = curr.content[name]

    return curr


def getpath(obj):
    if obj == root:
        return "/"
    else:
        return join(getpath(obj.parent), obj.name)


def join(*args):
    def cleaning(dirname):
        if dirname.startswith(".") and not dirname.startswith(".."):
            dirname = dirname[1:]
        return dirname

    args = list(map(cleaning, args))
    return "/".join(args).replace("//", "/")


def clean(path):
    return getpath(access(path))


def isdir(path):
    return type(access(path)).__name__ == "Folder"


def isfile(path):
    return type(access(path)).__name__ == "File"


def ispermitted(path, mode, user):
    obj = access(path)

    # not support group
    if obj.owner == user:
        return all(m in obj.permission[0:3] for m in mode)
    else:
        return all(m in obj.permission[6:9] for m in mode)
