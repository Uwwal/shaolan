import gc
from io import BytesIO

from PIL import Image

from plugins.bigwangchang.sprite_continuous import SpriteContinuous
from plugins.bigwangchang.wangchang import random_image
from plugins.wangchangarrive.arrive import wangchang_arrive, wangchang_arrive_mirror
from utils.image_utils import download_image, gif_to_png_list, base64_to_message_segment


async def random_wangchang_gif(image_url, p, img_type, args):
    image_content = await download_image(image_url)

    if image_content is None:
        return "看不见图, 你要不自己飞"

    with Image.open(image_content) as image:
        if image.format == 'GIF':
            png_list, duration_list = await gif_to_png_list(image)
        else:
            if img_type == '镜镜' or img_type == '像像':
                arrive = await wangchang_arrive_mirror(image, img_type == '像像')
            else:
                arrive = await wangchang_arrive(image, p, img_type)

            if arrive is None:
                return [await random_image(args, image_content, p)]
            else:
                return [arrive]

        gif_io = BytesIO()

        sprite_continuous = SpriteContinuous(image.size)

        images = []

        for png in png_list:
            img_bytes_io = await random_image(args, png, p, from_gif=True, sprite_continuous=sprite_continuous)

            with img_bytes_io:
                with Image.open(img_bytes_io) as img:
                    images.append(img.copy())

        del img_bytes_io

        # images = [Image.open(png) for png
        #           in png_list]

        images[0].save(
            gif_io,
            format='GIF',
            save_all=True,
            append_images=images[1:],
            duration=duration_list,
            loop=0,
            # optimize=True,
            # transparency=0,
            disposal=2,
        )

        for img in images:
            img.close()

        del images
        gc.collect()

        return await base64_to_message_segment(gif_io)
