from config.constant import keep_wum_rarity_num, recycle_sum_coin
from models.wum_pool import system_inventory
from plugins.calculateprice.calculate_price import calculate_price
from utils.wum_utils import get_rarity, get_wum_rarity_weight


def test():
    wums = system_inventory.data["wums"]

    rarity_weight = get_wum_rarity_weight()

    system_gain_coins = 0

    for wum_name, l in wums.items():
        num = l["num"]

        rarity = get_rarity(wum_name)

        for i in range(num - keep_wum_rarity_num[rarity - 1]):
            coin = calculate_price(rarity, rarity_weight, recycle_sum_coin)

            system_gain_coins += coin

            system_inventory.delete_wum(wum_name, 1)

    print(system_gain_coins)

    if system_gain_coins != 0:
        system_gain_coins = round(system_gain_coins, 4)

        system_inventory.top_up(system_gain_coins)

if __name__ == "__main__":
    test()
