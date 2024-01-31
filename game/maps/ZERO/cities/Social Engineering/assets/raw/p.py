from PIL import Image
"""
read 'img1.png', and process it:
iterate each pixel, if black, 1, else 0.
then, print out as '*' for 1, ' ' for 0.
"""

def process_image():
    image_path = 'img1.png'
    image = Image.open(image_path)
    width, height = image.size

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            if pixel[1] > 127:  # assuming black pixels
                print('\u2588', end='')
            else:
                print(' ', end='')
        print()  # new line after each row

process_image()

