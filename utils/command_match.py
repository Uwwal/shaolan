async def command_match(msg, command="", support_quote=False):
    if msg:
        i = 0
        tag = msg[0].type
        if support_quote and tag == 'quote':
            i = 1
            len_msg = len(msg)
            if len_msg > 1:
                tag = msg[1].type
            if tag == 'at':
                i = 2
                if len_msg > 2:
                    tag = msg[2].type

        if tag == 'text' and msg[i].data["text"].replace(" ", "").startswith(command):
            # new_msg = msg
            # new_msg[0].data['text'][len(command):].strip()
            # return new_msg

            return True

    return False


async def command_match_strict(msg, command=""):
    if msg and msg[0].type == 'text':
        return msg[0].data["text"].replace(" ", "") == command
    return False


async def command_match_list(msg, command_list=None):
    if command_list is None:
        command_list = []

    for command in command_list:
        if await command_match(msg, command):
            return True

    return False
