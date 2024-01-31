import tkinter as tk
import ui.kingdom_map as testmd


storage = {}


def main_menu(canvas):
    """
    Display the main menu.
    """

    # Functions
    def f_resume(e):
        root = canvas.master
        for item in all_items:
            canvas.delete(item)
        root.bind("<Escape>", lambda _: main_menu(canvas))
        canvas.bind("<Button-1>", storage["onclick"])

    def f_shutdown(e):
        root = canvas.master
        root.destroy()
        root.quit()

    # Menu
    menu = [("RESUME", f_resume), ("SHUTDOWN", f_shutdown)]
    all_items = []

    def display_on_center():
        # Calculate
        WIDTH = 200
        x1, x2 = (1600 - WIDTH) / 2, (1600 + WIDTH) / 2
        HEIGHT = 50
        TEXTSIZE = 20
        YPAD = 5
        TOTALHEIGHT = len(menu) * HEIGHT + (len(menu) - 1) * YPAD
        YBIAS = (1000 - TOTALHEIGHT) / 2

        # Display
        for i in range(len(menu)):
            # Draw
            name, func = menu[i]
            y1 = YBIAS + i * (HEIGHT + YPAD)
            y2 = y1 + HEIGHT
            a = canvas.create_rectangle(
                x1, y1, x2, y2, fill="black", outline="#d4be73", width=1
            )
            b = canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=name,
                fill="#d4be73",
                font=("Arial", TEXTSIZE),
            )
            all_items.extend([a, b])

            # Bind
            canvas.tag_bind(a, "<Button-1>", func)
            canvas.tag_bind(b, "<Button-1>", func)

    display_on_center()

    # Bind
    root = canvas.master
    root.bind("<Escape>", f_resume)
    canvas.unbind("<Button-1>")


def display_tk():
    root = tk.Tk()

    # Set up window
    root.title("Map")
    root.geometry("800x600")
    root.resizable(False, False)
    root.attributes("-topmost", False)
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    # Screen Parameters
    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()

    # Scale
    SCALE_WIDTH = 1600 / SCREEN_WIDTH
    SCALE_HEIGHT = 1000 / SCREEN_HEIGHT
    MIN_SCALE = min(SCALE_WIDTH, SCALE_HEIGHT)
    MAX_SCALE = max(SCALE_WIDTH, SCALE_HEIGHT)
    WIDTH = 1600 / MAX_SCALE
    HEIGHT = 1000 / MAX_SCALE

    # Padding
    XPAD = (SCREEN_WIDTH - WIDTH) // 2
    YPAD = (SCREEN_HEIGHT - HEIGHT) // 2

    # Create canvas
    canvas = tk.Canvas(root, width=1600, height=1000, highlightthickness=0)
    canvas.scale("all", 0, 0, MIN_SCALE, MIN_SCALE)
    canvas.place(x=XPAD, y=YPAD, width=WIDTH, height=HEIGHT)

    # Bind Events
    root.bind("<Escape>", lambda _: main_menu(canvas))

    # Display Map & Widgets
    testmd.PAD = (XPAD, YPAD)
    testmd.display(canvas, root)
    storage["onclick"] = testmd.onclick
    canvas.bind("<Button-1>", testmd.onclick)

    root.mainloop()


if __name__ == "__main__":
    display_tk()
