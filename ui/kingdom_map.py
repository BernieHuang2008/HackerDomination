import yaml
import tkinter as tk

from graph import Graph
from graph import graph_py

import progress
import ui.game_preview as game_preview

# These variables will be set by 'main' later
PAD = (0, 0)
SCALE = 1000 / 600  # base scale

graph = None
SETTINGS = {
    "screen-width": 1600,
    "screen-height": 1000,
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

PROGRESS = progress.read_kingdom_progress("ZERO")


storage = {}


def init(kingdom_dir):
    """
    Initialize the map.
    """
    SETTINGS["kingdom-dir"] = kingdom_dir

    """Helper Functions"""

    def load_ui():
        with open(kingdom_dir + "ui.yaml", "r") as f:
            ui = yaml.safe_load(f)
            SETTINGS["ui"] = ui["map"]

    def load_about():
        with open(kingdom_dir + "about.yaml", "r") as f:
            about = yaml.safe_load(f)
            SETTINGS["about"] = about

    def load_graph():
        global graph
        graph = Graph.from_json(kingdom_dir + "graph.json")

    def init_start_city():
        """
        Initialize the start city.
        """
        graph.add_node("__START__", [0, 1000])
        graph.add_edge("__START__", SETTINGS["about"]["city"]["start"])

        PROGRESS["captured"]["list"].append("__START__")

    """Load"""
    load_ui()
    load_about()
    load_graph()

    """Init"""
    init_start_city()


def apply_style():
    """
    Apply style to the graph module.
    """

    def apply_node(n, style):
        n["custom"] = {
            "node_size": style["radius"] * 2,
            "node_color": style["color"],
            "border_color": style["border"],
            "border_width": style["borderWidth"],
            "text_size": SETTINGS["textSize"],
        }

    for name, node in graph.nodes.items():
        if name in PROGRESS["captured"]["list"]:
            apply_node(node, SETTINGS["ui"]["city"]["captured"])
        elif "capital" in node.properties and node["capital"] is True:
            apply_node(node, SETTINGS["ui"]["city"]["capital"])
        else:
            apply_node(node, SETTINGS["ui"]["city"]["ordinary"])

    graph_py.SETTINGS["text_color"] = SETTINGS["ui"]["textColor"]
    graph_py.SETTINGS["edge_width"] = SETTINGS["ui"]["road"]["width"]
    graph_py.SETTINGS["edge_color"] = SETTINGS["ui"]["road"]["color"]


def display_bg(canvas):
    """
    Display the background of the map.
    """
    global storage

    if "bg" not in storage:
        bg_name = SETTINGS["ui"]["background"]
        bg_path = SETTINGS["kingdom-dir"] + "assets/" + bg_name
        bg = tk.PhotoImage(file=bg_path)
        canvas.create_image(0, 0, image=bg, anchor="nw")
        storage["bg"] = bg
    else:
        canvas.create_image(0, 0, image=storage["bg"], anchor="nw")


def widget_rect(i):
    settings = SETTINGS["widget"]

    x1 = settings["xpad"]
    y1 = i * (settings["height"] + settings["ypad"]) + settings["ypad"]
    x2 = x1 + settings["width"]
    y2 = y1 + settings["height"]

    return x1, y1, x2, y2


def display_widgets(canvas, root):
    """
    Display the widgets of the map.
    """

    def f_return():
        # TODO: return to the previous page
        root.destroy()
        root.quit()

    global widgets
    widgets = [
        ("\uE0D5", f_return),
    ]

    settings = SETTINGS["widget"]

    for i in range(len(widgets)):
        name, func = widgets[i]

        # Draw the widget
        x1, y1, x2, y2 = widget_rect(i)
        canvas.create_rectangle(x1, y1, x2, y2, outline=settings["border"], width=3)
        canvas.create_text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            text=name,
            fill=settings["border"],
            font=settings["font"],
        )


def get_city_status(name):
    """
    Get the status of a city.
    """
    target = graph.nodes[name]

    if name in PROGRESS["captured"]["list"]:
        return "captured"

    if any(x in PROGRESS["captured"]["list"] for x in target.neighbors()):
        return "contested"

    return "locked"


def open_preview(target):
    """
    Open the preview page.
    """
    global storage

    name, target = target, graph.nodes[target]

    pos = target.pos
    pos = [pos[0] * SCALE + 150, pos[1] * SCALE]
    top = pos[1]
    right = SETTINGS["screen-width"] - pos[0]

    status = get_city_status(name)

    # P1 = left-top
    preview_size = [300, 400]
    if right >= preview_size[0]:
        x1 = pos[0]
    else:
        x1 = pos[0] - preview_size[0]
    if top >= preview_size[1]:
        y1 = pos[1] - preview_size[1]
    else:
        y1 = pos[1]

    pos = [x1 + PAD[0], y1 + PAD[1]]

    # create canvas
    can2 = tk.Canvas(
        storage["root"],
        width=preview_size[0],
        height=preview_size[1],
        bg=SETTINGS["ui"]["preview-bg"],
        highlightthickness=0,
    )
    can2.place(x=pos[0], y=pos[1])
    game_preview.display(can2, name, status, close_preview)

    storage["preview"] = can2
    storage["preview-target"] = name


def close_preview(is_passed=False):
    """
    Close the preview page.
    """
    if "preview" in storage:
        # Update progress
        name = storage["preview-target"]
        if is_passed and name not in PROGRESS["captured"]["list"]:
            PROGRESS["captured"]["list"].append(name)
            progress.write_kingdom_progress("ZERO", PROGRESS)

        # Destroy
        storage["preview"].destroy()
        del storage["preview"]
        del storage["preview-target"]

        # Redraw
        display(storage["canvas"], storage["root"])


def onclick(e):
    """
    Handle the click event.
    """
    x, y = e.x, e.y
    sx = (x - 150) / SCALE
    sy = y / SCALE

    # Check for game preview
    if "preview" in storage:
        close_preview()

    # Check for widgets
    # widgets won't be scaled, so no need to scale back
    for i in range(len(widgets)):
        x1, y1, x2, y2 = widget_rect(i)
        if x1 <= x <= x2 and y1 <= y <= y2:
            widgets[i][1]()
            return

    # Check for nodes
    target = graph_py.find_node(graph, sx, sy)  # remove offset
    if target is not None:
        open_preview(target)


def display(canvas=None, root=None):
    """
    Display the map.
    """
    # Use default values
    if "canvas" not in storage:
        storage["canvas"] = canvas
        storage["root"] = root
    else:
        canvas = canvas or storage["canvas"]
        root = root or storage["root"]

    # Clear
    canvas.delete("all")

    # Draw
    apply_style()
    display_bg(canvas)
    graph.draw(canvas, clearprev=False, offset=(150, 0), scale=SCALE)
    display_widgets(canvas, root)


# Load Map Settings (TODO: Just Temporary)
init("game/maps/ZERO/")
