from utils.command_match import command_match

command = "=ping"

"""
ping相关:
=ping: 还能说话吗
"""


async def ping_match(msg):
    return await command_match(msg, command)


async def ping():
    return "岑"
