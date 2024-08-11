import asyncio

from PIL import Image, ImageDraw, ImageFont
from os import path

import math
import random

from config.constant import font_path
from utils.draw_utils import draw_rounded_rectangle

start_y = 20 * 2
start_x = 20 * 2

label_height = 40 * 2

circle_background_side = 320 * 2
circle_background_width = circle_background_side + start_x * 2

image_width = circle_background_width
image_height = image_width + label_height + start_y * 2

label_font_size = 30 * 2
content_font_size = 14 * 2

line_width = 2 * 2
circle_line_width = 3 * 2

circle_outside_radius = 130 * 2

origin_x = image_width // 2
origin_y = (image_width + label_height) // 2 + start_y * 2

msyh_font_path = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), 'font', 'msyh.ttc')

label_font = ImageFont.truetype(font_path, label_font_size)
content_font = ImageFont.truetype(msyh_font_path, content_font_size)


async def draw_luck_image(name, parameter_list):
    image = Image.new('RGB', (image_width, image_height), '#2c2b2b')
    draw = ImageDraw.Draw(image, mode='RGB')

    draw.text((20, 20), f"{name}的今日人品", fill='white', font=label_font)

    await draw_rounded_rectangle(draw,
                                 (start_x, start_y + label_height, image_width - start_x, image_height - start_y),
                                 fill='#545353', radius=15)

    draw_circle(draw, circle_outside_radius)

    list_size = len(parameter_list)
    angle = 360 / list_size

    last_point_coordinate = None
    first_point_coordinate = None
    luck = None

    sum_luck = 0

    draw_polygon_inside(draw, list_size)

    for i in range(list_size):
        luck = random.randint(1, 100)

        sum_luck += luck

        x, y = get_coordinate(int(luck / 100 * circle_outside_radius), angle * i)

        if last_point_coordinate:
            draw.line(((last_point_coordinate[0], last_point_coordinate[1]), (x, y)),
                      fill="white", width=line_width, joint='curve')
        else:
            first_point_coordinate = (x, y)

        parameter = parameter_list[i]
        draw_text_outside(draw, parameter, luck, angle * i)

        last_point_coordinate = (x, y)

    draw.line(((last_point_coordinate[0], last_point_coordinate[1]),
               (first_point_coordinate[0], first_point_coordinate[1])),
              fill="white", width=line_width, joint='curve')

    if list_size == 1:
        draw_circle(draw, int(luck / 100 * circle_outside_radius))

    image = image.resize((image_width // 2, image_height // 2), Image.Resampling.LANCZOS)

    return image


def draw_polygon_inside(draw: ImageDraw, list_size: int):
    if 8 > list_size > 2:
        angle = 360 / list_size

        last_point_coordinate = None
        first_point_coordinate = None

        for i in range(list_size):
            x, y = get_coordinate(circle_outside_radius, angle * i)

            if last_point_coordinate:
                draw.line(((last_point_coordinate[0], last_point_coordinate[1]), (x, y)),
                          fill='white', width=line_width, joint='curve')
            else:
                first_point_coordinate = (x, y)

            last_point_coordinate = (x, y)

        draw.line(((last_point_coordinate[0], last_point_coordinate[1]),
                   (first_point_coordinate[0], first_point_coordinate[1])),
                  fill='white', width=line_width, joint='curve')


def draw_text_outside(draw: ImageDraw, parameter: str, luck: int, angle: float):
    x, y = get_coordinate(circle_outside_radius + content_font_size, angle)

    if not parameter:
        parameter = '运气'
    parameter_size = len(parameter)

    radian = get_radian(angle)

    if 270 > angle > 90:
        x += math.cos(radian) * (parameter_size - 1) * content_font_size
    x -= content_font_size / 2
    if 360 > angle > 180:
        y -= content_font_size
    y -= content_font_size

    draw.text((x, y), parameter + '\n' + str(luck), font=content_font, fill="white")


def get_coordinate(radius: int, angle: float):
    radian = get_radian(angle)

    x = math.cos(radian) * radius + origin_x
    y = math.sin(radian) * radius + origin_y
    return x, y


def get_radian(angle: float):
    return math.pi * angle / 180


def draw_circle(draw: ImageDraw, radius: int):
    draw.arc((origin_x - radius, origin_y - radius,
              (origin_x + radius, origin_y + radius)),
             0, 360, fill="white", width=circle_line_width)


if __name__ == "__main__":
    parameter_list = ['1', '2', '3', '4']
    # for i in range(10):
    #     parameter_list.append(str(i))
    #     image = draw_luck_image(parameter_list)
    #     image.show()

    image = asyncio.run(draw_luck_image("cnm", parameter_list))
    image.show()
