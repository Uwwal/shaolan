from config.constant import max_wum_name_len
from config.global_object import global_wum_name_list
from models.wum_pool import wum_pool
from utils.command_match import command_match
from utils.string_utls import get_message_sender, get_event_command_text, get_user_id

command = "=添加wum"


async def lemmn_debug_add_wum_match(msg):
    return await command_match(msg, command)


async def debug_add_wum(event):
    text = await get_event_command_text(event)
    name = get_message_sender(event)
    qq_id = get_user_id(event)

    args_list = text.strip()[len(command):].strip().split()

    if len(args_list) == 0:
        return "再想想"

    wum_inventory = wum_pool.get_inventory(qq_id)

    success_name_list = []
    success_num_list = []

    if isinstance(wum_inventory, str):
        return wum_inventory

    for i in args_list:
        if len(i) > max_wum_name_len:
            return f"{i}是什么{name}你解释一下"
        try:
            num = int(i)

            if success_num_list and num > 0:
                success_num_list[-1] = num
        except ValueError:
            wum_name = i.replace(" ", "_")
            if wum_name in global_wum_name_list and wum_name not in success_name_list:
                success_name_list.append(wum_name)
                success_num_list.append(1)
            else:
                return f"{wum_name}是什么{name}你解释一下"

    assert len(success_num_list) == len(success_name_list)

    for i in range(len(success_num_list)):
        wum_inventory.add_wum(success_name_list[i], success_num_list[i], save=False)

    wum_inventory.save()

    wum_pool.release_inventory(qq_id)

    wum_dict = dict(zip(success_name_list, success_num_list))

    return f"{name}({qq_id}): {str(wum_dict)}"
