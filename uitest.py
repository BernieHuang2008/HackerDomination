import tkinter as tk

import ui.kingdom_map as testmd


def main_menu(canvas):
    canvas.destroy()
    display_tk()

def display_tk():
    root = tk.Tk()

    root.title("Map")
    root.geometry("800x600")
    root.resizable(False, False)
    root.attributes("-topmost", False)
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()

    SCALE_WIDTH = 1600 / SCREEN_WIDTH
    SCALE_HEIGHT = 1000 / SCREEN_HEIGHT
    MIN_SCALE = min(SCALE_WIDTH, SCALE_HEIGHT)

    canvas = tk.Canvas(root, width=1600, height=1000)
    canvas.scale("all", 0, 0, MIN_SCALE, MIN_SCALE)
    canvas.pack()

    canvas.bind("<Escape>", lambda _: main_menu(canvas))

    testmd.display(canvas, root)
    canvas.bind("<Button-1>", testmd.onclick)
    
    root.mainloop()


if __name__ == "__main__":
    display_tk()
