import tkinter as tk

import ui.kingdom_map as testmd


def display_tk():
    root = tk.Tk()
    root.title("Map")
    root.geometry("800x600")
    root.resizable(False, False)
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()
    img = testmd.display(canvas, root)  # 持续引用,否则会被回收
    canvas.bind("<Button-1>", testmd.onclick)
    root.mainloop()


if __name__ == "__main__":
    display_tk()
