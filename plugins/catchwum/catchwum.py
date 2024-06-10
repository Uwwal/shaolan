import os

import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


from config.constant import font_path
from config.global_object import message_counter, global_wum_dict
from models.wum_pool import wum_pool, system_inventory
from utils.draw_utils import create_round_corner_mask
from utils.image_utils import download_image, change_non_transparent_alpha, base64_to_message_segment
from utils.wum_utils import get_rarity, get_rarity_color, get_rarity_name

background_dir = './data/catchwum/bg'

wum_target_size = (40, 40)

default_word = {'ns': ["大学", "山洞"],
                'nr': ["老者"],
                'n': ["作业", "魔法", "吉他", "水杯"],
                't': ["未来", "下午"],
                'a': ["尘封", "巨大", "普通", "热寂"],
                'vn': ["攻击", "发现", "解决", "点击"],
                'v': ["吃饭", "退勤"]}


async def catch_wum(qq_id, name):
    # start_time = time_.time()

    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    try_catch_res = wum_inventory.catch_wum(save=False)

    if try_catch_res[0]:
        new_wum = try_catch_res[1]
        wum_name = new_wum.name
        is_sleep = False
        new_num = try_catch_res[2]
        last_time = "ERROR"
        catch_cooling = "ERROR"
        r = random.randint(1, 60)
        if r == 1:
            system_inventory.catch_wum()
        await wum_inventory.add_last_steal_catchwum_count()
    else:
        is_sleep = True
        new_num = random.choice([1, 2, 3])
        wum_name = "wum"
        last_time = try_catch_res[2]
        catch_cooling = try_catch_res[1]

    wum_pool.release_inventory(qq_id)

    image_path = os.path.join(background_dir, f"{qq_id}.png")

    if os.path.exists(image_path):
        bg_image_path = image_path
    else:
        default_image = os.path.join(background_dir, "default.png")
        bg_image_path = default_image

    bg = Image.open(bg_image_path)
    bg_width, bg_height = bg.size

    for wum, v in wum_inventory.data["wums"].items():
        wum_img = Image.open(global_wum_dict[wum].buf)

        wum_img = wum_img.resize(wum_target_size)
        wum_width, wum_height = wum_img.size

        num = v["num"]
        for _ in range(num):
            x = random.randint(wum_width, bg_width - wum_width)
            y = random.randint(wum_height, bg_height - wum_height)

            bg.paste(wum_img, (x, y), wum_img)

    image = Image.new("RGB", (1000, 1540), '#2c2b2b')

    image.paste(bg, (50, 150), create_round_corner_mask(bg, 15))

    # head label start
    draw = ImageDraw.Draw(image)

    head_label_font = ImageFont.truetype(font_path, 72)

    draw.text((50, 30), name + " vs wum", fill="white", font=head_label_font)

    # caught wum image start
    caught_wum_bg = Image.new("RGB", (900, 350), '#545353')
    draw_caught_wum = ImageDraw.Draw(caught_wum_bg)

    caught_wum_font_40 = ImageFont.truetype(font_path, 40)
    draw_caught_wum.text((40, 15), "捕获wum", fill="#FDD2BF", font=caught_wum_font_40)

    caught_wum_font_30 = ImageFont.truetype(font_path, 30)

    if is_sleep:
        draw_caught_wum.text((300, 120), catch_cooling, fill="white", font=caught_wum_font_30)

        wum_img = Image.open(global_wum_dict["睡眠wum"].buf)

        wum_alpha = await change_non_transparent_alpha(wum_img, 0.6)

        resized_wum = wum_alpha.resize((250, 250))

        caught_wum_bg.paste(resized_wum, (630, 85), resized_wum)
    else:
        caught_wum_img = Image.open(new_wum.buf)

        resized_wum = caught_wum_img.resize((250, 250))

        caught_wum_bg.paste(resized_wum, (15, 85), resized_wum)

        draw_caught_wum.text((300, 85), wum_name, fill="white", font=caught_wum_font_40)

        rarity = get_rarity(wum_name)
        draw_caught_wum.text((500, 145), "稀有度: " + get_rarity_name(rarity), fill=get_rarity_color(rarity),
                             font=caught_wum_font_30)
        draw_caught_wum.text((300, 145), "x" + str(new_num), fill="white", font=caught_wum_font_30)
        draw_caught_wum.text((300, 190), f"抓到了{new_num}只", fill="white", font=caught_wum_font_30)

        rotated_wum_img = resized_wum.rotate(30, expand=True)

        wum_alpha = await change_non_transparent_alpha(rotated_wum_img, 0.6)

        caught_wum_bg.paste(wum_alpha, (630, 105), wum_alpha)

    draw_caught_wum.rounded_rectangle(
        [(12, 82), (268, 338)], radius=15, outline='#2c2b2b', width=4
    )

    image.paste(caught_wum_bg, (50, 735), create_round_corner_mask(caught_wum_bg, 15))

    # random event start
    event_bg = Image.new("RGB", (900, 370), '#545353')
    draw_event = ImageDraw.Draw(event_bg)

    draw_event.text((40, 15), "随机事件", fill="#FDD2BF", font=caught_wum_font_40)

    # 地名
    ns = get_random_word_list('ns', 2)
    # 人名
    nr = get_random_word_list('nr', 1)
    # 普通名词
    n = get_random_word_list('n', 4)
    # 形容词
    a = get_random_word_list('a', 4)
    # 时间
    t = get_random_word_list('t', 2)
    # 名动词
    vn = get_random_word_list('vn', 4)
    # 动词
    v = get_random_word_list('v', 2)

    message_counter.re_add_popped_word()

    time = t[0] + t[1]

    r = random.randint(0, 1)

    event_font_size = 28
    story_y = 100
    if r == 0:
        story = f"在一个{a[0]}的{time}，\n" \
                f"{name}在前往{ns[0]}的路上遇到了{new_num}只{wum_name}正在{vn[0]}{n[1]}。\n" \
                f"{name}被{wum_name}的{n[1]}{a[1]}地吸引，却意外{vn[1]}{a[2]}的{n[2]}。\n" \
                f"为了{vn[2]}{a[2]}的{n[2]}，{name}寻找到了一个{a[3]}{nr[0]}。\n" \
                f"{nr[0]}告诉{name}，关键在于用{n[3]}{v[0]}。\n"
        if is_sleep:
            story += f"可惜{wum_name}还需要{last_time}才能{v[1]},\n" \
                     f"{name}一个人回{ns[1]}了。"
        else:
            story += f"{name}成功{vn[2]}了{a[2]}的{n[2]}，和{new_num}只{wum_name}一起回{ns[1]}了。"
    elif r == 1:
        story_y = 75
        event_font_size = 26
        if len(name) > 8:
            event_font_size = 20
            story_y += 15
        elif len(name) > 6:
            event_font_size = 22
            story_y += 5
        elif len(name) > 4:
            event_font_size = 24

        story = f"一个{a[0]}的{time}，{a[3]}{nr[0]}给{name}打来电话，\n" \
                f"{name}豪爽的答应了：“我当然敢！”。\n" \
                f"周日下午在{ns[0]}举行，谁不来谁就是怂货。\n" \
                f"{name}原本以为{name}恐吓了{a[3]}{nr[0]}，" \
                f"{a[3]}{nr[0]}应该躲在{ns[1]}，不敢找{name}。\n" \
                f"可正当这时，{name}听见了{vn[0]}声，原来是{name}{n[0]}{vn[1]}了。\n" \
                f"一看，竟然是{wum_name}{vn[1]}的{n[0]}，他还真有{n[1]}。\n" \
                f"{wum_name}也要和{name}举行{vn[0]}大战，于是{name}按照约定，到达了{ns[0]}，\n"
        if is_sleep:
            story += f"{name}和{wum_name}势均力敌，平分秋色，比了{last_time}，也没分出胜负。"
        else:
            story += f"{name}{vn[2]}了{n[0]}，打的{wum_name}不敢还手，\n" \
                     f"对{wum_name}的打击比{vn[3]}{n[2]}还大。"

    event_wum_font_28 = ImageFont.truetype(font_path, event_font_size)

    draw_event.text((50, story_y), story, fill="white", font=event_wum_font_28)

    image.paste(event_bg, (50, 1115), create_round_corner_mask(event_bg, 15))

    buf = BytesIO()
    image.save(buf, format='PNG')

    # print("done", time_.time() - start_time)

    return await base64_to_message_segment(buf)


def get_random_word_list(p, num):
    return [
        word_tuple[1][0] if (word_tuple := message_counter.get_random_words(
            p)) is not None else default_word[p][i]
        for i in range(num)
    ]


async def change_wum_background_image(url, qq_id):
    image_data = await download_image(url)

    if image_data is None:
        return "此图暂时无能为力"

    image = Image.open(image_data)

    resized_image = image.resize((900, 550), Image.Resampling.LANCZOS)

    # if not resized_image.mode == 'RGB':
    #     resized_image = resized_image.convert('RGB')

    file_path = os.path.join(background_dir, f"{qq_id}.png")

    resized_image.save(file_path, "PNG")

    return "下次抓wum，要一起去这里哦"
