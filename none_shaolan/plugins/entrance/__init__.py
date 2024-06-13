import random

from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageEvent, Bot, ActionFailed

from config.constant import ignore_list, learn_word_channel_list, iupar_channel_list, superuser_list, \
    ignore_channel_list, is_lemmn
from plugins.bigwangchang import wangchang_config_add_channel_match, wangchang_config_remove_channel_match, \
    wangchang_config_remove_id_match, wangchang_match, random_wangchang, \
    add_channel_wangchang, remove_channel_wangchang, check_channel_and_id, on_image_receive_wangchang, \
    wangchang_config_add_id_match, add_id_wangchang, remove_id_wangchang
from plugins.catchwum import catch_wum_match, change_wum_background_image_match, \
    change_wum_background_image_process_params, show_wum_match, show_wum_process_param, show_system_wum_match, \
    show_wum_collect_progress_match, show_wum_collect_progress_process_params
from plugins.catchwum.catchwum import catch_wum
from plugins.checkstatus import check_group_status_process_params, check_group_status_match
from plugins.help import help_process_params, help_match
from plugins.iupar import iupar_message, iupar_delete_match, iupar_delete_word, process_raw_message, iupar_match, \
    add_channel_iupar, iupar_add_channel_match, iupar_remove_channel_match, remove_channel_iupar
from plugins.lemmndebug import lemmn_debug_add_wum_match, debug_add_wum
from plugins.makeoddwum import make_odd_wum_match, make_odd_wum_process_params, make_odd_history_match, \
    make_odd_history_process_params
from plugins.personalinfo import personal_info_command_match, personal_info_process_params
from plugins.ping import ping, ping_match
from plugins.protectwum import protect_wum_match, protect_cancel_wum_match, protect_wum_process_params, \
    protect_cancel_wum_process_params
from plugins.recyclewum import recycle_wum_process_params, recycle_wum_match, recycle_wum_rarity_match, \
    recycle_wum_rarity_process_params, recycle_wum_num_match, recycle_wum_num_process_params
from plugins.stealwum import steal_wum_match, steal_wum_history_process_params, steal_wum_process_params, \
    steal_wum_set_unit_match, steal_wum_set_unit_process_params, steal_wum_set_steal_strategy_process_params, \
    set_steal_strategy_match
from plugins.updateinfo import update_match, update_info
from plugins.wumblindbox import wum_blind_box_match, wum_blind_box_process_params
from utils.string_utls import get_message_sender, get_user_id, get_group_id

message_receive = on_message()


