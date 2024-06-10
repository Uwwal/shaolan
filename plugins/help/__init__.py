from config.constant import bot_qq, help_command_param_list, help_docs_dict
from plugins.help.help import docs_help
from utils.command_match import command_match
from utils.string_utls import get_event_command_text

command = "=help"


async def help_match(msg, to_me):
    t = await command_match(msg, command)
    if t:
        return t

    if to_me and msg[0].type == 'text':
        text = msg[0].data['text'].strip()

        if text == 'help' or text == '帮助':
            return True

    return False


async def help_process_params(event):
    text = await get_event_command_text(event)
    args = text.strip()[len(command):].strip()

    if len(args) == 0:
        return await docs_help()

    if args in help_command_param_list:
        return await docs_help(args + "详细帮助", help_docs_dict[args])

    return await docs_help()
