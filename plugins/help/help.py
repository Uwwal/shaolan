from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from config.constant import font_path
from config.global_object import docs_list
from utils.draw_utils import create_round_corner_mask
from utils.image_utils import base64_to_message_segment

docs_help_list_ = ['帮助相关:\n=help: 你已经抵达这里了\n[a|b]: a or b\n{}: param\n?: match 0 or 1 times\n(*): superuser指令\n'
                   '手机发图: 全屏输入->点击图片\n联系我们 群: 732908053']
docs_help_list_.extend(docs_list)


async def docs_help(head_label_text="", docs_help_list=""):
    if head_label_text == "":
        head_label_text = "使用帮助"
        docs_help_list = docs_help_list_

    row = len(docs_help_list)

    start_y = 150
    start_x = 50

    row_start_y = 15
    row_end_y = 15

    margin = 15

    row_head_font_size = 45
    row_text_font_size = 30

    image_height = start_y + 55 + row_start_y * row + row_head_font_size * row + 5 * row + row_end_y * row + margin * row

    n_num = row
    n_count_list = []
    for i in docs_help_list:
        n_count = i.count("\n") + 1
        n_num += n_count
        n_count_list.append(n_count)
        image_height += (row_text_font_size + 3) * n_count

    col_weight = 900

    # head label start
    image = Image.new("RGB", (start_x + col_weight + 50, image_height), '#2c2b2b')
    draw = ImageDraw.Draw(image)

    head_label_font = ImageFont.truetype(font_path, 72)

    draw.text((50, 30), head_label_text, fill="white", font=head_label_font)

    row_font_head = ImageFont.truetype(font_path, row_head_font_size)
    row_font_text = ImageFont.truetype(font_path, row_text_font_size)

    last_row_end_y = start_y
    # row start
    for i in range(row):
        origin_text = docs_help_list[i]

        n_count = n_count_list[i]

        row_height = row_start_y + row_head_font_size + 5 + (row_text_font_size + 3) * n_count + row_end_y
        row_bg = Image.new("RGB", (col_weight, row_height), '#545353')
        draw_row_bg = ImageDraw.Draw(row_bg)

        split_text = origin_text.split("\n")

        draw_row_bg.text((row_start_y, row_start_y), split_text[0], fill="white", font=row_font_head)

        y = row_start_y + row_head_font_size + 15

        for j in range(1, n_count):
            draw_row_bg.text((row_start_y * 2, y), split_text[j], fill="white", font=row_font_text)
            y += 5
            y += row_text_font_size

        row_bg_x = start_x
        last_row_end_y += margin

        image.paste(row_bg, (row_bg_x, last_row_end_y), create_round_corner_mask(row_bg, 15))

        last_row_end_y += row_height

    buf = BytesIO()
    image.save(buf, format='PNG')

    return await base64_to_message_segment(buf)
