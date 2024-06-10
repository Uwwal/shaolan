from config.constant import iupar_channel_list
from config.global_object import message_counter
from utils.command_match import command_match, command_match_strict

import re

from utils.string_utls import get_group_id

command = '=iupar'

delete_command = '=delete'

command_add_channel = "添加群iupar"
command_remove_channel = '删除群iupar'

"""
iupar相关:
=iupar {text}: 在看着你哦在看着你哦在看着你哦
随机触发: 需联系superuser将群加入白名单
(*)=delete {text}: 忘记这个词
(*)[删除|添加]群iupar: 将群删除 or 加入白名单
"""


async def process_raw_message(msg):
    string = ""
    for i in msg:
        if i.type == 'text':
            if re.search(r'([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}', i.data['text']):
                continue
            string += i.data['text']

    message_counter.process_message(string)


async def iupar_message(msg, is_command=False):
    string = ""

    for i in msg:
        if i.type == 'text':
            text = i.data['text'].replace(" ", "")
            if text.startswith(command):
                string += text[len(command):].strip()
            else:
                string += text

    if string == "":
        return None

    return message_counter.iupar_message(string, is_command)


async def iupar_delete_word(msg):
    return message_counter.delete_word(msg[0].data['text'][len(delete_command):].strip())


async def iupar_match(msg):
    return await command_match(msg, command)


async def iupar_delete_match(msg):
    return await command_match(msg, delete_command)


async def iupar_add_channel_match(msg):
    return await command_match_strict(msg, command_add_channel)


async def iupar_remove_channel_match(msg):
    return await command_match_strict(msg, command_remove_channel)


async def add_channel_iupar(event):
    channel = get_group_id(event)

    if channel not in iupar_channel_list:
        iupar_channel_list.append(channel)
    return "Hello, Palestine"


async def remove_channel_iupar(event):
    channel = get_group_id(event)

    if channel in iupar_channel_list:
        iupar_channel_list.remove(channel)
    return "さようなら、パレスチナ"
