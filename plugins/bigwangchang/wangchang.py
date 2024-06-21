import random
from io import BytesIO

from PIL import Image

from utils.image_utils import mirror_image, base64_to_message_segment


def get_random_position(wc_size, bg_size):
    # temp = (500 // num) if num < 500 else 1
    # if random.randint(1, 2) == 1:
    # row = 540 - random.randint(1, min(500, i * temp + 250))
    # else:
    #    row = 540 + random.randint(1, min(500, i * temp + 250))  
    # if random.randint(1, 2) == 1:
    #    col = 540 - random.randint(1, min(500, i * temp + 250))
    # else:
    #    col = 540 + random.randint(1, min(500, i * temp + 250))

    max_x = bg_size[0] - wc_size[0]
    max_y = bg_size[1] - wc_size[1]

    if max_x < 0:
        max_x = int(bg_size[0] / 5)
    if max_y < 0:
        max_y = int(bg_size[1] / 5)

    row = random.randint(1, max_x)
    col = random.randint(1, max_y)
    return row, col


def calculate_reduce_scale(n):
    if n > 30:
        return 6
    else:
        return 1 + 0.3 * n


async def random_image(args, image_content, p, from_gif=False, sprite_continuous=None):
    # if args > 10:
    #     num = random.randint(10, args)
    # else:
    #     num = args

    if args > 300:
        num = 100
    elif args == 0:
        num = 10
    else:
        num = args

    base = Image.open(image_content)
    gif_first_run = False

    if p == '镜镜' or p == '像像':
        image = await mirror_image(base, p == '像像')

        buf = BytesIO()
        image.save(buf, format='PNG')

        if from_gif:
            return buf

        return await base64_to_message_segment(buf)

    if not from_gif:
        base = base.resize((1080, int(base.size[1] * 1080 / base.size[0])), Image.Resampling.LANCZOS)
    elif not sprite_continuous.sprite_list:
        gif_first_run = True

    bg_size = base.size

    f_wangchang = Image.open(p)

    if base.mode != 'RGBA':
        base = base.convert('RGBA')

    wc_size = f_wangchang.size

    min_side = min(bg_size)

    new_wc_size = (int(min_side / calculate_reduce_scale(args)),
                   int(wc_size[1] * min_side / calculate_reduce_scale(args) / wc_size[0]))

    f_wangchang = f_wangchang.resize(new_wc_size, Image.Resampling.LANCZOS)

    get_params_from_sprite = from_gif and not gif_first_run

    for i in range(0, num):
        cockroach_rand = random.randint(1, 10)

        random_angle = random.randint(1, 11) * 30

        if cockroach_rand > 4:
            if get_params_from_sprite:
                pos, angle = sprite_continuous.get_sprite(i, new_wc_size)
                row, col = pos
            else:
                row, col = get_random_position(new_wc_size, bg_size)
                angle = random_angle

            f_wangchang = f_wangchang.rotate(angle)

            base.paste(f_wangchang, (row, col), f_wangchang)
        else:
            tem_wc_size = (int(random.uniform(0.2, 1.5) * new_wc_size[0]),
                           int(random.uniform(0.2, 1.5) * new_wc_size[1]))

            if get_params_from_sprite:
                pos, angle = sprite_continuous.get_sprite(i, tem_wc_size)
                row, col = pos
            else:
                row, col = get_random_position(tem_wc_size, bg_size)
                angle = random_angle

            f_new = f_wangchang.resize(tem_wc_size, Image.Resampling.LANCZOS)
            f_new = f_new.rotate(angle)

            base.paste(f_new, (row, col), f_new)

        if gif_first_run:
            sprite_continuous.append_sprite((row, col), random_angle)

    buf = BytesIO()
    base.save(buf, format='PNG')

    base.close()
    f_wangchang.close()

    if from_gif:
        return buf

    return await base64_to_message_segment(buf)
