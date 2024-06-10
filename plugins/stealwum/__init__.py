from config.constant import max_wum_name_len, steal_strategy_string_list
from config.global_object import global_wum_name_list
from plugins.stealwum.stealwum import steal_wum, set_steal_unit, set_defend_unit, set_steal_strategy, steal_wum_history
from utils.command_match import command_match
from utils.string_utls import get_message_sender, get_event_command_text, get_user_id, get_group_id

command = "偷wum"
command_strategy = "设置策略"
command_set_unit_list = ["设置行动队", "设置防卫队"]

"""
偷wum相关:      支持=help详细查询
偷wum {At}: 根据行动策略对指定人进行行动
设置策略 [注重稀有|防卫破坏|拿钱就跑]: 默认注重稀有
偷wum 历史查询: 看最近5次行动与5次防卫记录
设置 [行动队|防卫队] {wum_name} {num}?:
    可以让最多五种wum加入到队伍,
    wum和num交替填写, num为1时可省略
    使用_代替wum_name中的空格
"""


async def steal_wum_match(msg):
    if msg:
        tag = msg[0].type

        if tag == 'text' and msg[0].data['text'].replace(" ", "").startswith(command):
            text = msg[0].data['text']
            if len(msg) == 1:
                args = text.strip()[len(command):].strip()

                if args == "历史查询":
                    return True, -1  # -1 == 历史查询
            elif msg[1].type == 'at':
                # [Text(text='喂？'), At(id='3408183732', name='lemmn'), Text(text=' ')]
                return True, str(msg[1].data['qq'])

    return False


async def set_steal_strategy_match(msg):
    return await command_match(msg, command_strategy)


async def steal_wum_set_unit_match(msg):
    if msg:
        tag = msg[0].type

        if tag == 'text':
            text = msg[0].data['text']

            if text.replace(" ", "").startswith(command_strategy):
                return False

            for i in range(len(command_set_unit_list)):

                if text.replace(" ", "").startswith(command_set_unit_list[i]):
                    return i
    return False


async def steal_wum_history_process_params(event):
    qq_id = get_user_id(event)
    name = get_message_sender(event)

    return await steal_wum_history(qq_id, name)


async def steal_wum_set_steal_strategy_process_params(event):
    qq_id = get_user_id(event)

    text = await get_event_command_text(event)

    args = text.strip()[len(command_strategy):].strip()

    if args in steal_strategy_string_list:
        i = steal_strategy_string_list.index(args)
    else:
        return "再想想"

    return await set_steal_strategy(qq_id, i)


async def steal_wum_process_params(event, at_id, at_name):
    qq_id = get_user_id(event)
    name = get_message_sender(event)
    return await steal_wum(qq_id, at_id, name, at_name)


async def steal_wum_set_unit_process_params(event, index):
    qq_id = get_user_id(event)
    name = get_message_sender(event)
    text = await get_event_command_text(event)
    text = text.strip()

    success_name_list = []
    success_num_list = []

    if index == 0:
        if text.startswith(command_set_unit_list[0]):
            args_list = text[len(command_set_unit_list[0]):].strip().split()
        else:
            args_list = text[len(command_set_unit_list[0]) + 1:].strip().split()
    else:
        if text.startswith(command_set_unit_list[1]):
            args_list = text[len(command_set_unit_list[1]):].strip().split()
        else:
            args_list = text[len(command_set_unit_list[1]) + 1:].strip().split()

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

    wum_dict = dict(zip(success_name_list, success_num_list))

    if len(wum_dict) > 5:
        return f"我不是极简主义 {len(wum_dict)} / 5"

    if index == 0:
        return await set_steal_unit(qq_id, wum_dict)
    else:
        return await set_defend_unit(qq_id, wum_dict)
