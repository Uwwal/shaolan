from config.constant import wum_rarity_num, wum_collect_score_list
from config.global_object import wum_rarity_dict_list
from models.wum_pool import wum_pool
from plugins.wumstoimage.wumstoimage import wums_to_image
from utils.wum_utils import get_rarity, get_rarity_name

wum_rarity_count_list = [0] * wum_rarity_num
max_collect_score = 0
for rarity_, l in wum_rarity_dict_list.items():
    len_l = len(l)
    wum_rarity_count_list[rarity_-1] = len_l
    max_collect_score += len_l * wum_collect_score_list[rarity_-1]


async def show_qq_id_wum(qq_id, name, page_id=1):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    wum_pool.release_inventory(qq_id)

    wums = wum_inventory.data["wums"]

    head_label_text_1 = name + "的wum统计"
    head_label_text_2 = f"wum币余额: {wum_inventory.data['coins']}"

    return await wums_to_image(wums, page_id, head_label_text_1, head_label_text_2)


async def show_wum_collect_progress(qq_id, name):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    wum_pool.release_inventory(qq_id)

    wums = wum_inventory.data["wums"]

    rarity_list = [0] * wum_rarity_num

    for wum_name in wums.keys():
        rarity = get_rarity(wum_name)

        rarity_list[rarity - 1] += 1

    score = 0

    r = f"{name}的wum收集进度:\n"

    for i in range(wum_rarity_num):
        score += rarity_list[i] * wum_collect_score_list[i]
        r += f"{get_rarity_name(i+1)}: {rarity_list[i]} / {wum_rarity_count_list[i]} \n"

    r += "\n"

    rate = score / max_collect_score * 100

    r += f"评分: {rate:.2f}\n"

    if rate < 20:
        summary = "虽然你的进度很低, 但也不要给废品哥好脸"
    elif rate < 40:
        summary = "卡在这了吗, 要不抽个大盲盒"
    elif rate < 60:
        summary = "距离老登还差回收大于1"
    elif rate < 80:
        summary = "导致wum伤心的五个行为, 建议收藏"
    elif rate < 100:
        summary = "渴望赞赏吗？"
    elif rate == 100:
        summary = "少抓wum多鹿馆"
    else:
        summary = f"{rate}, 你开挂了? 反馈bug喜提封号大奖"

    # print(rarity_list)
    # print(rate)
    # print(score)
    # print(max_collect_score)
    # print(wum_rarity_count_list)

    r += summary
    return r
