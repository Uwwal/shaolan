from config.constant import max_steal_power


def steal_power_to_string(power):
    if power < 10:
        return "他紫砂了..."
    elif power < 20:
        return "拿着村好剑在厕所深思"
    elif power < 40:
        return "小群之力"
    elif power < 60:
        return "也叱咤风雨了？"
    elif power < 80:
        return "在紫荆之巅 相思创爱"
    elif power < 100:
        return "保持 突破"
    elif power < 200:
        return "维系 前行"
    elif power < max_steal_power:
        return "百步的最后十步"
    else:
        return "你在这装逼什么"


def defend_power_to_string(power):
    if power < 10:
        return "好过什么都不做 真的？"
    elif power < 20:
        return "我敢说这段文本比上面的好"
    elif power < 40:
        return "尝试精简"
    elif power < 60:
        return "问问谁敢偷你"
    elif power < 80:
        return "于杏林之谧 连环相连"
    elif power < 100:
        return "溶液中难溶解的固体物质从溶液中释出"
    elif power < 200:
        return "我不想编了 我们之后再见"
    elif power < max_steal_power:
        return "百步的最后十步"
    else:
        return "你在这装逼什么"

