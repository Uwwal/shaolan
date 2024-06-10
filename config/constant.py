import os

# main start

cur_path = os.getcwd()

lemmn_qq = "3408183732"
is_lemmn = True

# cur_path = os.path.join(cur_path, "..")
# print(cur_path)

bot_qq = "1077230687"
if is_lemmn:
    bot_qq = lemmn_qq

learn_word_channel_list = ["560954591", "617557230", "897380826"]
ignore_list = [bot_qq, "1006130858", "2362510272"]
ignore_channel_list = []
if not is_lemmn:
    ignore_channel_list.append("732908053")
iupar_channel_list = ["560954591", "783925178", "617557230", "897380826", "178362967"]
superuser_list = ["3476365499", "3165862735"]

# dir start
wums_dir = os.path.join(cur_path, 'data', 'catchwum', 'wums')

background_dir = os.path.join(cur_path, 'data', 'catchwum', 'bg')

font_path = os.path.join(cur_path, 'fonts', 'msyh.ttc')

# wangchang start
wangchang_path = os.path.join(cur_path, 'plugins', 'bigwangchang', 'wangchang.png')
ludan_path = os.path.join(cur_path, 'plugins', 'bigwangchang', 'ludan.png')
wum_path = os.path.join(cur_path, 'plugins', 'bigwangchang', 'wum.png')
yushe_path = os.path.join(cur_path, 'plugins', 'bigwangchang', 'yushe.png')
nielian_path = os.path.join(cur_path, 'plugins', 'bigwangchang', 'nielian.png')

wangchang_img_arg_name_list = ['王畅', '卤蛋', 'wum', '羽蛇', '捏脸', '镜镜', '像像']
wangchang_img_path_list = [wangchang_path, ludan_path, wum_path, yushe_path, nielian_path, '镜镜', '像像']

wangchang_img_num = len(wangchang_img_arg_name_list)

side_length_list = [135, 251, 401, 289, 518, -1, -1]
middle_point_list = [(-0.5, -4.5), (-0.5, -5.5), (23.5, -5.5), (-25.5, -3.5), (-11, -219), (-1, -1), (-1, -1)]
multi_scale_list = [1.3, 1.3, 1.3, 1.6, 1.4, 1, 1]

default_wangchang_num = 15
default_nielian_num = 5

# recycle start

matong_gif_path = os.path.join(cur_path, 'data', 'recyclewum', 'matong.gif')

# wum start
recycle_sum_coin = 4

yi_wum_recycle_price = 2
dian_wum_recycle_price = 5

yi_rarity = 5
dian_rarity = 6

system_catch_wum_p = [0, 0, 0, 0, 0, 100]
user_catch_wum_p = [50, 30, 15, 5, 0, 0]

recycle_coin_list = [0.2, 0.6, 1.2, 2.0]

keep_wum_rarity_num = [20, 30, 60, 50, 999, 999]

wum_page_capacity = 40

wum_collect_score_list = [1, 3, 6, 10, 20, 25]

# base 1
# colorful + 2
# odd + 1
# yi wum = 5
# dian wum = 6

wum_rarity_num = 6