@message_receive.handle()
async def handle_function(event: MessageEvent, bot: Bot):
    triggered = False

    if event.anonymous is None and event.user_id and get_user_id(event) in superuser_list and get_group_id(event):
        msg = event.get_message()

        if await wangchang_config_add_channel_match(msg):
            triggered = True
            await message_receive.finish(await add_channel_wangchang(event))
        elif await wangchang_config_remove_channel_match(msg):
            triggered = True
            await message_receive.finish(await remove_channel_wangchang(event))
        elif await iupar_delete_match(msg):
            triggered = True
            await message_receive.finish(await iupar_delete_word(msg))
        elif await iupar_add_channel_match(msg):
            triggered = True
            await message_receive.finish(await add_channel_iupar(event))
        elif await iupar_remove_channel_match(msg):
            triggered = True
            await message_receive.finish(await remove_channel_iupar(event))

    if is_lemmn:
        msg = event.get_message()
        if await lemmn_debug_add_wum_match(msg):
            triggered = True
            await message_receive.finish(await debug_add_wum(event))

    if (event.anonymous is None and get_user_id(event) and get_user_id(event) not in ignore_list and get_group_id(event) and
            get_group_id(event) not in ignore_channel_list):
        msg = event.get_message()

        channel = get_group_id(event)
        qq_id = get_user_id(event)

        at_name = "ERROR!"
        if len(msg) > 1 and msg[1].type == 'at':
            at_id = msg[1].data['qq']
            at_user = await bot.get_group_member_info(group_id=int(channel), user_id=at_id)
            at_name = at_user['card'] if at_user['card'] else at_user['nickname']

        r = random.randint(0, 100)

        if await catch_wum_match(msg):
            await message_receive.finish(await catch_wum(get_user_id(event), get_message_sender(event)))
        elif await change_wum_background_image_match(msg):
            await message_receive.finish(await change_wum_background_image_process_params(msg, get_user_id(event)))
        elif await wangchang_config_add_id_match(msg):
            await message_receive.finish(await add_id_wangchang(event))
        elif await wangchang_config_remove_id_match(msg):
            await message_receive.finish(await remove_id_wangchang(event))
        elif await wangchang_match(msg):
            await message_receive.finish(await random_wangchang(msg, channel))
        elif await help_match(msg, event.to_me):
            await message_receive.finish(await help_process_params(event))
        elif await check_group_status_match(msg):
            await message_receive.finish(await check_group_status_process_params(event))
        elif await recycle_wum_rarity_match(msg):
            await message_receive.finish(await recycle_wum_rarity_process_params(event))
        elif await recycle_wum_num_match(msg):
            await message_receive.finish(await recycle_wum_num_process_params(event))
        elif await recycle_wum_match(msg):
            res = await recycle_wum_process_params(event)
            if res is not None:
                await message_receive.finish(res)
        elif await show_wum_match(msg):
            await message_receive.finish(await show_wum_process_param(event))
        elif await show_system_wum_match(msg):
            await message_receive.finish(await show_wum_process_param(event, True))
        elif await show_wum_collect_progress_match(msg):
            await message_receive.finish(await show_wum_collect_progress_process_params(event))
        elif await wum_blind_box_match(msg):
            await message_receive.finish(await wum_blind_box_process_params(event))
        elif await ping_match(msg):
            await message_receive.finish(await ping())
        elif await update_match(msg):
            await message_receive.finish(await update_info())
        elif await make_odd_wum_match(msg):
            await message_receive.finish(await make_odd_wum_process_params(event, channel))
        elif await make_odd_history_match(msg):
            await message_receive.finish(await make_odd_history_process_params(channel, bot))
        elif await protect_wum_match(msg):
            await message_receive.finish(await protect_wum_process_params(event))
        elif await protect_cancel_wum_match(msg):
            await message_receive.finish(await protect_cancel_wum_process_params(event))
        elif await set_steal_strategy_match(msg):
            await message_receive.finish(await steal_wum_set_steal_strategy_process_params(event))
        elif t := await steal_wum_match(msg):
            print("A:", msg, t)
            if t[1] == -1:
                await message_receive.finish(await steal_wum_history_process_params(event))
            else:
                await message_receive.finish(await steal_wum_process_params(event, t[1], at_name))
        elif not isinstance(t := await steal_wum_set_unit_match(msg), bool):
            print("B:", msg, t)
            await message_receive.finish(await steal_wum_set_unit_process_params(event, t))
        elif await personal_info_command_match(msg):
            await message_receive.finish(await personal_info_process_params(event))
        elif await iupar_match(msg):
            send_message = await iupar_message(msg, is_command=True)
            if send_message is not None:
                await message_receive.finish(send_message)
            else:
                print("LOG::IUPAR\t\t本条随机结果与原串相同")
        else:
            if get_user_id(event) != "3465450433" and channel in learn_word_channel_list and not triggered:
                await process_raw_message(msg)
            if r in range(75, 90) and get_user_id(event) != "3465450433":
                if channel in iupar_channel_list and not triggered:
                    send_message = await iupar_message(msg)
                    if send_message is not None:
                        await message_receive.finish(send_message)
                    else:
                        print("LOG::IUPAR\t\t本条随机结果与原串相同")
            elif r in range(90, 100):
                if await check_channel_and_id(channel, qq_id):
                    for i in msg:
                        if i.type == 'image':
                            res = await on_image_receive_wangchang(i)
                            if res is not None and not isinstance(res, str):
                                await message_receive.finish(res)
                                break
