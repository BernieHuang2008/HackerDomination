import tkinter as tk
import ui.kingdom_map as testmd
import progress


storage = {}
MAIN_PROGRESS = None
MAX_SCALE = 1


def main_menu(canvas):
    """
    Display the main menu.
    """
    global MAX_SCALE

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
        # Parameters
        SCREEN_WIDTH = 1600
        SCREEN_HEIGHT = 1000
        WIDTH = 200
        HEIGHT = 50
        TEXTSIZE = 20
        YPAD = 5

        # Scale
        # fmt: off
        SCREEN_WIDTH    *= MAX_SCALE
        SCREEN_HEIGHT   *= MAX_SCALE
        WIDTH           *= MAX_SCALE
        HEIGHT          *= MAX_SCALE
        TEXTSIZE        = int(TEXTSIZE * MAX_SCALE)
        YPAD            *= MAX_SCALE
        # fmt: on

        # Calculate
        x1, x2 = (SCREEN_WIDTH - WIDTH) / 2, (SCREEN_WIDTH + WIDTH) / 2
        TOTALHEIGHT = len(menu) * HEIGHT + (len(menu) - 1) * YPAD
        YBIAS = (SCREEN_HEIGHT - TOTALHEIGHT) / 2

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
    global MAX_SCALE

    root = tk.Tk()

    # Set up window
    root.title("Map")
    root.resizable(False, False)
    root.attributes("-topmost", False)
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    # Screen Parameters
    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()

    # Scale
    SCALE_WIDTH = SCREEN_WIDTH / 1600
    SCALE_HEIGHT = SCREEN_HEIGHT / 1000
    MAX_SCALE = max(SCALE_WIDTH, SCALE_HEIGHT)
    MIN_SCALE = min(SCALE_WIDTH, SCALE_HEIGHT)
    WIDTH = 1600 * MIN_SCALE
    HEIGHT = 1000 * MIN_SCALE

    # Padding
    XPAD = (SCREEN_WIDTH - WIDTH) // 2
    YPAD = (SCREEN_HEIGHT - HEIGHT) // 2

    # Create canvas
    canvas = tk.Canvas(root, width=1600, height=1000, highlightthickness=0)
    canvas.place(x=XPAD, y=YPAD, width=WIDTH, height=HEIGHT)

    # Bind Events
    root.bind("<Escape>", lambda _: main_menu(canvas))

    # Display Map & Widgets
    testmd.PAD = (XPAD, YPAD)
    testmd.SCALE *= MAX_SCALE
    testmd.display(canvas, root)
    storage["onclick"] = testmd.onclick
    canvas.bind("<Button-1>", testmd.onclick)

    root.mainloop()


if __name__ == "__main__":
    # TODO: update MAIN_PROGRESS more frequently
    MAIN_PROGRESS = progress.read_main_progress()
    display_tk()
