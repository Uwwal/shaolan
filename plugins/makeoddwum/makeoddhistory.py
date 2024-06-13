import time
from datetime import datetime
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from config.constant import font_path
from config.global_object import make_odd_history_collection, global_wum_dict
from utils.image_utils import base64_to_message_segment


async def insert_make_odd_history(res, wum_dict, channel_id, odd_point):
    record = {
        'time': time.time(),
        'result': res,
        'wum_dict': wum_dict,
        'channel': channel_id,
        'odd_point': odd_point
    }

    make_odd_history_collection.insert_one(record)


async def query_make_odd_history():
    return make_odd_history_collection.find().sort('time', -1).limit(10)


async def make_odd_history_to_image(channel_id, channel_name):
    cursor = await query_make_odd_history()
    record_list = list(cursor)
    len_record_list = len(record_list)

    col = 2
    row = len_record_list // col + len_record_list % col

    side = 100

    col_horizontal_padding = 20

    row_head_font_size = 40
    row_wum_font_size = 16
    row_time_font_size = 30

    result_font_size = 40

    wum_image_margin = 5

    col_weight = side * 6 + col_horizontal_padding + side + col_horizontal_padding + wum_image_margin * 4
    row_height = side * 2 + row_head_font_size + row_wum_font_size * 2 + row_time_font_size + wum_image_margin

    col_margin = 20
    row_margin = 20

    time_margin = 20
    result_image_left_margin = 20

    start_y = 150
    start_x = 50

    image = Image.new("RGB",
                      (
                          start_x + col * col_weight + 50 + col_margin * col * 2,
                          start_y + row_height * row + 50 + row_margin * row * 2
                      ),
                      '#2c2b2b')

    draw = ImageDraw.Draw(image)

    draw.rectangle((start_x, start_y, start_x + col * col_weight + col_margin * col * 2,
                    start_y + row_height * row + row_margin * row * 2), fill='#545353')

    head_label_font = ImageFont.truetype(font_path, 72)
    row_head_font = ImageFont.truetype(font_path, row_head_font_size)
    row_wum_font = ImageFont.truetype(font_path, row_wum_font_size)
    row_time_font = ImageFont.truetype(font_path, row_time_font_size)

    result_font = ImageFont.truetype(font_path, result_font_size)

    draw.text((50, 30), f"异化wum历史查询", fill="white", font=head_label_font)

    for i in range(col):
        x_offset = start_x + i * col_weight + col_margin * i * 2 + col_margin

        if i > 0:
            draw.line((x_offset - col_margin, start_y, x_offset - col_margin,
                       start_y + row_height * row + row_margin * row * 2 + 50), fill="#2c2b2b",
                      width=20)

        for j in range(row):
            index = j * col + i
            if index >= len_record_list:
                break

            y_offset = start_y + row_height * j + row_margin * j * 2 + row_margin
            record = record_list[index]
            record_time = record['time']
            result = record['result']
            wum_dict = record['wum_dict']
            record_channel = record['channel']
            odd_point = record.get('odd_point', '我不知道')

            if record_channel == channel_id:
                draw.text((x_offset + 20, y_offset), f"{channel_name}:", fill='white', font=row_head_font)
            else:
                draw.text((x_offset + 20, y_offset), f"不知名的远方:", fill='white', font=row_head_font)

            odd_point_len = len(str(odd_point))
            draw.text((x_offset + col_weight - 140 - odd_point_len * row_head_font_size // 2, y_offset),
                      f"异化点: {odd_point}", fill='white', font=row_head_font)

            y_offset += row_head_font_size + wum_image_margin

            len_wum_dict = len(wum_dict)

            tem_y_offset = y_offset

            is_len_above_five = False

            if len_wum_dict > 5:
                is_len_above_five = True

                len_wum_first_row = len_wum_dict // 2

                tem_wum_list = list(wum_dict.keys())

                loop_time = 0
                is_second_row = False

                for k in range(len_wum_dict):
                    wum_name = tem_wum_list[k]
                    num = wum_dict[wum_name]

                    if not is_second_row and k == len_wum_first_row:
                        tem_y_offset += side + row_wum_font_size
                        len_wum_first_row = len_wum_dict - len_wum_first_row
                        loop_time = 0
                        is_second_row = True

                    wum = global_wum_dict[wum_name]

                    wum_img = Image.open(wum.buf)

                    resized_wum = wum_img.resize((side, side))

                    wum_image_draw_x = (x_offset +
                                        (col_weight - side * 2 - side * len_wum_first_row -
                                         wum_image_margin * (len_wum_first_row - 1)) // 2
                                        + loop_time * (side + wum_image_margin))
                    wum_image_draw_y = tem_y_offset

                    image.paste(resized_wum, (wum_image_draw_x, wum_image_draw_y), resized_wum)

                    draw.text((wum_image_draw_x, wum_image_draw_y + side), wum_name, color='white',
                              font=row_wum_font)

                    draw.text((wum_image_draw_x + side - row_wum_font_size, wum_image_draw_y + side), f"x{num}",
                              color='white',
                              font=row_wum_font)

                    loop_time += 1

            else:
                tem_y_offset += side // 2
                loop_time = 0
                for wum_name, num in wum_dict.items():
                    wum = global_wum_dict[wum_name]

                    wum_img = Image.open(wum.buf)

                    resized_wum = wum_img.resize((side, side))

                    wum_image_draw_x = (
                            x_offset + (col_weight - side * 2 - side * len_wum_dict - wum_image_margin * (
                                len_wum_dict - 1)) // 2
                            + loop_time * (side + wum_image_margin))
                    wum_image_draw_y = tem_y_offset

                    image.paste(resized_wum, (wum_image_draw_x, wum_image_draw_y), resized_wum)

                    draw.text((wum_image_draw_x, wum_image_draw_y + side), wum_name, color='white',
                              font=row_wum_font)

                    draw.text((wum_image_draw_x + side - row_wum_font_size, wum_image_draw_y + side), f"x{num}",
                              color='white',
                              font=row_wum_font)

                    loop_time += 1

            tem_x_offset = x_offset + side * 5 + side // 2
            tem_y_offset = y_offset + side // 2

            draw.text((tem_x_offset + side // 3, tem_y_offset + side // 2 - result_font_size // 3), "->", fill='white',
                      font=result_font)

            tem_x_offset += side

            if isinstance(result, int):
                draw.text((tem_x_offset, tem_y_offset + 15), "一缕\n香烟", fill='white', font=result_font)
            elif len(result) == 0:
                wum = global_wum_dict["wum"]

                wum_img = Image.open(wum.buf)

                resized_wum = wum_img.resize((side, side))

                image.paste(resized_wum, (tem_x_offset, tem_y_offset), resized_wum)

                draw.text((tem_x_offset, tem_y_offset + side), "wum", color='white',
                          font=row_wum_font)

                draw.text((tem_x_offset + side - row_wum_font_size, tem_y_offset + side), "x0",
                          color='white',
                          font=row_wum_font)
            else:
                wum_name, num = result.popitem()

                wum = global_wum_dict[wum_name]

                wum_img = Image.open(wum.buf)

                resized_wum = wum_img.resize((side, side))

                image.paste(resized_wum, (tem_x_offset, tem_y_offset), resized_wum)

                draw.text((tem_x_offset, tem_y_offset + side), "wum", color='white',
                          font=row_wum_font)

                draw.text((tem_x_offset + side - row_wum_font_size, tem_y_offset + side), "x0",
                          color='white',
                          font=row_wum_font)

            y_offset += 2 * side + 2 * row_wum_font_size

            if is_len_above_five:
                y_offset += time_margin

            draw.text((x_offset, y_offset), f"仪式时间: {datetime.fromtimestamp(int(record_time))}", fill="white",
                      font=row_time_font)

    buf = BytesIO()
    image.save(buf, format='PNG')

    return await base64_to_message_segment(buf)
