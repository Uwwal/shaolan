from models.wum_pool import wum_pool
from plugins.personalinfo.power_to_string import steal_power_to_string, defend_power_to_string
from utils.command_match import command_match
from utils.string_utls import get_message_sender, get_user_id

"""
个人简报相关:      
个人简报: 显示偷wum队伍情况, 其他待接
"""

command = "个人简报"


async def personal_info_command_match(msg):
    return await command_match(msg, command)


async def personal_info_process_params(event):
    qq_id = get_user_id(event)
    name = get_message_sender(event)

    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    steal_new_count = wum_inventory.data["steal_new_count"]

    await wum_inventory.clear_steal_new_count(save=False)

    wum_inventory.save()

    wum_pool.release_inventory(qq_id)

    steal_unit = wum_inventory.data["steal_unit"]

    defend_unit = wum_inventory.data["defend_unit"]

    steal_power = await wum_inventory.get_steal_power()
    defend_power = await wum_inventory.get_defend_power()

    return (f"{name}({qq_id})的个人简报:\n"
            f"行动队 : {steal_unit} {steal_power_to_string(steal_power)}\n"
            f"防卫队 : {defend_unit} {defend_power_to_string(defend_power)}\n"
            f"在这段时间被偷了 {steal_new_count} 次")
