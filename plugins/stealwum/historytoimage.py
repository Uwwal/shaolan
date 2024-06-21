from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from config.constant import font_path
from config.global_object import global_wum_dict
from utils.image_utils import base64_to_message_segment


async def history_to_image(solve_res, name):
    col = len(solve_res)
    row = max(len(solve_res[0]), len(solve_res[1]))

    col_weight = 650
    row_height = 350

    main_hint_height = 50

    col_margin = 20
    row_margin = 20

    start_y = 150
    start_x = 50

    image = Image.new("RGB",
                      (
                          start_x + col * col_weight + 50 + col_margin * col * 2,
                          start_y + row_height * row + 55 + main_hint_height + 50 + row_margin * row * 2
                      ),
                      '#2c2b2b')

    draw = ImageDraw.Draw(image)

    draw.rectangle((start_x, start_y, start_x + col * col_weight + col_margin * col * 2,
                    start_y + row_height * row + main_hint_height + 50 + row_margin * row * 2), fill='#545353')

    head_label_font = ImageFont.truetype(font_path, 72)

    draw.text((50, 30), f"{name}的偷wum历史查询", fill="white", font=head_label_font)

    main_hint_font = ImageFont.truetype(font_path, 50)
    vs_font = ImageFont.truetype(font_path, 36)
    context_font = ImageFont.truetype(font_path, 30)
    coin_font = ImageFont.truetype(font_path, 50)

    success_color = "#05d8e9"
    fail_color = "#fb3737"

    side = 200

    # col start
    for i in range(col):
        # row start

        x_offset = start_x + i * col_weight + col_margin * i * 2 + col_margin

        if i > 0:
            draw.line((x_offset - col_margin, start_y, x_offset - col_margin,
                       start_y + row_height * row + row_margin * row * 2 + main_hint_height + 50), fill="#2c2b2b",
                      width=20)

        draw.text((x_offset + 20, start_y + 20), "行动历史" if i == 0 else "防御历史", fill="white",
                  font=main_hint_font)

        for j in range(len(solve_res[i])):
            y_offset = start_y + row_height * j + main_hint_height + 20 + row_margin * j * 2 + row_margin

            res_dict = solve_res[i][j]

            qq_name = res_dict.get('qq_name', "ERROR")
            other_name = res_dict.get('other_name', "ERROR")
            other_qq = res_dict.get('other_qq', "ERROR")
            is_success_hint = res_dict.get('is_success_hint', "ERROR")
            is_success_user = res_dict.get('is_success_user', "ERROR")
            trophy_hint = res_dict.get('trophy_hint', "ERROR")
            trophy = res_dict.get('trophy', "ERROR")
            strategy = res_dict.get('strategy', "ERROR")
            time_hint = res_dict.get('time_hint', "ERROR")
            time = res_dict.get('time', "ERROR")

            if len(other_name) > 7:
                other_name = other_name[:7]
                other_name += "..."

            draw.text((x_offset + 10, y_offset + 20), f"vs {other_name}({other_qq})",
                      fill="white", font=vs_font)

            draw.text((x_offset + col_weight - 120, y_offset + 20), is_success_hint,
                      fill=success_color if is_success_user else fail_color, font=vs_font)

            if isinstance(trophy, (int, float)):
                coin = str(trophy)

                coin_offset = 130
                coin_offset -= 5 * len(coin)

                draw.text((x_offset + 125, y_offset + 170), f"{trophy_hint} {coin} wum币", color='white',
                          font=coin_font)
            else:
                draw.text((x_offset + 10, y_offset + 60), trophy_hint, color='white', font=context_font)

                draw_wum_cur_time = 0
                len_wum_tuple = len(trophy)

                wum_image_margin = 10

                if len_wum_tuple == 0:
                    draw.text((x_offset + 170, y_offset + 170), "就当无事发生", color='white', font=coin_font)

                for wum_tuple in trophy:
                    wum_name, num = wum_tuple

                    wum = global_wum_dict[wum_name]

                    wum_img = Image.open(wum.get_buf())

                    resized_wum = wum_img.resize((side, side))

                    wum_img.close()

                    wum_image_draw_x = x_offset + (
                            col_weight - side * len_wum_tuple - wum_image_margin * (len_wum_tuple - 1)) // 2 + draw_wum_cur_time * (side + wum_image_margin)
                    wum_image_draw_y = y_offset + 100

                    image.paste(resized_wum, (wum_image_draw_x, wum_image_draw_y), resized_wum)

                    draw.text((wum_image_draw_x, wum_image_draw_y + side), wum_name, color='white',
                              font=context_font)

                    draw.text((wum_image_draw_x + side - 22, wum_image_draw_y + side), f"x{num}", color='white',
                              font=context_font)

                    draw_wum_cur_time += 1

            draw.text((x_offset + 20, y_offset + 140 + side), f"{time_hint} {time}", fill="white", font=context_font)
            draw.text((x_offset + col_weight - 120, y_offset + 140 + side), strategy, fill="white", font=context_font)

    buf = BytesIO()
    image.save(buf, format='PNG')

    return await base64_to_message_segment(buf)
