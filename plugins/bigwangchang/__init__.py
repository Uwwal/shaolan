import random

from config.constant import wangchang_img_arg_name_list, wangchang_img_path_list, wangchang_img_num, \
    default_nielian_num, default_wangchang_num
from plugins.bigwangchang.wangchang_gif import random_wangchang_gif
from utils.command_match import command_match

from config.global_object import ftwc_config
from utils.image_utils import find_quote_image
from utils.string_utls import find_first_text_in_quote, get_message_sender, get_group_id, get_user_id

command = '飞天大'
command_remove_id = "叛教" + command + "wum"
command_add_id = '皈依' + command + "wum"
command_remove_channel = '删除群' + command + 'wum'
command_add_channel = '添加群' + command + 'wum'

"""
飞天大wum相关:
飞天大{param} {num}? {img}: 换脸 or 随机
param: [王畅|卤蛋|wum|羽蛇|捏脸|镜镜|像像]
[叛教|皈依]飞天大wum: 
    神的随机降临, 需联系superuser将群加入白名单
(*)[删除|添加]群飞天大wum: 将群删除 or 加入白名单
"""


async def wangchang_match(msg):
    return await command_match(msg, command, support_quote=True)


async def wangchang_config_add_channel_match(msg):
    return await command_match(msg, command_add_channel)


async def wangchang_config_remove_channel_match(msg):
    return await command_match(msg, command_remove_channel)


async def wangchang_config_add_id_match(msg):
    return await command_match(msg, command_add_id)


async def wangchang_config_remove_id_match(msg):
    return await command_match(msg, command_remove_id)


async def random_wangchang(msg, channel):
    index = 0
    for i in msg[1:]:
        if i.type == 'image':
            image = i.data['url']
            break
    else:
        image = await find_quote_image(msg)
        if image is None:
            return "tune"
        index = find_first_text_in_quote(msg)

    image_type_and_args = msg[index].data['text'].strip()[len(command):].strip()

    i = 0
    for try_arg_name in wangchang_img_arg_name_list:
        name_len = len(try_arg_name)

        if image_type_and_args[:name_len] == try_arg_name:
            if try_arg_name == '王畅' and channel not in ftwc_config.channel_list:
                return "本群畅度不足, 无法进行上位召唤"
            img_type = try_arg_name
            args = image_type_and_args[name_len:]
            p = wangchang_img_path_list[i]
            break

        i += 1
    else:
        try_arg_name = '镜像'
        name_len = len(try_arg_name)
        if image_type_and_args[:name_len] == try_arg_name:
            img_type = '镜镜'
            args = image_type_and_args[name_len:]
            p = wangchang_img_path_list[wangchang_img_arg_name_list.index(img_type)]
        else:
            return "并不认识这个伪物"

    args = args.strip()

    if not args.isdigit():
        random_num = default_wangchang_num
        if img_type == '捏脸':
            random_num = default_nielian_num

        arrive = await random_wangchang_gif(image, p, img_type, random.randint(1, random_num))
        return arrive
    else:
        args = int(args)
        if args <= 0:
            args = abs(args)

    return await random_wangchang_gif(image, p, img_type, args=args)


async def on_image_receive_wangchang(img):
    t = random.randint(0, wangchang_img_num - 1)

    img_type = wangchang_img_arg_name_list[t]

    random_num = default_wangchang_num
    if img_type == '捏脸':
        random_num = default_nielian_num

    r_image = await random_wangchang_gif(img.data['url'], wangchang_img_path_list[t], img_type, random.randint(1, random_num))
    return r_image


async def add_channel_wangchang(event):
    channel = get_group_id(event)

    ftwc_config.add_channel(channel)
    return "好了, 王畅将会在未来降临本群"


async def remove_channel_wangchang(event):
    channel = get_group_id(event)

    ftwc_config.remove_channel(channel)
    return "王畅不会再主动巡游此地"


async def add_id_wangchang(event):
    qq_id = get_user_id(event)

    ftwc_config.add_id(qq_id)

    name = get_message_sender(event)

    return name + "，你将成为王畅的信徒，之一"


async def remove_id_wangchang(event):
    qq_id = get_user_id(event)

    ftwc_config.remove_id(qq_id)
    return "滚，你这个不守畅道的东西"


async def check_channel_and_id(channel, qq_id):
    return ftwc_config.channel_id_in_config(channel, qq_id)
