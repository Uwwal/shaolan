from config.constant import wums_rarity_dict, wum_rarity_num, system_catch_wum_p, user_catch_wum_p


def get_rarity(name):
    return wums_rarity_dict[name]


def get_wum_rarity_weight(system=False):
    if system:
        return system_catch_wum_p
    else:
        return user_catch_wum_p


def get_rarity_name(rarity):
    if rarity == 1:
        return "普通"
    elif rarity == 2:
        return "轻冉"
    elif rarity == 3:
        return "色彩"
    elif rarity == 4:
        return "群"
    elif rarity == 5:
        return "异"
    elif rarity == 6:
        return "典"


def get_rarity_color(rarity):
    if rarity == 1:
        return "#fcf681"
    elif rarity == 2:
        return "#81fcc3"
    elif rarity == 3:
        return "#81e0fc"
    elif rarity == 4:
        return "#fc81c9"
    elif rarity == 5:
        return "#fba834"
    elif rarity == 6:
        return "#ff9696"

async def wum_dict_standard(wum_dict):
    for k, v in wum_dict.items():
        wum_dict[k] = {'num': v, 'isProtected': False}
    return wum_dict

rarity_name_list = [get_rarity_name(f) for f in range(1, wum_rarity_num + 1)]
