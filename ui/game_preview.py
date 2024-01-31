import yaml

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


storage = {}


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
        300,
        text="  IP: " + str(settings["ip"]),
        fill="black",
        font=("Consolas", 12),
        anchor="nw",
    )

    # Display the manual URI
    canvas.create_text(
        150,
        360,
        text="View Mission Manual",
        fill="#82c7ff",
        font=("Consolas", 12, "underline"),
        anchor="center",
    )


def onclick(e):
    """
    Handle the click event.
    """
    x, y = e.x, e.y

    # Check for links
    link_area = [(60, 340), (240, 380)]
    if link_area[0][0] <= x <= link_area[1][0] and link_area[0][1] <= y <= link_area[1][1]:
        # TODO: open the manual
        ...


def display(canvas, name):
    """
    Display the preview box.
    """
    # Load
    load_preview(f"{kingdom_dir}cities/{name}/preview.yaml")

    # Draw
    display_info(canvas)


# Load Map Settings (Just Temporary)
kingdom_dir = "game/maps/ZERO/"
