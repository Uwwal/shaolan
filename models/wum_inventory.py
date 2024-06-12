import random
from datetime import datetime, timedelta
import json

from config.constant import wum_rarity_num, base_steal_power, \
    wum_steal_power_list, base_defend_power, base_complexly_multiple, wum_type_complexly_effect_list, \
    wum_defend_power_list, steal_strategy_power_multiple_list, max_defend_power, max_steal_power, catch_wum_odd_point
from config.global_object import catchwum_collection, wum_rarity_dict_list
from utils.wum_steal_utils import query_steal_wum_record
from utils.wum_utils import get_rarity, get_wum_rarity_weight

default_attribute_list = [
    ("wums", {}),
    ("last_time", -1),
    ("wums_rarity_count", [0] * wum_rarity_num),
    ("coins", 0),
    ("last_steal_catchwum_count", 0),
    ("steal_unit", {}),
    ("defend_unit", {}),
    ("steal_strategy", 0),
    ("steal_history_list", [[], []]),
    ("steal_new_count", 0),
    ("odd_point", 0),
]


class WumInventory:
    def __init__(self, qq_id):
        self.qq_id = qq_id
        self.data = self.load()

    def load(self, is_debug=True):
        query = {"id": self.qq_id}
        result = catchwum_collection.find_one(query)

        if result is None:
            default_data = {}
            for i in default_attribute_list.copy():
                default_data.update({i[0]: i[1]})
                print("default data", i)
            return default_data

        data = result["content"]
        print("data", data)

        for i in default_attribute_list.copy():
            if i[0] not in data:
                data.update({i[0]: i[1]})

        if isinstance(data, str):
            data = json.loads(data)

        if "wums" in data and data["wums"] is not None:
            for k, v in data["wums"].items():
                if isinstance(v, int):
                    data["wums"][k] = {"num": v, "isProtected": False}

        if is_debug:
            data.update({"wums_rarity_count": self.get_wums_rarity_count_from_file(data["wums"])})
        elif "wums_rarity_count" not in data or len(data['wums_rarity_count']) < wum_rarity_num:
            data.update({"wums_rarity_count": self.get_wums_rarity_count_from_file(data["wums"])})

        return data

    async def get_steal_power(self):
        unit = self.data["steal_unit"]

        strategy = self.data["steal_strategy"]
        i = strategy
        strategy_multiple = steal_strategy_power_multiple_list[i]

        l = len(unit)

        power = base_steal_power

        complexly_multiple = base_complexly_multiple

        if unit:
            for wum_name, num in unit.items():
                rarity = get_rarity(wum_name)
                power += num * wum_steal_power_list[rarity - 1]
                if l != 1:
                    complexly_multiple *= 1 - wum_type_complexly_effect_list[rarity - 1]

        return min(
            power * complexly_multiple * strategy_multiple * await self.calculate_steal_catchwum_count_multiple(),
            max_steal_power)

    async def get_defend_power(self):
        unit = self.data["defend_unit"]

        l = len(unit)

        power = base_defend_power

        complexly_multiple = base_complexly_multiple

        if unit:
            for wum_name, num in unit.items():
                rarity = get_rarity(wum_name)
                power += num * wum_defend_power_list[rarity - 1]
                if l != 1:
                    complexly_multiple *= 1 - wum_type_complexly_effect_list[rarity - 1]

        return min(power * complexly_multiple * await self.calculate_steal_catchwum_count_multiple(is_defend=True),
                   max_defend_power)

    async def set_steal_unit(self, wum_dict, save=True):
        self.data["steal_unit"] = wum_dict
        if save:
            self.save()

    async def set_defend_unit(self, wum_dict, save=True):
        self.data["defend_unit"] = wum_dict
        if save:
            self.save()

    async def set_steal_strategy(self, index, save=True):
        # steal_strategy_string_list.index
        self.data["steal_strategy"] = index
        if save:
            self.save()

    async def insert_steal_history(self, index, r_id, save=True):
        # 0 steal 1 defend
        self.data["steal_history_list"][index].append(r_id)

        if len(self.data["steal_history_list"][index]) > 5:
            self.data["steal_history_list"][index].pop(0)

        if save:
            self.save()

    async def query_steal_history(self):
        r = []
        for history_list in self.data["steal_history_list"]:
            t = []
            for i in history_list:
                t.append(await query_steal_wum_record(i))
            r.append(t)
        return r

    async def calculate_steal_catchwum_count_multiple(self, is_defend=False):
        count = self.data["last_steal_catchwum_count"]

        base = 0.8 if is_defend else 0.5

        if count == 0:
            return base
        else:
            return base + 0.15 + count * 0.1

    async def add_last_steal_catchwum_count(self, save=True):
        self.data["last_steal_catchwum_count"] += 1
        if save:
            self.save()

    async def clear_last_steal_catchwum_count(self, save=True):
        self.data["last_steal_catchwum_count"] = 0
        if save:
            self.save()

    def get_wums_rarity_count_from_file(self, wums):
        res = [0] * wum_rarity_num

        for k, v in wums.items():
            res[get_rarity(k) - 1] += v["num"]

        return res

    def save(self):
        if self.data is None or self.data == {}:
            print(self.qq_id, "SAVE ERROR")
            return False

        query = {"id": self.qq_id}
        update_data = {"$set": {"content": self.data}}
        catchwum_collection.update_one(query, update_data, upsert=True)

    def add_wum(self, wum_name, num, save=True):
        rarity = get_rarity(wum_name)

        if wum_name not in self.data["wums"]:
            self.data["wums"][wum_name] = {"num": 0, "isProtected": False}

        self.data["wums"][wum_name]["num"] += num

        self.data["wums_rarity_count"][rarity - 1] += num
        if save:
            self.save()

    def catch_wum(self, save=True):
        system = self.qq_id == 'system'

        now = datetime.now()

        last_time = self.data["last_time"]
        if last_time != -1 and not system:
            last_datetime = datetime.fromtimestamp(last_time)
            if now - last_datetime < timedelta(hours=4):
                time_difference = now - last_datetime

                remaining_time = timedelta(hours=4) - time_difference

                hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)

                time_difference_str = "下一只wum还要等\n" \
                                      f"        {int(hours)}小时{int(minutes)}分{int(seconds)}秒\n\n\n" \
                                      "才能成熟"

                return False, time_difference_str, f"{int(hours)}小时{int(minutes)}分{int(seconds)}秒"

        new_wum, num = self.random_wum(system)

        self.data["last_time"] = int(now.timestamp())
        self.add_wum(new_wum.name, num, save)

        if not system:
            self.add_odd_point(new_wum.name, save)

        return True, new_wum, num

    def random_wum(self, system=False):
        rarity = random.choices(list(range(1, wum_rarity_num + 1)), weights=get_wum_rarity_weight(system), k=1)[0]

        new_wum = random.choice(wum_rarity_dict_list[rarity])

        num = random.choice([1, 2, 3])

        return new_wum, num

    def delete_wum(self, wum_name, num, save=True, is_recycle=True, is_steal=False):  # steal fail
        rarity = get_rarity(wum_name)

        cur_num = self.data["wums"][wum_name]["num"]
        if is_recycle:
            self.data["wums"][wum_name]["num"] -= num
            cur_num -= num
            if wum_name in self.data["steal_unit"] and self.data["steal_unit"][wum_name] > cur_num:
                if cur_num <= 0:
                    del self.data["steal_unit"][wum_name]
                else:
                    self.data["steal_unit"][wum_name] = cur_num
            if wum_name in self.data["defend_unit"] and self.data["defend_unit"][wum_name] > cur_num:
                if cur_num <= 0:
                    del self.data["defend_unit"][wum_name]
                else:
                    self.data["defend_unit"][wum_name] = cur_num
        elif is_steal:
            self.data["wums"][wum_name]["num"] -= num
            cur_num -= num
            if wum_name in self.data["steal_unit"]:
                self.data["steal_unit"][wum_name] -= num
                if cur_num <= 0:
                    del self.data["steal_unit"][wum_name]
                elif self.data["steal_unit"][wum_name] <= 0:
                    del self.data["steal_unit"][wum_name]
            if wum_name in self.data["defend_unit"]:
                self.data["defend_unit"][wum_name] -= num
                if cur_num <= 0:
                    del self.data["defend_unit"][wum_name]
                elif self.data["defend_unit"][wum_name] <= 0:
                    del self.data["defend_unit"][wum_name]
        if cur_num <= 0:
            del self.data["wums"][wum_name]

        self.data["wums_rarity_count"][rarity - 1] -= num

        if save:
            self.save()

    def top_up(self, coins, save=True):
        self.data["coins"] += coins
        self.data["coins"] = round(self.data["coins"], 4)
        if save:
            self.save()

    def payout(self, coins, save=True):
        self.data["coins"] -= coins
        self.data["coins"] = round(self.data["coins"], 4)
        if save:
            self.save()

    def change_is_protected(self, wum_name, is_protected):
        self.data["wums"][wum_name]["isProtected"] = is_protected
        self.save()

    async def add_steal_new_count(self, save=True):
        self.data["steal_new_count"] += 1
        if save:
            self.save()

    async def clear_steal_new_count(self, save=True):
        self.data["steal_new_count"] = 0
        if save:
            self.save()

    def add_odd_point(self, wum_name, save=True):
        rarity = get_rarity(wum_name)

        cur_odd_point = self.data["odd_point"]

        cur_odd_point += catch_wum_odd_point[rarity - 1]

        cur_odd_point = min(100, cur_odd_point)

        self.data["odd_point"] = cur_odd_point

        if save:
            self.save()

    def clear_odd_point(self, save=True):
        self.data["odd_point"] = 0

        if save:
            self.save()
