import base64
from io import BytesIO

from nonebot import on_command, CommandSession, MessageSegment
from PIL import Image, ImageDraw, ImageFont
from os import path

import math
import random


class Const:
    def __init__(self):
        self.ENLARGE_TIME = 2
        self.MAX_PARAMETER_NUM = 20
        self.LOWER_RAND_LIMIT = 1
        self.UPPER_RAND_LIMIT = 100
        self.BACKGROUND_COLOR = (4, 62, 88)
        self.FOREGROUND_COLOR = (248, 248, 248)
        self.LINE_WIDTH = 2 * self.ENLARGE_TIME
        self.CIRCLE_WIDTH = 3 * self.ENLARGE_TIME
        self.FONT_SIZE = 14 * self.ENLARGE_TIME
        # 指上侧标题栏
        self.IMAGE_LABEL_HEIGHT = 50 * self.ENLARGE_TIME
        # 指下侧主画布区
        self.IMAGE_MAIN_BORDER_LENGTH = 360 * self.ENLARGE_TIME
        # 外圈圆半径
        self.CIRCLE_OUTSIDE_RADIUS = 130 * self.ENLARGE_TIME
        # 原点坐标
        self.ORIGIN = (self.IMAGE_MAIN_BORDER_LENGTH / 2, self.IMAGE_MAIN_BORDER_LENGTH / 2 + self.IMAGE_LABEL_HEIGHT)
        self.IMAGE_SIZE = (self.IMAGE_MAIN_BORDER_LENGTH, self.IMAGE_MAIN_BORDER_LENGTH + self.IMAGE_LABEL_HEIGHT)


const = Const()


@on_command('今日人品', aliases='人品', only_to_me=False)
async def get_luck_today(session: CommandSession):
    parameter_list = session.current_arg_text.strip()
    image = draw_luck_image(parameter_list.split(' ', const.MAX_PARAMETER_NUM))
    base64_str = await image_to_base64(image)
    await session.send(MessageSegment.image(file='base64://' + str(base64_str, 'utf-8')))


async def image_to_base64(image):
    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str


def draw_luck_image(parameter_list: list):
    image = Image.new('RGB', const.IMAGE_SIZE, const.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image, mode='RGB')

    draw_circle(draw, const.CIRCLE_OUTSIDE_RADIUS)

    list_size = len(parameter_list)
    angle = 360 / list_size

    last_point_coordinate = None
    first_point_coordinate = None
    luck = None

    draw_polygon_inside(draw, list_size)

    for i in range(list_size):
        luck = random.randint(const.LOWER_RAND_LIMIT, const.UPPER_RAND_LIMIT)
        x, y = get_coordinate(int(luck / 100 * const.CIRCLE_OUTSIDE_RADIUS), angle * i)

        if last_point_coordinate:
            draw.line(((last_point_coordinate[0], last_point_coordinate[1]), (x, y)),
                      fill=const.FOREGROUND_COLOR, width=const.LINE_WIDTH, joint='curve')
        else:
            first_point_coordinate = (x, y)

        parameter = parameter_list[i]
        draw_text_outside(draw, parameter, luck, angle * i)

        last_point_coordinate = (x, y)

    draw.line(((last_point_coordinate[0], last_point_coordinate[1]),
               (first_point_coordinate[0], first_point_coordinate[1])),
              fill=const.FOREGROUND_COLOR, width=const.LINE_WIDTH, joint='curve')

    if list_size == 1:
        draw_circle(draw, int(luck / 100 * const.CIRCLE_OUTSIDE_RADIUS))

    image = image.resize((int(const.IMAGE_SIZE[0] / const.ENLARGE_TIME), int(const.IMAGE_SIZE[1] / const.ENLARGE_TIME)),
                         Image.ANTIALIAS)
    return image


# 内圈连了每个点的多边形
def draw_polygon_inside(draw: ImageDraw, list_size: int):
    if 8 > list_size > 2:
        angle = 360 / list_size

        last_point_coordinate = None
        first_point_coordinate = None

        for i in range(list_size):
            x, y = get_coordinate(const.CIRCLE_OUTSIDE_RADIUS, angle * i)

            if last_point_coordinate:
                draw.line(((last_point_coordinate[0], last_point_coordinate[1]), (x, y)),
                          fill=const.FOREGROUND_COLOR, width=const.LINE_WIDTH, joint='curve')
            else:
                first_point_coordinate = (x, y)

            last_point_coordinate = (x, y)

        draw.line(((last_point_coordinate[0], last_point_coordinate[1]),
                   (first_point_coordinate[0], first_point_coordinate[1])),
                  fill=const.FOREGROUND_COLOR, width=const.LINE_WIDTH, joint='curve')


# 指外圈文字的绘制
def draw_text_outside(draw: ImageDraw, parameter: str, luck: int, angle: float):
    font_path = path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), 'font', 'msyh.ttc')
    font = ImageFont.truetype(font_path, size=const.FONT_SIZE)

    x, y = get_coordinate(const.CIRCLE_OUTSIDE_RADIUS + const.FONT_SIZE, angle)

    if not parameter:
        parameter = '运气'
    parameter_size = len(parameter)

    radian = get_radian(angle)

    # 注意这里角度是自x正半轴顺时针
    if 270 > angle > 90:
        x += math.cos(radian) * (parameter_size - 1) * const.FONT_SIZE
    x -= const.FONT_SIZE / 2
    if 360 > angle > 180:
        y -= const.FONT_SIZE
    y -= const.FONT_SIZE

    draw.text((x, y), parameter + '\n' + str(luck), font=font, fill=const.FOREGROUND_COLOR)


# 获取坐标
def get_coordinate(radius: int, angle: float):
    radian = get_radian(angle)

    x = math.cos(radian) * radius + const.ORIGIN[0]
    y = math.sin(radian) * radius + const.ORIGIN[1]
    return x, y


def get_radian(angle: float):
    return math.pi * angle / 180


# 指以原点为中点画圆
def draw_circle(draw: ImageDraw, radius: int):
    draw.arc((const.ORIGIN[0] - radius, const.ORIGIN[1] - radius,
              (const.ORIGIN[0] + radius, const.ORIGIN[1] + radius)),
             0, 360, fill=const.FOREGROUND_COLOR, width=const.CIRCLE_WIDTH)
