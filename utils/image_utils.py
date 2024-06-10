import asyncio
import base64
from io import BytesIO

import requests
from PIL import Image, ImageOps
from nonebot.adapters.onebot.v11 import MessageSegment


async def download_image(image_url):
    if image_url is not None:
        response = requests.get(image_url)

        count = 0
        while count < 5:
            if response.status_code == 200:
                image_data = response.content

                return BytesIO(image_data)

                # image = Image.open(BytesIO(image_data))

                # image.show()

            else:
                count += 1
                print("无法获取文件内容, 次数: " + str(count))
    return None


# def get_cv2_image_with_url(image_url):
#     base_p = download_image(image_url)
#     if base_p is not None:
#         base = cv2.imread(base_p)
#         base = cv2.resize(base, (1080, int(base.shape[0] * 1080 / base.shape[1])), interpolation=cv2.INTER_LANCZOS4)
#         return base
#     return None

async def gif_to_png_list(image):
    png_list = []
    duration_list = []
    last_duration = 40

    while True:
        png_io = BytesIO()

        cur = image.tell()

        image.save(png_io, format="PNG")

        if 'duration' in image.info:
            cur_duration = image.info['duration']
            duration_list.append(cur_duration)
            last_duration = cur_duration
        else:
            duration_list.append(last_duration)

        png_list.append(png_io)

        try:
            image.seek(cur + 1)
        except EOFError:
            break

    return png_list, duration_list


def sync_gif_to_png_list(image):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(gif_to_png_list(image))


async def change_non_transparent_alpha(image, scale):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    alpha_channel = image.getchannel(3)

    alpha_channel = alpha_channel.point(lambda i: int(i * scale))

    return Image.composite(image, Image.new('RGBA', image.size, (0, 0, 0, 0)), alpha_channel)


def image_to_square(image):
    # 401 367
    width, height = image.size

    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    if width > height:
        border_height = (width - height) // 2

        if border_height % 2 == 1:
            r = ImageOps.expand(image, border=(0, border_height, 0, border_height + 1), fill=(0, 0, 0, 0))
        else:
            r = ImageOps.expand(image, border=(0, border_height, 0, border_height), fill=(0, 0, 0, 0))
    else:
        border_width = (height - width) // 2

        if border_width % 2 == 1:
            r = ImageOps.expand(image, border=(border_width, 0, border_width + 1, 0), fill=(0, 0, 0, 0))
        else:
            r = ImageOps.expand(image, border=(border_width, 0, border_width, 0), fill=(0, 0, 0, 0))

    return r


async def find_quote_image(msg):
    # if msg[0].type == 'quote':
    #     quote_msg = get_msg(-1)
    return None


async def mirror_image(image, reverse=False):
    width, height = image.size

    if reverse:
        right_half = image.crop((width // 2, 0, width, height))

        right_half_flipped = right_half.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        image.paste(right_half_flipped, (0, 0))
    else:
        left_half = image.crop((0, 0, width // 2, height))

        left_half_flipped = left_half.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        image.paste(left_half_flipped, (width // 2, 0))

    return image


async def base64_to_message_segment(base64_string):
    base64_str = f'base64://{base64.b64encode(base64_string.getvalue()).decode()}'
    return MessageSegment.image(file=base64_str)
