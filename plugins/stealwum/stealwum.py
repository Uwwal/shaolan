import datetime
import random

from config.constant import base_defend_power, steal_strategy_base_success_rate_list, steal_strategy_max_gain_wum_list, \
    base_steal_power, steal_wum_trophy_weight_list, steal_strategy_string_list
from models.wum_pool import wum_pool
from plugins.stealwum.historytoimage import history_to_image
from utils.wum_steal_utils import insert_steal_wum_new_record
from utils.wum_utils import get_rarity


async def steal_wum(qq_id, at_id, qq_name, at_name):
    print("steal start", qq_id, at_id, qq_name, at_name)

    user_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(user_inventory, str):
        return user_inventory

    at_inventory = wum_pool.get_inventory(at_id)

    if isinstance(at_inventory, str):
        wum_pool.release_inventory(qq_id)
        return at_inventory

    steal_power = await user_inventory.get_steal_power()
    defend_power = await at_inventory.get_defend_power()

    print("power", steal_power, defend_power)

    if steal_power == base_steal_power:
        wum_pool.release_inventory(qq_id)
        wum_pool.release_inventory(at_id)
        return "帮你想: 你的队空"

    if defend_power is None:
        defend_power = base_defend_power

    steal_strategy = user_inventory.data["steal_strategy"]
    success_rate = steal_strategy_base_success_rate_list[steal_strategy]

    delta_power = steal_power - defend_power
    delta_rate = (delta_power / defend_power) * 100
    success_rate += delta_rate

    success_rate = min(int(success_rate), 100)
    trophy = None

    r = random.randint(1, 100)

    print("success_rate", delta_power, success_rate, r)

    res = "操你妈"

    if r <= success_rate:
        success = True

        if steal_strategy == 0:
            at_wums = list(at_inventory.data["wums"].items())

            at_wums.sort(key=lambda x: get_rarity(x[0]), reverse=True)

            l = len(at_wums)
            loop_time = min(steal_strategy_max_gain_wum_list[steal_strategy], l)

            index = 0
            gain_wum_list = []
            for i in range(loop_time):
                while True:
                    if index >= l:
                        break

                    wum_name = at_wums[index][0]

                    rarity = get_rarity(wum_name)

                    index += 1

                    if steal_wum_trophy_weight_list[rarity - 1] > success_rate:
                        if rarity == 1:
                            break
                        continue

                    success_rate -= steal_wum_trophy_weight_list[rarity - 1]

                    gain_wum_list.append((wum_name, 1))

                    at_inventory.delete_wum(wum_name, 1, save=False)

                    user_inventory.add_wum(wum_name, 1, save=False)
            res = f"{qq_id} vs {at_id}, 你赢了!\n获得wum:{gain_wum_list}"
            trophy = gain_wum_list
        elif steal_strategy == 1:
            at_wums = list(at_inventory.data["defend_unit"].items())

            if at_wums:
                at_wums.sort(key=lambda x: get_rarity(x[0]), reverse=True)

                l = len(at_wums)
                loop_time = min(steal_strategy_max_gain_wum_list[steal_strategy], l)

                index = 0
                gain_wum_list = []
                for i in range(loop_time):
                    while True:
                        if index >= l:
                            break

                        wum_name = at_wums[index][0]

                        rarity = get_rarity(wum_name)

                        index += 1

                        if steal_wum_trophy_weight_list[rarity - 1] > success_rate:
                            if rarity == 1:
                                break
                            continue

                        success_rate -= steal_wum_trophy_weight_list[rarity - 1]

                        gain_wum_list.append((wum_name, 1))

                        at_inventory.delete_wum(wum_name, 1, save=False, is_recycle=False, is_steal=True)

                        user_inventory.add_wum(wum_name, 1, save=False)

                res = f"{qq_id} vs {at_id}, 你赢了!\n获得wum:{gain_wum_list}"

                trophy = gain_wum_list
            else:
                wum_pool.release_inventory(qq_id)
                wum_pool.release_inventory(at_id)

                return "收手吧, 他们已经没法反抗了"
        elif steal_strategy == 2:
            power_coin = await rate_to_coin(r)

            gain_coin = min(power_coin, at_inventory.data["coins"])

            at_inventory.payout(gain_coin, save=False)
            user_inventory.top_up(gain_coin, save=False)
            res = f"{qq_id} vs {at_id}, 你赢了!\n获得wum币:{gain_coin}"

            trophy = gain_coin
    else:
        success = False

        rate = (delta_power / steal_power) * 100

        lose_wum_list = []
        unit = user_inventory.data['steal_unit']

        if rate < - 80:
            key_list = list(unit.keys())

            if len(key_list) >= 3:
                wum_name_list = random.sample(key_list, 3)
            else:
                wum_name_list = key_list

            for wum_name in wum_name_list:
                lose_wum_list.append((wum_name, 1 + unit[wum_name] // 4))

        elif rate < - 40:
            key_list = list(unit.keys())

            if len(key_list) >= 2:
                wum_name_list = random.sample(key_list, 2)
            else:
                wum_name_list = key_list

            for wum_name in wum_name_list:
                lose_wum_list.append((wum_name, 1 + unit[wum_name] // 4))
        elif rate < 0:
            wum_name = random.choice(list(unit.keys()))

            lose_wum_list.append((wum_name, 1 + unit[wum_name] // 4))
        elif rate < 20:
            wum_name = random.choice(list(unit.keys()))

            lose_wum_list.append((wum_name, 1 + unit[wum_name] // 10))

        print("lose", lose_wum_list)

        for i in lose_wum_list:
            print(i[0], i[1])
            user_inventory.delete_wum(i[0], i[1], save=False, is_recycle=False, is_steal=True)
            at_inventory.add_wum(i[0], i[1], save=False)

        print(f"{qq_id}, {at_id}, fail, strategy: {steal_strategy}, {rate}")

        res = f"{qq_id} vs {at_id}, 你输了!\n损失如下: {lose_wum_list}"

        trophy = lose_wum_list

    current_time = datetime.datetime.now()

    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    record = {"content": {
        "qq_id": qq_id,
        "qq_name": qq_name,
        "at_id": at_id,
        "at_name": at_name,
        "success": success,
        "steal_strategy": steal_strategy,
        "trophy": trophy,
        "time": formatted_time
    }}

    r_id = await insert_steal_wum_new_record(record)

    await user_inventory.insert_steal_history(0, r_id, qq_id, at_id, save=False)
    await at_inventory.insert_steal_history(1, r_id, qq_id, at_id, save=False)

    await user_inventory.clear_last_steal_catchwum_count(save=False)
    await at_inventory.add_steal_new_count(save=False)

    user_inventory.save()
    at_inventory.save()

    wum_pool.release_inventory(qq_id)
    wum_pool.release_inventory(at_id)

    print(res)

    return res


async def set_steal_unit(qq_id, wum_dict):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    for wum_name, num in wum_dict.items():
        if wum_name not in wum_inventory.data["wums"] or wum_inventory.data["wums"][wum_name]["num"] < num:
            wum_pool.release_inventory(qq_id)
            return f"帮你想: 你有{num}只{wum_name}吗？"

    await wum_inventory.set_steal_unit(wum_dict, save=True)

    wum_pool.release_inventory(qq_id)

    return str(wum_dict)


async def set_defend_unit(qq_id, wum_dict):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    for wum_name, num in wum_dict.items():
        if wum_name not in wum_inventory.data["wums"] or wum_inventory.data["wums"][wum_name]["num"] < num:
            wum_pool.release_inventory(qq_id)
            return f"帮你想: 你有{num}只{wum_name}吗？"

    await wum_inventory.set_defend_unit(wum_dict, save=True)

    wum_pool.release_inventory(qq_id)

    return str(wum_dict)


async def set_steal_strategy(qq_id, index):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    await wum_inventory.set_steal_strategy(index, save=True)

    wum_pool.release_inventory(qq_id)

    return f"{qq_id}, {index}"


async def rate_to_coin(rate):
    coin = 0

    if rate < 10:
        coin += rate / 5
        return round(coin, 4)
    else:
        coin += 2
        rate -= 10

        if rate < 24:
            coin += rate / 8
            return round(coin, 4)

        else:
            coin += 3
            rate -= 24

            coin += rate / 15
            return round(coin, 4)


async def steal_wum_history(qq_id, name):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    history = await wum_inventory.query_steal_history()

    steal = history[0]
    defend = history[1]

    wum_pool.release_inventory(qq_id)

    solve_res = [[], []]

    i = 0
    while True:
        if i == len(steal):
            break

        if steal[i]['content']['qq_id'] != qq_id:
            steal.pop(i)
            continue

        is_success = steal[i]['content']['success']
        solve_res[0].append({
            'qq_name': name,
            'other_name': steal[i]['content']['at_name'] if 'at_name' in steal[i]['content'] else '神必人',
            'other_qq': steal[i]['content']['at_id'],
            'is_success_hint': '你赢了!' if is_success else '你输了!',
            'is_success_user': is_success,
            'trophy_hint': '战利品:' if is_success else '损失wum:',
            'trophy': steal[i]['content']['trophy'],
            'strategy': steal_strategy_string_list[steal[i]['content']['steal_strategy']],
            'time_hint': '时间:',
            'time': steal[i]['content']['time'] if 'time' in steal[i]['content'] else '我忘了'
        })

        i += 1

    i = 0
    while True:
        if i == len(defend):
            break

        if defend[i]['content']['at_id'] != qq_id:
            defend.pop(i)
            continue

        is_success = defend[i]['content']['success']
        solve_res[1].append({
            'qq_name': name,
            'other_name': defend[i]['content']['qq_name'] if 'qq_name' in defend[i]['content'] else '神必人',
            'other_qq': defend[i]['content']['qq_id'],
            'is_success_hint': '你输了!' if is_success else '你赢了!',
            'is_success_user': not is_success,
            'trophy_hint': '损失:' if is_success else '缴获wum:',
            'trophy': defend[i]['content']['trophy'],
            'strategy': steal_strategy_string_list[defend[i]['content']['steal_strategy']],
            'time_hint': '时间:',
            'time': defend[i]['content']['time'] if 'time' in defend[i]['content'] else '我忘了'
        })

        i += 1

    return await history_to_image(solve_res, name)
