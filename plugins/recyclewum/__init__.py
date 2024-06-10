from plugins.recyclewum.recyclewum import recycle_wum, recycle_wum_rarity, recycle_wum_num
from utils.command_match import command_match, command_match_list
from utils.string_utls import get_message_sender, get_event_command_text, get_user_id
from utils.wum_utils import rarity_name_list

command = "回收"
command_rarity_1 = "回收全部"
command_rarity_2 = "回收所有"
command_num_list = ["回收大于", "回收等于", "回收小于"]

command_suffix_list = ["全部", "所有", "大于", "等于", "小于"]

"""
回收wum相关:
回收 {wum_name} [{num}|all]: 回收指定数量wum
回收[全部|所有]{rarity}: 回收全部某稀有度wum
回收[大于|等于|小于]{num}:
    回收数量[大于|等于|小于]{num}的wum, 大于会保留至{num}个
"""


async def recycle_wum_match(msg):
    return await command_match(msg, command)


async def recycle_wum_rarity_match(msg):
    return (await command_match(msg, command_rarity_1)) or (await command_match(msg, command_rarity_2))


async def recycle_wum_num_match(msg):
    return await command_match_list(msg, command_num_list)


async def recycle_wum_rarity_process_params(event):
    text = await get_event_command_text(event)
    name = get_message_sender(event)
    qq_id = get_user_id(event)

    args = text.strip()[len(command_rarity_1):].strip()

    if len(args) == 0:
        return "再想想"

    if args in rarity_name_list:
        return await recycle_wum_rarity(qq_id, name, rarity_name_list.index(args) + 1)
    else:
        return "再想想"


async def recycle_wum_num_process_params(event):
    text = await get_event_command_text(event)
    name = get_message_sender(event)
    qq_id = get_user_id(event)

    command_type = text.strip()[len(command):len(command_num_list[0])].strip()
    args = text.strip()[len(command_num_list[0]):].strip()

    if len(args) == 0:
        return "再想想"

    try:
        num = int(args)

        if num < 0:
            return "再想想"
    except ValueError:
        return "再想想"

    return await recycle_wum_num(qq_id, name, command_type, num)


async def recycle_wum_process_params(event):
    text = await get_event_command_text(event)
    name = get_message_sender(event)
    qq_id = get_user_id(event)

    args_list = text.strip()[2:].strip().split()

    if len(args_list) == 0:
        return "再想想"
    if len(args_list[0]) >= 2:
        if args_list[0][:2] in command_suffix_list:
            return None

    wum_name = " ".join(args_list[:-1])
    wum_name.replace("_", " ")

    if args_list[-1] == "all":
        num = "all"
    else:
        try:
            num = int(args_list[-1])

            if num <= 0:
                return "再想想"
        except ValueError:
            return "再想想"

    return await recycle_wum(qq_id, name, wum_name, num)
