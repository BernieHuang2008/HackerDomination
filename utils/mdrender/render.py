import xmlparse
import markdown
import tkinter as tk
from PIL import Image, ImageTk


def _parse(md):
    """
    Parse the markdown to html.

    Args:
        md (str): The markdown text.
    """
    # convert to ast
    html = markdown.markdown(md)
    ast = xmlparse.parse(html)
    return ast


def _render(ast):
    inline_tags = {"strong", "em", "code", "a", "span"}
    text_tags = {
        "h1": ("Segoe UI", 30, ""),
        "h2": ("Segoe UI", 25, ""),
        "h3": ("Segoe UI", 20, ""),
        "h4": ("Segoe UI", 15, ""),
        "h5": ("Segoe UI", 10, ""),
        "text": ("Segoe UI", 12, ""),
    }

    def _meansure_text(text, font, **kwargs):
        # font
        font = list(font)
        if "bold" in kwargs and "bold" not in font[2]:
            font[2] += " bold"
        if "italic" in kwargs and "italic" not in font[2]:
            font[2] += " italic"
        font = tuple(font)

        # Measure the width of the string
        width = tk.font.Font(font=font).measure(text)

        # Count the number of lines
        num_lines = text.count("\n") + 1

        # Measure the height of the string
        line_height = tk.font.Font(font=font).metrics("linespace")
        height = line_height * num_lines

        return [width, height], font

    def _cvt_image(src):
        img = Image.open(src)

        w = 480
        h = int(w / img.width * img.height)

        img = img.resize((w, h), Image.ANTIALIAS)
        tk_img = ImageTk.PhotoImage(img)

        return [w, h], ImageTk.PhotoImage(img)

    def _render_tag(tag, **kwargs):
        """
        return:
            func(canvas) -> ([w, h], canvas.create_xxx, kwargs)

        * note: args doesn't include (x, y)
        """
        tag, params, content = tag["tag"], tag["params"], tag["content"]

        if tag in text_tags:
            meansure, font = _meansure_text(content, text_tags[tag], **kwargs)
            return lambda c: [
                meansure,
                c.create_text,
                {
                    "text": content,
                    "anchor": "nw",
                    "font": font,
                    "fill": kwargs.get("fg", "#000"),
                    "background": kwargs.get("bg", "#fff"),
                },
            ]

        elif tag == "img":
            meansure, tk_img = _cvt_image(params["src"])
            return lambda c: [
                [500, meansure[1]],
                c.create_image,
                {"image": tk_img, "anchor": "center"},
            ]

        else:
            if tag in inline_tags:
                if tag == "strong":
                    kwargs["bold"] = True
                if tag == "em":
                    kwargs["italic"] = True
                if tag == "code":
                    kwargs["font"] = ("Consolas", 12, "")
                    kwargs["fg"] = "#fc5531"
                    kwargs["bg"] = "#fff1f0"

                rendered = [[c["tag"], _render_tag(c, **kwargs)] for c in content]

                def render_inline(canvas):
                    def sub(x, y):
                        for name, func in rendered:
                            m, f, k = func(canvas)
                            w, h = m
                            f(
                                canvas,
                                x,
                                y,
                                **k,
                            )
                            x += w

                    return sub


                return lambda c: [
                    [sum(r[1](c)[0][0] for r in rendered), max(r[1](c)[0][1] for r in rendered)],
                    render_inline(c),
                    {},
                ]

            else:
                


if __name__ == "__main__":
    md = """
    # Mission Manual _of **Social Engineering**_

## Background
![plee](img/plee.png)
Dr.Peter Lee is graduated from _the University of FoolBar_ with a excellent mark in _Computer Science_. “He's a genius!” his teacher said.

A few days ago, he built a server that was claimed to be **"unhackable"**. Actually, no one can! So we need your help!

## Mission
1. Hack into Peter Lee's **"unhackable server"** (host name `PLee-Unhackable`)
2. Reset the password of 'root' user
3. Close the shell, another hacker will check the server later


## Knowledge about Social Engineering
Social engineering is to use some public informations to get more information, even private information.

Here is a classic example of social engineering:

> Once, a hacker got the door number of a person. Then he called Amazon to reset the password of the victim's Amazon account. Amazon asked him to provide the door number of the victim. He has the door number, so the hacker successfully reset the password.
>
> Then, he logged in to the victim's account and download his phone number.
>
> He called Apple to reset the password of the victim's iCloud account. Apple asked him to provide the phone number. He provided the phone number and successfully reset the password.
>
> After that, he logged in to the victim's iCloud account and download his email address ...


Emm, it might be something like that, i can't remember the details.


## Hint
1. Since no one can hack into the server, maybe you should try "social engineering"?
2. To change root's password, you need to activate a "root-shell" (unlike your normal shell) then run `passwd` command.

"""
    ast = _parse(md)
    _render(ast)
