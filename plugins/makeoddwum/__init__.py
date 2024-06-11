from config.constant import max_wum_name_len
from config.global_object import global_wum_name_list
from plugins.makeoddwum.makeoddwum import make_odd_wum
from utils.command_match import command_match
from utils.string_utls import get_user_id, get_message_sender, get_event_command_text

command = "异化wum"

"""
异化wum相关:      支持=help详细查询
异化wum {wum_name} {num}?:
    sum(num)==10
    wum和num交替填写, num为1时可省略
    使用_代替wum_name中的空格
"""

async def make_odd_wum_match(msg):
    return await command_match(msg, command)


async def make_odd_wum_process_params(event):
    qq_id = get_user_id(event)
    name = get_message_sender(event)
    text = await get_event_command_text(event)
    text = text.strip()

    success_name_list = []
    success_num_list = []

    args_list = text[len(command):].strip().split()

    if len(args_list) == 0:
        return "再想想"

    for i in args_list:
        if len(i) > max_wum_name_len:
            return f"{i}是什么{name}你解释一下"
        try:
            num = int(i)

            if success_num_list and num > 0:
                success_num_list[-1] = num
        except ValueError:
            wum_name = i.replace("_", " ")
            if wum_name in global_wum_name_list and wum_name not in success_name_list:
                success_name_list.append(wum_name)
                success_num_list.append(1)
            else:
                return f"{wum_name}是什么{name}你解释一下"

    assert len(success_num_list) == len(success_name_list)

    wum_num = sum(success_num_list)

    if wum_num != 10:
        return f"帮你想: 总数错误 {wum_num} / 10"

    wum_dict = dict(zip(success_name_list, success_num_list))

    return await make_odd_wum(qq_id, name, wum_dict)