wums_rarity_dict = {
    "niconico wum": 1,
    "o wum": 1,
    "uwu wum": 1,
    "w wum": 1,
    "wum": 1,
    "^^ wum": 1,
    "乏味wum": 1,
    "伤心wum": 2,  # odd
    "伤感wum": 1,
    "偷看wum": 2,  # odd
    "六点wum": 2,  # odd
    "双生wum": 2,  # odd
    "可爱wum": 1,
    "吃洋葱wum": 4,  # colorful odd
    "后墙wum": 2,  # odd
    "呲牙wum": 1,
    "哭哭wum": 3,  # colorful
    "啊啊wum": 1,
    "啊啊啊啊啊啊wum": 2,  # odd
    "喜怒wum": 1,
    "四目wum": 1,
    "困惑wum": 2,  # odd
    "圣诞wum": 4,  # colorful odd
    "大可爱wum": 1,
    "害羞wum": 3,  # colorful
    "小眼wum": 1,
    "巨目wum": 2,  # odd
    "平滑wum": 1,
    "开心wum": 3,  # colorful
    "微笑wum": 1,
    "惊惊惊讶wum": 2,  # odd
    "惊讶wum": 2,  # odd
    "旋转wum": 1,
    "无wum": 2,  # odd
    "无嘴wum": 1,
    "无目wum": 1,
    "无耳wum": 2,  # odd
    "无面wum": 2,  # odd
    "暗影wum": 4,  # colorful odd
    "极乐wum": 3,  # colorful
    "死亡wum": 1,
    "毛球wum": 2,  # odd
    "海盗wum": 2,  # odd
    "爬wum": 2,  # odd
    "爱可wum": 1,
    "狼wum": 1,
    "玉米wum": 4,  # colorful odd
    "疑惑wum": 2,  # odd
    "皮顽wum": 1,
    "眯眯wum": 1,
    "睡眠wum": 2,  # odd
    "福瑞wum": 1,
    "笨蛋wum": 1,
    "紧张wum": 1,
    "翻转mnw": 2,  # odd
    "翻转muw": 1,
    "肥wum": 2,  # odd
    "脸wum": 2,  # odd
    "说话wum": 2,  # odd
    "这啥wum": 2,  # odd
    "陈睿wum": 3,  # colorful
    "韵律wum": 1,
    "顽皮wum": 1,
    "风暴wum": 4,  # colorful odd
    "鼻子wum": 1,
    "恋恋wum": 2,  # odd
    "wuw": 1,
    "mum": 1,
    "宿命wum": 4,  # colorful odd
    "雅典娜wum": 6,  # blind box
    "娜典雅wum": 6,  # blind box
    "wum什戴尔": 6,  # blind box
    "wum守": 6,  # blind box
    "史莱wum王": 6,  # blind box
    "puzzle wum": 3,  # colorful
    "巨大wum": 2,  # odd
    "pou": 2,  # odd
    "mope wum": 3,  # colorful
}

max_wum_name_len = 0
for i in wums_rarity_dict.keys():
    max_wum_name_len = max(max_wum_name_len, len(i))

# steal start

wum_steal_power_list = [1, 2, 3, 5, 10, 20]
wum_defend_power_list = wum_steal_power_list

wum_type_complexly_effect_list = [0.01, 0.02, 0.03, 0.05, 0.07, 0.1]

max_steal_power = 300
max_defend_power = 300

base_steal_power = 0
base_defend_power = 10
base_complexly_multiple = 1.1

steal_strategy_string_list = ["注重稀有", "防卫破坏", "拿钱就跑"]
steal_strategy_power_multiple_list = [0.7, 1.3, 0.9]
steal_strategy_base_success_rate_list = [40, 70, 70]

steal_strategy_max_gain_wum_list = [2, 3, 0]

steal_wum_trophy_weight_list = [10, 20, 30, 50, 70, 100]

# help start

help_command_param_list = ["偷wum"]
help_docs_dict = {
    "偷wum": [
        "偷wum相关: \n"
        "你好啊，我是兼任偷窃之神的防卫哥，就由我给你说明吧！\n"
        "首先偷wum要组建wum行动队\n"
        "没有行动队就大张旗鼓去偷可不行*摇手指*\n"
        "行动队能力与队伍中wum数量与wum种类强相关\n"
        "行动成功率与距上次偷窃累计抓wum次数、行动策略有关\n"
        "既然说到行动策略就顺便提一下\n"
        "不同行动策略有不同的行动能力加成、成功率加成、产出加成\n"
        "当然也有可能是减成(笑)\n"
        "如果你想保护自己的wum的话，记住以下几点很重要\n"
        "首先就是设置防卫队，防卫队更容易替代wum库与行动队反应\n"
        "然后就是偷wum后累计的抓wum次数也会提升防御能力\n"
        "当然你也可以反击那些偷你的坏家伙，也是一种不错的防卫呢(笑)\n"
        "主要机制就这些，具体数值我也不懂，顺从本心就好\n"
        "预祝行动顺利"
    ]
}
