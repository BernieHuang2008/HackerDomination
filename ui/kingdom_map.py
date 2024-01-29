import yaml
import tkinter as tk

from graph import Graph
from graph import graph_py

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

PROGRESS = {
    "captured": [],
}


def load_ui(fname):
    with open(fname, "r") as f:
        ui = yaml.safe_load(f)
        SETTINGS["ui"] = ui["map"]


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
        if name in PROGRESS["captured"]:
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
        bg_path = kingdom_dir + "assets/" + bg_name
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


def onclick(e):
    """
    Handle the click event.
    """
    x, y = e.x, e.y

    # Check for widgets
    for i in range(len(widgets)):
        x1, y1, x2, y2 = widget_rect(i)
        if x1 <= x <= x2 and y1 <= y <= y2:
            widgets[i][1]()
            return

    # Check for nodes
    target = graph_py.find_node(graph, x - 150, y)  # remove offset
    if target is not None:
        ...
        if target not in PROGRESS["captured"]:
            PROGRESS["captured"].append(target)
            display(storage["canvas"], storage["root"])


def display(canvas, root):
    """
    Display the map.
    """
    global storage
    storage = {
        "canvas": canvas,
        "root": root,
    }

    canvas.delete("all")
    apply_style()

    display_bg(canvas)
    graph.draw(canvas, offset=(150, 0), clearprev=False)
    display_widgets(canvas, root)

    return storage


kingdom_dir = "game/maps/ZERO/"
load_ui(kingdom_dir + "ui.yaml")
graph = Graph.from_json(kingdom_dir + "graph.json")
