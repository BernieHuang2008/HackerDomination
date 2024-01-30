from tkinter import Tk, Text, Scrollbar, END
import re

# Create a new Tkinter window
window = Tk()
window.title("Terminal - Hacker Domination")

# Create Text widget as terminal window
text = Text(window, bg="black", fg="white")
text.pack(fill="both", expand=True)

text.configure(insertbackground="white", font=("Consolas", 12))


def fake_print(s, end="\n"):
    def get_lc(content, pos):
        """
        Get line (l) and column (c) of a position in the content
        """
        line = content[:pos].count("\n")
        col = pos - content[:pos].rfind("\n") - 1
        return line, col

    # Process 033
    content, styles = dash033(s + end)
    cline, ccol = map(int, text.index("insert").split(".")) # backup
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
            f"{cline + line1}.{col1}",
            f"{cline + line2}.{col2}",
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

    # Stop input
    forbid_input()

    # Get current line
    line = text.get("insert linestart", "insert lineend")
    uinput = line[forbid_delete:]

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

    if col > forbid_delete:
        text.delete("insert-1c")

    return "break"


def allow_input():
    text.unbind("<Key>")
    text.bind("<Return>", handle_input)
    text.bind("<BackSpace>", handle_backspace)


def forbid_input():
    text.bind("<Key>", lambda e: "break")
    text.unbind("<Return>")
    text.unbind("<BackSpace>")


def fake_input(callback):
    def f_input(s):
        # Restore processor
        api["process"] = bk_processor

        # Close input
        forbid_input()

        # Call callback
        callback(s)

    allow_input()
    bk_processor = api["process"]
    api["process"] = f_input


api = {
    # Provided
    "ch-title": lambda s: window.title(s),
    "print": fake_print,
    "input": lambda: fake_input,
    "clear": lambda: text.delete("1.0", END),
    "mainloop": window.mainloop,
    "input-allow": allow_input,
    "input-forbid": forbid_input,
    "exit": lambda: [window.destroy(), window.quit()],
    # Required
    "process": None,
}
forbid_input()
