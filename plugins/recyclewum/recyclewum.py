import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from config.constant import recycle_sum_coin, matong_gif_path, font_path, keep_wum_rarity_num, yi_rarity
from config.global_object import global_wum_dict
from models.wum_pool import wum_pool, system_inventory
from plugins.calculateprice.calculate_price import calculate_price
from plugins.recyclewum.wum_continuous import WumContinuous
from utils.image_utils import sync_gif_to_png_list, base64_to_message_segment
from utils.wum_utils import get_rarity, get_wum_rarity_weight

matong_gif = Image.open(matong_gif_path)
matong_png_list, duration_list = sync_gif_to_png_list(matong_gif)

min_side = min(matong_gif.size)
new_wum_size = (int(min_side / 15), int(367 * min_side / 15 / 401))

name_pos_list = [(125, 20), (124, 15), (125, 17), (120, 17), (118, 14)]
coin_pos_list = [(0, 30), (0, 28), (0, 24), (0, 16), (0, 0)]
coin_alpha_list = [255, 204, 153, 102, 51]


async def recycle_wum(qq_id, name, wum_name, num):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    wums = wum_inventory.data["wums"]

    if isinstance(num, str) and num == 'all':
        if wum_name not in wums.keys():
            wum_pool.release_inventory(qq_id)
            return "你根本没带够诚意吧"
        num = wums[wum_name]['num']

    if wum_name not in wums.keys() or wums[wum_name]['num'] < num:
        wum_pool.release_inventory(qq_id)
        return "你根本没带够诚意吧"

    if wums[wum_name]['isProtected']:
        wum_pool.release_inventory(qq_id)
        return "你个福瑞不如的东西"

    rarity = get_rarity(wum_name)

    gain_coins = 0
    system_gain_coins = 0

    rarity_weight = get_wum_rarity_weight()

    recycle_dict = {}

    for i in range(num):
        coin = calculate_price(rarity, rarity_weight, recycle_sum_coin)
        gain_coins += coin

        if rarity == yi_rarity:
            system_gain_coins += coin
        elif wum_name in system_inventory.data["wums"] and system_inventory.data["wums"][wum_name]["num"] >= \
                keep_wum_rarity_num[rarity - 1]:
            system_gain_coins += coin
        else:
            system_inventory.add_wum(wum_name, 1, save=False)

    recycle_dict.update({wum_name: num})

    wum_inventory.delete_wum(wum_name, num, save=False)

    gain_coins = round(gain_coins, 4)
    system_gain_coins = round(system_gain_coins, 4)

    wum_inventory.top_up(gain_coins, save=False)
    system_inventory.payout(gain_coins - system_gain_coins, save=False)

    wum_inventory.save()
    system_inventory.save()

    wum_pool.release_inventory(qq_id)

    return await recycle_wum_gif(name, recycle_dict, gain_coins, num)
    # return f"{num}只{wum_name}在{name}的指示下化为了一些wum币, 有{gain_coins}这么多\n不过wum们还会回来, 不是吗"


async def recycle_wum_rarity(qq_id, name, rarity):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    wums = wum_inventory.data["wums"]

    wum_num = 0

    sum_coin = 0

    rarity_weight = get_wum_rarity_weight()

    wums_items_copy = wums.copy()

    recycle_dict = {}

    for wum_name, v in wums_items_copy.items():
        wum_rarity = get_rarity(wum_name)

        if wum_rarity != rarity:
            continue

        num = v["num"]
        is_protect = v["isProtected"]
        if is_protect:
            continue

        gain_coins = 0
        system_gain_coins = 0

        for i in range(num):
            coin = calculate_price(rarity, rarity_weight, recycle_sum_coin)
            gain_coins += coin

            if rarity == yi_rarity:
                system_gain_coins += coin
            elif wum_name in system_inventory.data["wums"] and system_inventory.data["wums"][wum_name]["num"] >= \
                    keep_wum_rarity_num[wum_rarity - 1]:
                system_gain_coins += coin
            else:
                system_inventory.add_wum(wum_name, 1, save=False)

        wum_num += num

        recycle_dict.update({wum_name: num})

        wum_inventory.delete_wum(wum_name, num, save=False)

        sum_coin += gain_coins

        sum_coin = round(sum_coin, 4)
        system_gain_coins = round(system_gain_coins, 4)

        wum_inventory.top_up(gain_coins, save=False)
        system_inventory.payout(gain_coins - system_gain_coins, save=False)

    wum_inventory.save()
    system_inventory.save()

    wum_pool.release_inventory(qq_id)

    return await recycle_wum_gif(name, recycle_dict, sum_coin, wum_num)
    # return f"{wum_num}只wum在{name}的指示下化为了一些wum币, 有{sum_coin}这么多\n不过wum们还会回来, 不是吗"


