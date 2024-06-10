default_word = {'ns': ["大学", "山洞"],
                'nr': ["老者"],
                'n': ["作业", "魔法", "吉他", "水杯"],
                't': ["未来", "下午"],
                'a': ["尘封", "巨大", "普通", "热寂"],
                'vn': ["攻击", "发现", "解决", "点击"],
                'v': ["吃饭", "退勤"]}

def get_random_word_list(p, num):
    # return [
    #     word_tuple[1][0] if (word_tuple := message_counter.get_random_words(
    #         p)) is not None else default_word[p][i]
    #     for i in range(num)
    # ]
    return [default_word[p][i] for i in range(num)]

# 地名
ns = get_random_word_list('ns', 2)
# 人名
nr = get_random_word_list('nr', 1)
# 普通名词
n = get_random_word_list('n', 4)
# 形容词
a = get_random_word_list('a', 4)
# 时间
t = get_random_word_list('t', 2)
# 名动词
vn = get_random_word_list('vn', 4)
# 动词
v = get_random_word_list('v', 2)

wum_name = "圣诞wum"
new_num = 3

# user name
name = "江之岛盾子"

time = t[0] + t[1]
last_time = "3小时0分25秒"

def main():
    for i in [-1, 0]:
        new_index = i
        story = f"一个{a[0]}的{time}，{a[3]}{nr[0]}给{name}打来电话，\n" \
            f"{name}豪爽的答应了：“我当然敢！”。周日下午在{ns[0]}举行，谁不来谁就是怂货。\n" \
            f"{name}原本以为{name}恐吓了{a[3]}{nr[0]}，{a[3]}{nr[0]}应该躲在{ns[1]}，不敢找{name}。\n" \
            f"可正当这时，{name}听见了{vn[0]}声，原来是{name}{n[0]}{vn[1]}了。\n" \
            f"一看，竟然是{wum_name}{vn[1]}的{n[0]}，他还真有{n[1]}\n" \
            f"{wum_name}也要和{name}举行{vn[0]}大战，于是{name}按照约定，到达了{ns[0]}，\n"
        if new_index == -1:
            story += f"{name}和{wum_name}势均力敌，平分秋色，比了{last_time}，也没分出胜负。"
        else:
            story += f"{name}{vn[2]}了{n[0]}，打的{wum_name}不敢还手，对{wum_name}的打击比{vn[3]}{n[2]}还大。"

        print(story)
        print()


if __name__ == "__main__":
    main()
