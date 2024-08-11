import math

from PIL import Image, ImageDraw


def create_round_corner_mask(image, radius):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = image.size

    draw.rounded_rectangle(
        [(0, 0), (width, height)], radius=radius, fill=255
    )

    if image.mode == 'RGBA':
        alpha_channel = image.getchannel(3)

        mask = Image.composite(mask, alpha_channel, mask)

    # if image.mode == 'RGBA':
    #     for x in range(width):
    #         for y in range(height):
    #             min_alpha = min(image.getpixel((x, y))[3], mask.getpixel((x, y)))
    #             draw.point((x, y), fill=min_alpha)
    return mask


async def draw_ray(image, start_point, angle_degrees, color='black'):
    length = image.size[0]
    # 计算射线的终点
    angle_radians = math.radians(angle_degrees)
    end_x = start_point[0] + length * math.cos(angle_radians)
    end_y = start_point[1] - length * math.sin(angle_radians)
    end_point = (end_x, end_y)

    # 在图像上绘制射线
    draw = ImageDraw.Draw(image)
    draw.line([start_point, end_point], fill=color, width=2)

    angle_degrees += 180
    angle_radians %= 360

    angle_radians = math.radians(angle_degrees)
    end_x = start_point[0] + length * math.cos(angle_radians)
    end_y = start_point[1] - length * math.sin(angle_radians)
    end_point = (end_x, end_y)

    # 在图像上绘制射线
    draw = ImageDraw.Draw(image)
    draw.line([start_point, end_point], fill=color, width=2)


async def draw_rounded_rectangle(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy

    radius = min(radius, (x1 - x0) / 2, (y1 - y0) / 2)

    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)

    draw.rectangle([x0 + radius, y0, x1 - radius, y0 + radius], fill=fill)
    draw.rectangle([x0 + radius, y1 - radius, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x0 + radius, y1 - radius], fill=fill)
    draw.rectangle([x1 - radius, y0 + radius, x1, y1 - radius], fill=fill)

    draw.rectangle([x0 + radius, y0 + radius, x1 - radius, y1 - radius], fill=fill)
