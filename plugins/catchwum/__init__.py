from plugins.catchwum.catchwum import change_wum_background_image
from plugins.catchwum.showwum import show_qq_id_wum, show_wum_collect_progress
from utils.command_match import command_match_strict, command_match
from utils.image_utils import find_quote_image
from utils.string_utls import get_message_sender, get_event_command_text, get_user_id

command = "抓wum"
command_change_bg = "来这抓wum"
command_show_wum = "wum库"
command_show_system_wum = "wum奖池"
command_show_wum_collect_progress = "wum进度"

"""
抓wum相关:
抓wum: 4小时抓一次
来这抓wum {img}: 更换bg
wum库 {page_index}?: 已有wum 40种wum占一页 从1开始
wum奖池 {page_index}?: 查看废品哥wum库
wum进度: wum收集进度
"""


async def catch_wum_match(msg):
    return await command_match_strict(msg, command)


async def change_wum_background_image_match(msg):
    return await command_match(msg, command_change_bg, support_quote=True)


async def show_wum_match(msg):
    return await command_match(msg, command_show_wum)


async def show_system_wum_match(msg):
    return await command_match(msg, command_show_system_wum)


async def show_wum_collect_progress_match(msg):
    return await command_match(msg, command_show_wum_collect_progress)


async def change_wum_background_image_process_params(msg, qq_id):
    if msg:
        if len(msg) > 1 and msg[1].type == 'image':
            return await change_wum_background_image(msg[1].data['url'], qq_id)
        else:
            image = await find_quote_image(msg)
            return await change_wum_background_image(image, qq_id)
    return "tune"


async def show_wum_process_param(event, is_system=False):
    if is_system:
        qq_id = "system"
        name = "废品哥"
        cur_command = command_show_system_wum
    else:
        qq_id = get_user_id(event)
        name = get_message_sender(event)
        cur_command = command_show_wum

    text = await get_event_command_text(event)

    args = text.strip()[len(cur_command):].strip()

    if len(args) == 0:
        return await show_qq_id_wum(qq_id, name)

    try:
        num = int(args)

        if num <= 0:
            return await show_qq_id_wum(qq_id, name)

        return await show_qq_id_wum(qq_id, name, num)
    except ValueError:
        return await show_qq_id_wum(qq_id, name)


async def show_wum_collect_progress_process_params(event):
    qq_id = get_user_id(event)
    name = get_message_sender(event)

    return await show_wum_collect_progress(qq_id, name)
