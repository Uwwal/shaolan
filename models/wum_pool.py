from models.wum_inventory import WumInventory


class WumPool:
    def __init__(self):
        self.wum_pool = []

    def get_inventory(self, qq_id):
        if qq_id in self.wum_pool:
            return "少抽wum多鹿馆"
        self.wum_pool.append(qq_id)
        return WumInventory(qq_id)

    def release_inventory(self, qq_id):
        if qq_id in self.wum_pool:
            self.wum_pool.remove(qq_id)


wum_pool = WumPool()

system_inventory = WumInventory("system")
