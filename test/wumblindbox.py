import random

price_list = [5, 10]
delta_value_list = [lambda: random.uniform(-2.3, 0.1), lambda: random.uniform(-10, 7.7)]

def get_value(i):
    price = price_list[i]
    max_value = price + delta_value_list[i]()
    cur_price = 0
    while cur_price < max_value:
        cur_price += random.choice([0.0938, 0.2272, 1.178, 2.5001])
    return cur_price

def calculate_expectation():
    num_iterations = 100000

    for index in range(len(price_list)):
        values = []
        for _ in range(num_iterations):
            values.append(get_value(index))

        # 计算值的范围
        min_value = min(values)
        max_value = max(values)

        # 定义直方图的桶数量
        num_bins = 20

        # 计算每个桶的宽度
        bin_width = (max_value - min_value) / num_bins

        # 初始化直方图
        histogram = [0] * num_bins
        for value in values:
            index = int((value - min_value) / bin_width)
            if index == num_bins:  # 处理值为最大值的情况
                index -= 1
            histogram[index] += 1

        # 找到最大高度以缩放条形图
        max_height = max(histogram)
        scale_factor = 50.0 / max_height

        # 打印直方图
        print("Distribution of get_value() Results")
        for i in range(num_bins):
            bin_start = min_value + i * bin_width
            bin_end = bin_start + bin_width
            bar = '*' * int(histogram[i] * scale_factor)
            print(f"{bin_start:.2f} - {bin_end:.2f}: {bar}")

        sum = 0
        for i in values:
            sum += i
        print(sum/len(values))

if __name__ == '__main__':
    calculate_expectation()
    # for i in range(100):
    #     price = price_list[1]
    #     max_value = price + delta_value_list[1]()
    #     print(max_value)