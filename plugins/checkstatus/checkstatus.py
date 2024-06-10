from config.constant import iupar_channel_list
from config.global_object import ftwc_config


async def check_group_status_process(channel):
    res = f"{channel}的状态如下:\n"

    if channel in ftwc_config.channel_list:
        res += "畅神*会*在随机时间降临本群\n"
    else:
        res += "*不会*受到畅神眷顾\n"
    if channel in iupar_channel_list:
        res += "iupar is *watching* you"
    else:
        res += "iupar对这里*没有*兴趣"

    return res
