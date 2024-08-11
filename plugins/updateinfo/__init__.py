from utils.command_match import command_match

command = "=update"

"""
update相关:
=update: 看最近几次更新内容
"""


async def update_match(msg):
    return await command_match(msg, command)


async def update_info():
    return ("0711:价格已修改\n"
            "0622:略微提高大盲盒出典概率\n"
            "0621:预计在不久后将价格从稀有度相关调整为库存单种数目相关, 勿谓言之不预\n"
            "0621:优化代码, 如果出现图发不出请到处乱叫\n"
            "0613:增加更多可异化wum，异化help增强，加入异化历史\n"
            "0612:增加更多可异化wum\n"
            "0612:教你笑点解析bot, 成为见解独特的黑马用户: 发送=help\n"
            "0611:异化wum\n"
            "0610:迁移到了新的框架, 艾特问题应该修好了, 若出现存档丢失欢迎联系\n"
            "0609:偷wum已部署, 记得看help, 被偷了建议发动外交攻势\n"
            "0606:偷wum框架已完成, 测试进群732908053\n"
            "0605:wum奖池优化了10倍速度, 抓wum优化了7倍速度, 偷wum还在开发, 别急\n"
            "0605:已恢复, 补偿5币, 废品哥出钱。\n"
            "0604:数据库被临时工wum删了, 将缺失典发往lemmncat@gmail.com或者反馈群将在0605统一补\n"
            "0604:偷wum火热开发中，指导意见：提升wum数量\n0603:wum进度")
