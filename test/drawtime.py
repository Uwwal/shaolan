import time

from PIL import Image, ImageDraw

from utils.draw_utils import create_round_corner_mask


def draw_rounded_rectangle_pieslice(draw, xy, radius, fill):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy

    # Ensure the radius is not greater than half the rectangle's width or height
    radius = min(radius, (x1 - x0) / 2, (y1 - y0) / 2)

    # Draw the four corners
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)  # Top-left
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)  # Top-right
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)  # Bottom-left
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)  # Bottom-right

    # Draw the four edges
    draw.rectangle([x0 + radius, y0, x1 - radius, y0 + radius], fill=fill)  # Top edge
    draw.rectangle([x0 + radius, y1 - radius, x1 - radius, y1], fill=fill)  # Bottom edge
    draw.rectangle([x0, y0 + radius, x0 + radius, y1 - radius], fill=fill)  # Left edge
    draw.rectangle([x1 - radius, y0 + radius, x1, y1 - radius], fill=fill)  # Right edge

    # Draw the center rectangle
    draw.rectangle([x0 + radius, y0 + radius, x1 - radius, y1 - radius], fill=fill)

    # Create a blank image with a white background


if __name__ == '__main__':
    width, height = 200, 200
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    xy = (50, 50, 150, 150)
    radius = 15
    fill = 'blue'

    late = time.time()
    for i in range(10000):
        draw_rounded_rectangle_pieslice(draw, xy, radius, fill)

    print(time.time() - late)

    image.show()

    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    late = time.time()
    for i in range(10000):
        image_ = Image.new('RGB', (width, height), 'blue')
        image.paste(image_,(50,50),mask=create_round_corner_mask(image_,15))

    print(time.time() - late)
