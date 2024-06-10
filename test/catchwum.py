# def sync_function():
#     loop = asyncio.get_event_loop()
#     return loop.run_until_complete(catch_wum_test())
#
# async def catch_wum_test():
#     j = {
#         "wums": {
#             "巨鹿wum": 1,
#             "o wum": 1,
#             "睡眠wum": 1,
#             "后墙wum": 1,
#             "无鹿wum": 1,
#             "niconico wum": 1,
#             "wuw": 1,
#             "旋转wum": 1,
#             "wum": 1,
#             "顽皮wum": 1,
#             "脸wum": 1,
#             "海盗wum": 1,
#             "微笑wum": 1,
#             "眯眯wum": 1,
#             "无耳wum": 1,
#             "吃洋葱wum": 1,
#             "惊讶wum": 1,
#             "死亡wum": 1,
#             "风暴wum": 1,
#             "开心wum": 1,
#             "福禄wum": 1,
#             "爱可wum": 1,
#             "宿敌wum": 1,
#             "偷窥wum": 1,
#             "笨蛋wum": 1,
#             "无wum": 1,
#             "翻转muw": 1,
#             "这啥wum": 1,
#             "疑惑wum": 1,
#             "韵律wum": 1,
#             "暗影wum": 1,
#             "哭哭wum": 1,
#             "伤感wum": 1,
#             "紧张wum": 1,
#             "极乐wum": 1,
#             "w wum": 1,
#             "无面wum": 1,
#             "无嘴wum": 1,
#             "锯齿wum": 1,
#             "乏味wum": 1,
#             "说话wum": 1,
#             "皮肤wum": 1,
#             "小眼wum": 1,
#             "毛球wum": 1,
#             "大可爱wum": 1,
#             "四鹿wum": 1,
#             "困惑wum": 1,
#             "双生wum": 1,
#             "狼wum": 1,
#             "啊啊啊啊啊啊wum": 1,
#             "啊啊wum": 1,
#             "害羞wum": 1,
#             "uwu wum": 1,
#             "^^ wum": 1,
#             "伤心wum": 1,
#             "恋爱wum": 1,
#             "鼻子wum": 1,
#             "平滑wum": 1,
#             "陈旧wum": 1,
#             "玉米wum": 1,
#             "喜怒wum": 1,
#             "猪wum": 1,
#             "六点wum": 1,
#             "翻转mnw": 1,
#             "可爱wum": 1,
#             "肥wum": 1,
#             "惊惊惊wum": 1,
#             "mum": 1
#         },
#         "last_time": -1,
#         "wums_rarity_count": [327, 179, 82, 37, 0],
#         "coins": 0
#     }
#
#     w1 = WumInventory('test1')
#     w1.data = j
#     w2 = WumInventory('test2')
#     w2.data = j
#     w3 = WumInventory('test3')
#     w3.data = j
#     w4 = WumInventory('test4')
#     w4.data = j
#     w5 = WumInventory('test5')
#     w5.data = j
#     w1.save()
#     w2.save()
#     w3.save()
#     w4.save()
#     w5.save()
#
#     w1 = WumInventory('test1')
#     w2 = WumInventory('test2')
#     w3 = WumInventory('test3')
#     w4 = WumInventory('test4')
#     w5 = WumInventory('test5')
#
#     w1.catch_wum()
#     w2.catch_wum()
#     w3.catch_wum()
#     w4.catch_wum()
#     w5.catch_wum()
#
#
# sync_function()