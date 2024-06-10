from plugins.checkstatus.checkstatus import check_group_status_process
from utils.command_match import command_match_strict
from utils.string_utls import get_group_id

"""
状态查询相关:
=群状态: wum神降临, iupar凝视
"""

command_check_group_status = "=群状态"


async def check_group_status_match(msg):
    return await command_match_strict(msg, command_check_group_status)


async def check_group_status_process_params(event):
    channel = get_group_id(event)

    return await check_group_status_process(channel)
