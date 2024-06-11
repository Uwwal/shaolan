import random

from config.constant import recycle_sum_coin, dian_rarity
from config.global_object import wum_rarity_dict_list
from models.wum_pool import wum_pool, system_inventory
from plugins.calculateprice.calculate_price import calculate_price
from plugins.wumstoimage.wumstoimage import wums_to_image
from utils.wum_utils import get_rarity, get_wum_rarity_weight, wum_dict_standard

price_list = [5, 10]
delta_value_list = [lambda: random.uniform(-2.2, 0.1), lambda: random.uniform(-10, 7)]


async def wum_blind_box(qq_id, name, type_index):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    coins = wum_inventory.data['coins']

    price = price_list[type_index]
    max_value = price + delta_value_list[type_index]()

    if coins < price:
        wum_pool.release_inventory(qq_id)
        return "给我好好带钱过来啊, 你这混蛋"

    wums = system_inventory.data['wums']

    wums_num = sum(system_inventory.data["wums_rarity_count"])

    if wums_num < 4:
        wum_pool.release_inventory(qq_id)
        return "废品哥货源不足"

    wum_inventory.payout(price, save=False)
    system_inventory.top_up(price, save=False)

    blind_box_value = 0

    wum_dict = {}

    rarity_weight = get_wum_rarity_weight()

    skip_normal_blind_box = False

    if type_index == 1:
        r = random.randint(0, 100)
        if r > 97:
            skip_normal_blind_box = True
            wum = random.choice(wum_rarity_dict_list[dian_rarity])
            wum_dict.update({wum.name: 1})

    if not skip_normal_blind_box:
        for i in range(wums_num):
            wum_name = random.choice(list(wums.keys()))

            rarity = get_rarity(wum_name)

            if blind_box_value > max_value:
                break

            if rarity == dian_rarity:
                for tem_wum_name, num in wum_dict.items():
                    system_inventory.add_wum(tem_wum_name, num, save=False)

                wum_dict.clear()
                wum_dict.update({wum_name: 1})

                system_inventory.delete_wum(wum_name, 1, save=False)

                break
            else:
                t_price = calculate_price(rarity, rarity_weight, recycle_sum_coin)

            blind_box_value += t_price

            if wum_name in wum_dict.keys():
                wum_dict[wum_name] += 1
            else:
                wum_dict.update({wum_name: 1})

            system_inventory.delete_wum(wum_name, 1, save=False)

            # print(
            #     f"name: {wum_name}, rarity: {rarity}, price: {t_price}, value: {blind_box_value}, max_value: {max_value}")

    for wum_name, num in wum_dict.items():
        wum_inventory.add_wum(wum_name, num, save=False)

    wum_inventory.save()
    system_inventory.save()

    wum_pool.release_inventory(qq_id)

    blind_box_name_prefix = ""
    if type_index == 1:
        blind_box_name_prefix = "大"

    head_label_text_1 = name + "的" + blind_box_name_prefix + "盲盒"
    head_label_text_2 = f"wum币余额: {wum_inventory.data['coins']}      异化点: {wum_inventory.data['odd_point']}"

    return await wums_to_image(await wum_dict_standard(wum_dict), 0, head_label_text_1, head_label_text_2, True)

