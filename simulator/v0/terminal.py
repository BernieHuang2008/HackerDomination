from tkinter import Tk, Text, Scrollbar, END
import re

# Create a new Tkinter window
window = Tk()
window.title("Shell-Like Window")

# Create a new Text widget with a black background and white text
text = Text(window, bg="black", fg="white")
text.pack(fill="both", expand=True)

text.configure(insertbackground="white", font=("Consolas", 12))


def fake_print(s):
    def get_lc(content, pos):
        """Get line and column of a position in the content"""
        line = content[:pos].count("\n")
        col = pos - content[:pos].rfind("\n") - 1
        return line, col

    content, styles = dash033(s)
    text.insert(END, content)

    for i in range(len(styles)):
        s1 = styles[i]
        s2 = styles[i + 1] if i + 1 < len(styles) else None

        pos1, style = s1["pos"], s1["style"]
        pos2 = s2["pos"] if s2 is not None else len(content)

        # Get line and column
        line1, col1 = get_lc(content, pos1)
        line2, col2 = get_lc(content, pos2)
        cline, ccol = map(int, text.index("insert").split("."))

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


def dash033(content):
    def process_color_code(s):
        codesheet = {
            0: "black",
            1: "red",
            2: "#23d18b",   # green
            3: "yellow",
            4: "#3b8eea",   # blue
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


# Function to handle input
def handle_input(event):
    # Get the current line
    line = text.get("insert linestart", "insert lineend")
    # You can process the input here
    print(f"You entered: {line}")
    # Insert a new line
    text.insert("insert", "\n")
    fake_print("hello\n")
    fake_print(f"\033[1;32mhacker@Empire\033[0m:\033[1;34m/home/hacker\033[0m$ ")
    return "break"


def handle_backspace(event):
    # Get the current line and column
    line, column = map(int, text.index("insert").split("."))
    # If the cursor is not at the start of a line
    if column > 0:
        # Delete the previous character
        text.delete("insert-1c")

    return "break"


# Bind the Return key to the handle_input function
text.bind("<Return>", handle_input)
text.bind("<BackSpace>", handle_backspace)

# Start the Tkinter event loop
window.mainloop()