async def recycle_wum_num(qq_id, name, command_type, command_num):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    wums = wum_inventory.data["wums"]

    wum_num = 0

    sum_coin = 0

    rarity_weight = get_wum_rarity_weight()

    wums_items_copy = wums.copy()

    recycle_dict = {}

    for wum_name, v in wums_items_copy.items():
        num = v["num"]
        is_protect = v["isProtected"]
        if is_protect:
            continue

        if command_type == "大于":
            if not num > command_num:
                continue
            num -= command_num
        elif command_type == "等于":
            if not num == command_num:
                continue
        elif command_type == "小于":
            if not num < command_num:
                continue

        wum_rarity = get_rarity(wum_name)

        gain_coins = 0
        system_gain_coins = 0

        for i in range(num):
            coin = calculate_price(wum_rarity, rarity_weight, recycle_sum_coin)
            gain_coins += coin

            if wum_rarity == yi_rarity:
                system_gain_coins += coin
            elif wum_name in system_inventory.data["wums"] and system_inventory.data["wums"][wum_name]["num"] >= \
                    keep_wum_rarity_num[wum_rarity - 1]:
                system_gain_coins += coin
            else:
                system_inventory.add_wum(wum_name, 1, save=False)

        wum_num += num

        recycle_dict.update({wum_name: num})

        wum_inventory.delete_wum(wum_name, num, save=False)

        sum_coin += gain_coins

        sum_coin = round(sum_coin, 4)
        system_gain_coins = round(system_gain_coins, 4)

        wum_inventory.top_up(gain_coins, save=False)
        system_inventory.payout(gain_coins - system_gain_coins, save=False)

    wum_inventory.save()
    system_inventory.save()

    wum_pool.release_inventory(qq_id)

    return await recycle_wum_gif(name, recycle_dict, sum_coin, wum_num)


async def recycle_wum_gif(name, wum_dict, coins, sum_num):
    wum_continuous = WumContinuous(sum_num, len(matong_png_list))

    name_font = ImageFont.truetype(font_path, 30)
    coin_font = ImageFont.truetype(font_path, 30)

    gif_index = 0

    png_list = [Image.open(f) for f in matong_png_list]

    res_list = []

    for png in png_list:
        if png.mode != 'RGBA':
            png = png.convert('RGBA')

        draw = ImageDraw.Draw(png)

        # draw wum
        wum_index = 0

        for wum_name, num in wum_dict.items():
            wum_image = Image.open(global_wum_dict[wum_name].buf)

            wum_image_resize = wum_image.resize(new_wum_size)

            for _ in range(num):
                pos, angle = wum_continuous.get(wum_index, gif_index)

                wum_index += 1

                wum_image_rotate = wum_image_resize.rotate(angle, expand=True)

                png.paste(wum_image_rotate, pos, wum_image_rotate)

        # draw name
        draw.text(name_pos_list[gif_index], name, fill="white", font=name_font)

        # draw coin
        draw.text((365 + coin_pos_list[gif_index][0], 10 + coin_pos_list[gif_index][1]), f"+{coins}",
                  fill=(255, 255, 255, coin_alpha_list[gif_index]), font=coin_font)

        gif_index += 1

        res_list.append(png)

    gif_io = BytesIO()

    r = random.randint(1, 5)

    if r == 1:
        res_list = res_list[::-1]

    res_list[0].save(
        gif_io,
        format='GIF',
        save_all=True,
        append_images=res_list[1:],
        # duration=duration_list,
        duration=150,
        loop=0,
        # optimize=True,
        # transparency=0,
        disposal=2,
    )

    return await base64_to_message_segment(gif_io)
