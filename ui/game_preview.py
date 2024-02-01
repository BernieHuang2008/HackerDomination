import yaml
import markdown
import tkinter as tk
import tkinterweb as th3
import threading
import json

import ui.shell_starter as shell_starter
import progress

SETTINGS = {
    "textSize": 12,
    "widget": {
        "border": "#d4be73",
        "width": 50,
        "xpad": 30,
        "ypad": 20,
        "height": 50,
        "font": ("MWF MDL2 Assets", 20, "bold"),
    },
}


storage = {"kingdom_dir": "game/maps/ZERO/"}  # just temp


def load_preview(fname):
    with open(fname, "r") as f:
        ui = yaml.safe_load(f)
        SETTINGS["preview_page"] = ui


def widget_rect(i):
    settings = SETTINGS["widget"]

    x1 = settings["xpad"]
    y1 = i * (settings["height"] + settings["ypad"]) + settings["ypad"]
    x2 = x1 + settings["width"]
    y2 = y1 + settings["height"]

    return x1, y1, x2, y2


def autosplit(text, width):
    """
    Split the text into lines automatically.
    """
    lines = []
    line = ""
    for word in text.split(" "):
        if len(line) + len(word) > width:
            if width - len(line) >= 3 and len(line) + len(word) - width >= 3:
                line += word[:2] + "-"
                lines.append(line)
                line = word[2:]
            else:
                lines.append(line)
                line = word
        else:
            line += " " + word
    lines.append(line)

    lines = "\n".join(lines)
    lines = "  " + lines.strip()  # indent
    return lines


def display_info(canvas):
    """
    Display the information of the map.
    """
    settings = SETTINGS["preview_page"]

    # Display the title
    canvas.create_text(
        150,
        20,
        text=settings["name"],
        fill="#d4be73",
        font=("Consolas", 15, "bold underline italic"),
        anchor="center",
    )

    # Display the description
    canvas.create_text(
        10,
        40,
        text=autosplit(settings["description"], 30),
        fill="#d4be73",
        font=("Consolas", 12),
        anchor="nw",
    )

    # Display IP info
    canvas.create_text(
        10,
        250,
        text="IP: " + str(settings["ip"]),
        fill="#cf4d68",
        font=("Consolas", 12),
        anchor="nw",
    )

    # Display the manual URI
    canvas.create_text(
        150,
        310,
        text="View Mission Manual",
        fill="#82c7ff",
        font=("Consolas", 12, "underline"),
        anchor="center",
    )

    # Display the start button
    canvas.create_rectangle(60, 350, 240, 390, fill="#096aae", width=0)
    canvas.create_text(
        150,
        370,
        text="START",
        fill="white",
        font=("Times", 20, "bold"),
        anchor="center",
    )


def onclick(e):
    """
    Handle the click event.
    """
    x, y = e.x, e.y

    # Check for links
    link_area = [(60, 290), (240, 330)]
    if (
        link_area[0][0] <= x <= link_area[1][0]
        and link_area[0][1] <= y <= link_area[1][1]
    ):
        with open(
            f"{storage['kingdom_dir']}cities/{storage['name']}/assets/manual.md", "r"
        ) as f:
            md_text = f.read()
        html = markdown.markdown(md_text)

        # Start render
        def f():
            window = tk.Tk()
            bx = window.winfo_screenwidth() - 500
            by = window.winfo_screenheight() - 700
            window.geometry("500x700+{}+{}".format(bx // 2, by // 2))
            window.title("Mission Manual")

            frame = th3.HtmlFrame(window, messages_enabled=False)
            frame.load_html(html)
            frame.pack(fill="both", expand=True)

            window.mainloop()

        thread = threading.Thread(target=f)
        thread.start()

    # check for "start" button
    start_area = [(60, 350), (240, 390)]
    if (
        start_area[0][0] <= x <= start_area[1][0]
        and start_area[0][1] <= y <= start_area[1][1]
    ):
        prog = progress.read_main_progress()
        all_term = prog["terminals"]["list"]
        shell_list = {}

        for shell_ip in all_term:
            with open(f"game/machines/{shell_ip}/info.json") as f:
                shell_info = json.load(f)

            # Get Info
            hostname = shell_info["Hostname"]

            # Init shellcfg list
            shell_list[hostname] = [shell_ip]

        shell_starter.init(shell_list)
        shell_starter.render()


def display(canvas, name):
    """
    Display the preview box.
    """
    # Store
    storage["name"] = name

    # Load
    load_preview(f"{storage['kingdom_dir']}cities/{name}/preview.yaml")

    # Draw
    display_info(canvas)

    # Bind
    canvas.bind("<Button-1>", onclick)
