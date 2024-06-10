import nonebot
from nonebot.adapters.onebot.v11 import Adapter

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.load_plugins("none_shaolan/plugins")

if __name__ == "__main__":
    nonebot.run()
