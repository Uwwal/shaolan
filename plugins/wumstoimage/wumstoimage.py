import time
from io import BytesIO

from PIL import ImageDraw, Image, ImageFont

from config.constant import font_path, wum_page_capacity
from config.global_object import global_wum_dict
from utils.image_utils import change_non_transparent_alpha, base64_to_message_segment
from utils.wum_utils import get_rarity, get_rarity_name, get_rarity_color


async def wums_to_image(wums, page_id, head_label_text_1="", head_label_text_2="", is_blind_box=False):
    wum_list = [(wum_name, get_rarity(wum_name), v['num'], v['isProtected']) for wum_name, v in wums.items()]

    wum_sorted_list = sorted(wum_list, key=lambda x: x[1], reverse=True)

    wums_type_num = len(wum_sorted_list)

    if not is_blind_box:
        start_wum_index = (page_id - 1) * wum_page_capacity
        if start_wum_index > wums_type_num:
            page_id = 1
            start_wum_index = 0
        page_max = int(wums_type_num / wum_page_capacity) + (0 if wums_type_num % wum_page_capacity == 0 else 1)
        head_label_text_1 += f"        <第{page_id}页, 共{page_max}页>"

        end_wum_index = page_id * wum_page_capacity
        wum_sorted_list = wum_sorted_list[start_wum_index:end_wum_index]

        wums_type_num = len(wum_sorted_list)

    max_row_num = 10
    row_remainder = wums_type_num % max_row_num

    row = max_row_num if wums_type_num >= max_row_num else row_remainder
    col = int(wums_type_num / max_row_num) + (0 if row_remainder == 0 else 1)

    col_weight = 650
    row_height = 280

    start_y = 190
    start_x = 50

    # head label start
    image = Image.new("RGB", (start_x + col * col_weight + 50, start_y + row_height * row + 55), '#2c2b2b')
    if col == 0:
        image = Image.new("RGB", (1 * col_weight, start_y + row_height * row + 55), '#2c2b2b')

    draw = ImageDraw.Draw(image)

    draw.rectangle((start_x, start_y, start_x + col * col_weight, start_y + row_height * row), fill='#545353')

    head_label_font = ImageFont.truetype(font_path, 72)
    coins_font = ImageFont.truetype(font_path, 30)

    draw.text((50, 30), head_label_text_1, fill="white", font=head_label_font)
    draw.text((50, 125), head_label_text_2, fill="white", font=coins_font)

    row_font_50 = ImageFont.truetype(font_path, 50)
    row_font_35 = ImageFont.truetype(font_path, 35)

    # col start
    for i in range(col):
        # row start

        x_offset = start_x + i * col_weight

        for j in range(row):
            y_offset = start_y + row_height * j

            index = i * max_row_num + j

            if index == wums_type_num:
                break

            wum_name, rarity, num, is_protected = wum_sorted_list[index]
            wum = global_wum_dict[wum_name]

            wum_img = Image.open(wum.get_buf())

            resized_wum = wum_img.resize((250, 250))

            image.paste(resized_wum, (x_offset + 15, y_offset + 15), resized_wum)

            rotated_wum_img = resized_wum.rotate(30, expand=True)

            wum_alpha = await change_non_transparent_alpha(rotated_wum_img, 0.6)

            max_y = 342
            if j == row - 1:
                max_y = 260

            wum_alpha = wum_alpha.crop((0, 0, 265, max_y))

            image.paste(wum_alpha, (x_offset + 385, y_offset + 20), wum_alpha)

            draw.text((x_offset + 300, y_offset + 15), wum_name, fill="white", font=row_font_50)

            draw.text((x_offset + 300, y_offset + 85), "稀有度: " + get_rarity_name(rarity),
                      fill=get_rarity_color(rarity),
                      font=row_font_35)
            draw.text((x_offset + 300, y_offset + 125), "x" + str(num), fill="white", font=row_font_35)

            if is_protected:
                draw.text((x_offset + 300, y_offset + 165), "收藏中", fill="#eabf15", font=row_font_35)

            draw.rounded_rectangle(
                [(x_offset + 12, y_offset + 12), (x_offset + 268, y_offset + 268)], radius=15, outline='#2c2b2b',
                width=4
            )

            wum_img.close()

    buf = BytesIO()
    image.save(buf, format='PNG')

    return await base64_to_message_segment(buf)
