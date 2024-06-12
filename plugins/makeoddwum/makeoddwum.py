import random

from config.constant import make_odd_tag_dict
from config.global_object import tag_yi_wum_dict
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

    tag_dict = {}

    for wum_name, num in wum_dict.items():
        wum_inventory.delete_wum(wum_name, num, save=False)

        tem_tag_list = make_odd_tag_dict[wum_name]

        for tag_tuple in tem_tag_list:
            tag, weight = tag_tuple

            if tag in tag_dict:
                tag_dict[tag] += weight * num
            else:
                tag_dict[tag] = weight * num

    cur_odd_point = wum_inventory.data['odd_point']

    wum_inventory.clear_odd_point(save=False)

    success_rate = cur_odd_point // 2

    tem_odd_dict = {}

    print(tag_dict)

    for tag, weight in tag_dict.items():
        if tag not in tag_yi_wum_dict:
            continue

        odd_wum_list = tag_yi_wum_dict[tag]

        for odd_wum_tuple in odd_wum_list:
            wum_name, scale = odd_wum_tuple

            if wum_name in tem_odd_dict:
                tem_odd_dict[wum_name] += scale * weight
            else:
                tem_odd_dict[wum_name] = scale * weight

    print(tem_odd_dict)

    odd_dict = {k: int(v) for k, v in tem_odd_dict.items() if int(v) != 0}

    print(odd_dict)

    if len(odd_dict) == 0:
        wum_inventory.save()

        wum_pool.release_inventory(qq_id)

        return f"{name}，你的测验成绩是0"

    odd_name_list = list(odd_dict.keys())
    odd_weight_list = list(odd_dict.values())

    odd_name = random.choices(odd_name_list, odd_weight_list, k=1)[0]

    odd_p = odd_dict[odd_name]

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
