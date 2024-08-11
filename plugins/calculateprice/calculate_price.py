from config.constant import dian_wum_recycle_price, dian_rarity, yi_wum_recycle_price, yi_rarity, keep_wum_rarity_num
from models.wum_pool import system_inventory


def calculate_price(rarity, rarity_weight_, base_sum_coin, wum_name):
    # wums_rarity_count = system_inventory.data["wums_rarity_count"]
    if rarity == yi_rarity:
        return yi_wum_recycle_price
    elif rarity == dian_rarity:
        return dian_wum_recycle_price

    rarity_weight = rarity_weight_.copy()[:4]

    rarity_weight = rarity_weight[::-1]

    sum_rarity_weight = 0
    for i in rarity_weight:
        sum_rarity_weight += i

    base_coin_list = [f / sum_rarity_weight * base_sum_coin for f in rarity_weight]

    base_coin = base_coin_list[rarity - 1]

    wums = system_inventory.data["wums"]

    if wum_name in wums.keys():
        num = wums[wum_name]['num']
    else:
        num = 0

    delta_coin = (((keep_wum_rarity_num[rarity - 1] / 2) - num) / keep_wum_rarity_num[rarity - 1]) * base_coin

    base_coin += delta_coin

    # min_rarity_num = wums_rarity_count[0]
    # for i in wums_rarity_count[:4]:
    #     min_rarity_num = min(min_rarity_num, i)
    #
    # coin_list_len = len(base_coin_list)
    #
    # delta_price_list = [0] * coin_list_len
    # final_price_list = base_coin_list.copy()
    # for i in range(coin_list_len):
    #     num = wums_rarity_count[i] - min_rarity_num
    #
    #     if num > 460:
    #         final_price_list[i] *= 0.2
    #     else:
    #         ratio = pow(0.9965, num)
    #
    #         final_price_list[i] = max(final_price_list[i] * ratio, base_coin_list[i] * 0.2)
    #
    #     delta_price_list[i] += final_price_list[i] - base_coin_list[i]
    #
    # for i in range(coin_list_len):
    #     tem_sum_rarity = sum_rarity_weight - rarity_weight[i]
    #
    #     for j in range(coin_list_len):
    #         if i == j:
    #             continue
    #         scale = rarity_weight[j] / tem_sum_rarity
    #
    #         final_price_list[j] -= delta_price_list[i] * scale

    return base_coin