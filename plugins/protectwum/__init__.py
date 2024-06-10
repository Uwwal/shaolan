from plugins.protectwum.protectwum import protect_wum
from utils.command_match import command_match
from utils.string_utls import get_event_command_text, get_user_id

command = "收藏"
command_cancel = "取消收藏"

"""
收藏wum相关:
收藏 {wum_name}: wum不会被你回收了!
取消收藏 {wum_name}: 你行
"""


async def protect_wum_match(msg):
    return await command_match(msg, command)


async def protect_cancel_wum_match(msg):
    return await command_match(msg, command_cancel)


async def protect_wum_process_params(event):
    text = await get_event_command_text(event)
    qq_id = get_user_id(event)

    args = text.strip()[len(command):].strip()

    if len(args) == 0:
        return "再想想"

    return await protect_wum(qq_id, args, True)


async def protect_cancel_wum_process_params(event):
    text = await get_event_command_text(event)
    qq_id = get_user_id(event)

    args = text.strip()[len(command_cancel):].strip()

    if len(args) == 0:
        return "再想想"

    return await protect_wum(qq_id, args, False)
