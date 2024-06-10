import asyncio

from models.wum_inventory import WumInventory
from plugins.catchwum.catchwum import catch_wum
from plugins.stealwum import steal_wum


def main():
    asyncio.run(catch_wum("1","2"))

    print(asyncio.run(steal_wum("3476365499", "1", "TEST", "TEST")))


if __name__ == "__main__":
    main()
