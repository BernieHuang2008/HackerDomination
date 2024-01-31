from tkinter import Tk, Text, Scrollbar, END
import re

# Create a new Tkinter window
window = Tk()
window.geometry("960x540")  # Set the window size to hold 80x30 characters
window.title("Terminal - Hacker Domination")

# Create Text widget as terminal window
text = Text(window, bg="black", fg="white")
text.pack(fill="both", expand=True)

text.configure(insertbackground="white", font=("Consolas", 12))


def fake_print(s="", end="\n"):
    def get_lc(content, pos):
        """
        Get line (l) and column (c) of a position in the content
        """
        line = content[:pos].count("\n")
        col = pos - content[:pos].rfind("\n") - 1
        return line, col

    # Process 033
    content, styles = dash033(s + end)
    cline, ccol = map(int, text.index("insert").split("."))  # backup
    text.insert(END, content)

    # Color & Print
    for i in range(len(styles)):
        s1 = styles[i]
        s2 = styles[i + 1] if i + 1 < len(styles) else None

        pos1, style = s1["pos"], s1["style"]
        pos2 = s2["pos"] if s2 is not None else len(content)

        # Get line and column
        line1, col1 = get_lc(content, pos1)
        line2, col2 = get_lc(content, pos2)

        # Add Tags
        tname = f"style_{style['fg']}_{style['bg']}_{style['bold']}"
        text.tag_add(
            tname,
            f"{cline + line1}.{col1+(ccol if line1==0 else 0)}",
            f"{cline + line2}.{col2+(ccol if line2==0 else 0)}",
        )

        # Config Tags
        text.tag_config(
            tname,
            foreground=style["fg"],
            background=style["bg"],
            font=("Consolas", 12, "bold" if style["bold"] else "normal"),
        )

    # Set forbid delete
    global forbid_delete
    cline, ccol = map(int, text.index("insert").split("."))
    forbid_delete = ccol


def dash033(content):
    def process_color_code(s):
        codesheet = {
            0: "black",
            1: "red",
            2: "#23d18b",  # green
            3: "yellow",
            4: "#3b8eea",  # blue
            5: "magenta",
            6: "cyan",
            7: "white",
        }

        # Parameters
        codes = s[2:-1].split(";")
        codes = list(map(int, codes))
        color = {
            "fg": "white",
            "bg": "black",
            "bold": False,
        }

        # Process
        for code in codes:
            c1 = code // 10
            c2 = code % 10
            if c1 == 3:
                color["fg"] = codesheet[c2]
            elif c1 == 4:
                color["bg"] = codesheet[c2]
            elif c1 == 0:
                if c2 == 0:
                    color["fg"] = "white"
                    color["bg"] = "black"
                    color["bold"] = False
                if c2 == 1:
                    color["bold"] = True

        return color

    styles = []
    cursor = 0
    counted = 0
    while True:
        # Find next color code
        match = re.search(r"\033\[[0-9;]+m", content[cursor:])
        if match is None:
            break

        # Store
        styles.append(
            {
                "pos": cursor - counted + match.start(),
                "style": process_color_code(match.group()),
            }
        )
        cursor += match.end()

        # Count
        counted += match.end() - match.start()

    # Remove color codes
    content = re.sub(r"\033\[[0-9;]+m", "", content)

    return content, styles


def handle_input(event):
    global forbid_delete
    global command_cursor

    # Stop input
    forbid_input()

    # Move cursor to the end
    text.mark_set("insert", END)

    # Get current line
    line = text.get("insert linestart", "insert lineend")
    uinput = line[forbid_delete:]

    # History
    if uinput != "":
        api["history"].append(uinput)
        command_cursor = -1

    # New Line
    text.insert("insert", "\n")

    # Process
    api["process"](uinput)

    # Resume input
    allow_input()
    return "break"


def handle_backspace(event):
    global forbid_delete

    # Get current line and column
    line, col = map(int, text.index("insert").split("."))

    if col <= forbid_delete:
        return "break"


def handle_up(event):
    global command_cursor
    if command_cursor == 0:
        return "break"
    elif command_cursor == -1:
        command_cursor = len(api["history"]) - 1
        cline, ccol = map(int, text.index("insert").split("."))
        text.delete(f"{cline}.{forbid_delete}", "insert lineend")
        text.insert("insert", api["history"][command_cursor])
        return "break"
    else:
        command_cursor -= 1
        cline, ccol = map(int, text.index("insert").split("."))
        text.delete(f"{cline}.{forbid_delete}", "insert lineend")
        text.insert("insert", api["history"][command_cursor])
        return "break"


def handle_down(event):
    global command_cursor
    if command_cursor == -1:
        return "break"
    elif command_cursor == len(api["history"]) - 1:
        command_cursor = -1
        cline, ccol = map(int, text.index("insert").split("."))
        text.delete(f"{cline}.{forbid_delete}", "insert lineend")
        return "break"
    else:
        command_cursor += 1
        cline, ccol = map(int, text.index("insert").split("."))
        text.delete(f"{cline}.{forbid_delete}", "insert lineend")
        text.insert("insert", api["history"][command_cursor])
        return "break"


def allow_input():
    global g_allow_input
    g_allow_input = True


def forbid_input():
    global g_allow_input
    g_allow_input = False


def fake_input(callback):
    def fake_cb(s):
        # Restore
        api["process"] = bk_processor
        forbid_input()

        # Call callback
        callback(s)

    # Start input
    allow_input()
    bk_processor = api["process"]
    api["process"] = fake_cb


def clear():
    global command_cursor
    command_cursor = -1
    api["history"] = []
    text.delete("1.0", END)


# Bind events
text.bind("<Key>", lambda e: "break" if not g_allow_input else None)
text.bind("<Return>", handle_input)
text.bind("<BackSpace>", handle_backspace)
text.bind("<Left>", handle_backspace)
text.bind("<Up>", handle_up)
text.bind("<Down>", handle_down)


api = {
    # Provided
    "ch-title": lambda s: window.title(s),
    "print": fake_print,
    "input": fake_input,
    "clear": clear,
    "mainloop": window.mainloop,
    "input-allow": allow_input,
    "input-forbid": forbid_input,
    "exit": lambda: [window.destroy(), window.quit()],
    # Variables
    "history": [],
    # Required
    "process": None,
}
command_cursor = -1
forbid_input()
