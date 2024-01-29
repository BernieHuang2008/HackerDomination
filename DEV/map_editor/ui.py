import os, sys
import tkinter as tk

sys.path.append(os.path.abspath('../../'))
print(sys.path)
if 1:
    from graph import Graph
    from graph import find_node

SETTINGS = {
    "node_size": 10,
}


def ui(g: Graph):
    ret = False

    # Create the main window
    root = tk.Tk()
    root.title("Graph Editor")
    # Set window size to 600x700
    root.geometry("600x700")
    # Create the matplotlib canvas where the graph will be drawn
    canvas = tk.Canvas(master=root)
    canvas.update()
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # Create the toolbar for the matplotlib canvas
    toolbar = tk.Frame(master=root)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    # Set toolbar height to 100
    toolbar.config(height=100)

    # Create the button to restart the graph ui
    def restart():
        nonlocal ret
        ret = True
        root.destroy()
        root.quit()

    restart_button = tk.Button(master=toolbar, text="Refersh", command=restart)
    restart_button.pack(side=tk.LEFT)
    # Create the button to save the graph
    save_button = tk.Button(
        master=toolbar, text="Save", command=lambda: g.save("graph.json")
    )
    save_button.pack(side=tk.LEFT)
    # Create the button to load the graph
    load_button = tk.Button(master=toolbar, text="Load")
    load_button.pack(side=tk.LEFT)
    # Create the button to set capital
    capital_button = tk.Button(
        master=toolbar, text="Capital", command=lambda: set_capital(g)
    )
    capital_button.pack(side=tk.LEFT)
    # Bind the canvas to add a new node to the graph
    canvas.bind("<Button-3>", lambda e: add_node(e, g))
    # Bind the canvas to select a node
    canvas.bind("<Button-1>", lambda e: select_node(e, g))
    # Bind the canvas dragging to move the selected node
    canvas.bind("<B1-Motion>", lambda e: move_node(e, g))
    # Bind the 'delete' key to delete the selected node
    root.bind("<Delete>", lambda _: del_node())
    # Bind the 'f5' key to restart the graph ui
    root.bind("<F5>", lambda _: restart())
    # Draw the initial graph
    g.draw(canvas)
    # Start the main loop
    root.mainloop()

    return ret


def input(prompt):
    # Create the input window
    win = tk.Tk()
    win.title("Input")
    # Set window size to 200x100
    win.geometry("200x100")
    # Display the prompt
    prompt_label = tk.Label(master=win, text=prompt)
    prompt_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # Create the input field
    input_field = tk.Entry(master=win)
    input_field.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # Create the button to submit the input
    input_value = None

    def ret():
        nonlocal input_value
        input_value = input_field.get()
        win.destroy()
        win.quit()

    submit_button = tk.Button(master=win, text="Submit", command=ret)
    submit_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
    # Loose focus, return.
    win.bind("<FocusOut>", lambda _: ret())
    # Bind the enter key to submit the input
    win.bind("<Return>", lambda _: ret())

    # Focus input
    input_field.focus_force()
    # Start the main loop
    win.mainloop()
    # Return the input
    return input_value


def add_node(event, g: Graph):
    # Function: clear select
    selected_nodes.clear()
    # Get the position of the mouse click
    x = event.x
    y = event.y
    # Create the node
    name = input("Node Name:")
    g.add_node(name, [x, y])
    g.draw()


selected_nodes = []


def select_node(event, g: Graph):
    # Get the position of the mouse click
    x = event.x
    y = event.y

    r = SETTINGS["node_size"] / 2
    nodes = []
    for name, node in g.nodes.items():
        if abs(x - node.pos[0]) <= 2 * r and abs(y - node.pos[1]) <= 2 * r:
            nodes.append(name)

    target = find_node(g, x, y)
    if target is None:
        return

    selected_nodes.append(target)

    if len(selected_nodes) == 2:
        if selected_nodes[0] != selected_nodes[1]:
            g.add_edge(selected_nodes[0], selected_nodes[1])
        selected_nodes.clear()
        g.draw()


def move_node(event, g: Graph):
    # print(len(g.edges))
    # Get the position of the mouse click
    x = event.x
    y = event.y

    target = find_node(g, x, y)
    if target is not None:
        g.nodes[target].pos = [x, y]
        g.draw()


def del_node():
    if len(selected_nodes) > 0:
        target = selected_nodes.pop()
        g.remove_node(target)
        g.draw()


def set_capital(g: Graph):
    name = input("Capital:")
    g.nodes[name].properties["capital"] = True
    g.draw()


if __name__ == "__main__":
    if os.path.exists("graph.json"):
        g = Graph.from_json("graph.json")
    else:
        g = Graph()

    # Main loop
    while ui(g):
        pass
