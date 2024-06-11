import random

from config.constant import make_odd_dict, yi_rarity
from config.global_object import wum_rarity_dict_list
from models.wum_pool import wum_pool
from plugins.wumstoimage.wumstoimage import wums_to_image
from utils.wum_utils import wum_dict_standard


async def make_odd_wum(qq_id, name, wum_dict):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    for wum_name, num in wum_dict.items():
        if wum_name not in wum_inventory.data["wums"] or wum_inventory.data["wums"][wum_name]["num"] < num:
            wum_pool.release_inventory(qq_id)
            return f"帮你想: 你有{num}只{wum_name}吗？"

    tem_odd_dict = {}

    for wum_name, num in wum_dict.items():
        wum_inventory.delete_wum(wum_name, num, save=False)

        if wum_name == "wum":
            all_odd_wum = [wum_.name for wum_ in wum_rarity_dict_list[yi_rarity]]
            for odd_name in all_odd_wum:
                if odd_name in tem_odd_dict:
                    tem_odd_dict[odd_name] += num
                else:
                    tem_odd_dict[odd_name] = num
        elif wum_name in make_odd_dict:
            odd_list = make_odd_dict[wum_name]

            for odd_name, weight in odd_list:
                if odd_name in tem_odd_dict:
                    tem_odd_dict[odd_name] += weight * num
                else:
                    tem_odd_dict[odd_name] = weight * num

    cur_odd_point = wum_inventory.data['odd_point']

    wum_inventory.clear_odd_point(save=False)

    success_rate = cur_odd_point // 2

    print(len(tem_odd_dict))
    print(tem_odd_dict)

    if len(tem_odd_dict) == 0:
        wum_inventory.save()

        wum_pool.release_inventory(qq_id)

        return f"{name}，你的测验成绩是0"

    odd_name_list = list(tem_odd_dict.keys())
    odd_weight_list = list(tem_odd_dict.values())

    odd_name = random.choices(odd_name_list, odd_weight_list, k=1)[0]

    odd_p = tem_odd_dict[odd_name]

    success_rate += odd_p

    r = random.randint(1, 100)

    print(r, success_rate)

    gain_wum_dict = {}

    if r <= success_rate:
        wum_inventory.add_wum(odd_name, 1, save=False)
        gain_wum_dict.update({odd_name: 1})
    else:
        gain_wum_num = success_rate // 10
        if gain_wum_num > 1:
            wum_inventory.add_wum("wum", gain_wum_num, save=False)
            gain_wum_dict.update({"wum": gain_wum_num})

    wum_inventory.save()

    wum_pool.release_inventory(qq_id)

    head_label_text_1 = name + "的异化结果"
    head_label_text_2 = f"wum币余额: {wum_inventory.data['coins']}      异化点: {wum_inventory.data['odd_point']}"

    return await wums_to_image(await wum_dict_standard(gain_wum_dict), 0, head_label_text_1, head_label_text_2, True)
