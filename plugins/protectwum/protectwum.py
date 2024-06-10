from models.wum_pool import wum_pool


async def protect_wum(qq_id, wum_name, is_protected):
    wum_inventory = wum_pool.get_inventory(qq_id)

    if isinstance(wum_inventory, str):
        return wum_inventory

    wums = wum_inventory.data["wums"]

    if wum_name not in wums.keys():
        wum_pool.release_inventory(qq_id)
        return "帮你想: 你有这种wum吗"

    wum_inventory.change_is_protected(wum_name,is_protected)

    wum_pool.release_inventory(qq_id)

    if is_protected:
        return f"喜收藏, 又何妨, {wum_name}狠狠爱"
    else:
        return f"{wum_name}又做错了什么呢"
