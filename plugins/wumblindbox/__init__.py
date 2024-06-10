from plugins.wumblindbox.wumblindbox import wum_blind_box
from utils.command_match import command_match_list
from utils.string_utls import get_message_sender, get_event_command_text, get_user_id

command_list = ["wum盲盒", "wum大盲盒"]

"""
wum盲盒相关:
wum盲盒: 花费5 wum币从废品哥wum库购买盲盒
wum大盲盒: 花费10 wum币, 低概率无中生典
"""


async def wum_blind_box_match(msg):
    return await command_match_list(msg, command_list)


async def wum_blind_box_process_params(event):
    name = get_message_sender(event)
    qq_id = get_user_id(event)
    text = await get_event_command_text(event)

    index = 0

    for command in command_list:
        if text.replace(" ", "").startswith(command):
            break
        index += 1

    return await wum_blind_box(qq_id, name, index)
