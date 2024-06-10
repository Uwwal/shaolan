import json
import os
import random

import jieba
import jieba.analyse
import jieba.posseg

from config.constant import cur_path
from utils.string_utls import check_standard_word


class MessageCounter:
    def __init__(self):
        self.sorted_word_counts = {'ns': [], 'n': [], 'vn': [], 'v': [], 'f': [],
                                   't': [], 'nr': [], 'nt': [], 'nw': [],
                                   'nz': [], 'a': [], 'ad': [], 'an': [],
                                   'd': [], 'm': [], 'r': [], 'p': [], 'c': []}
        self.file_path = os.path.join(cur_path, 'data','iupar','iupar_json')
        self.counter = 0
        self.save_counter = 0
        self.word_stack = []
        self.word_dicts = {
            'ns': {},  # 地名
            'n': {},  # 普通名词
            'vn': {},  # 名动词
            'v': {},  # 动词
            'f': {},  # 方位名词
            't': {},  # 时间
            'nr': {},  # 人名
            'nt': {},  # 机构名
            'nw': {},  # 作品名
            'nz': {},  # 其他专名
            'a': {},  # 形容词
            'ad': {},  # 副形词
            'an': {},  # 名形词
            'd': {},  # 副词
            'm': {},  # 数量词
            'r': {},  # 代词
            'p': {},  # 介词
            'c': {},  # 连词
        }
        self.p_list = [
            'ns', 'n', 'vn', 'v', 'f',
            't', 'nr', 'nt', 'nw',
            'nz', 'a', 'ad', 'an',
            'd', 'm', 'r', 'p', 'c'
        ]
        self.popped_word = []
        self.load()

    def process_message(self, message):
        while self.counter > 3000:
            self.counter -= 1
            word_counts = self.word_stack.pop(0)
            for word, weight in word_counts:
                pos = jieba.posseg.lcut(word)[0].flag
                if pos in self.word_dicts and word in self.word_dicts[pos]:
                    self.word_dicts[pos][word] -= weight
                    if self.word_dicts[pos][word] <= 0:
                        del self.word_dicts[pos][word]

        word_counts = jieba.analyse.extract_tags(message, topK=20, withWeight=True,
                                                 allowPOS=('ns', 'n', 'vn', 'v', 'f',
                                                           't', 'nr', 'nt', 'nw',
                                                           'nz', 'a', 'ad', 'an',
                                                           'd', 'm', 'r', 'p', 'c'))

        # print("LOG::IUPAR\t\t本条消息获得以下内容:\n\t\t", end="")
        # for t in word_counts:
        #     print(t[0] + " - " + str(t[1]) + "\t", end="")
        # print("")

        if word_counts == [] or word_counts is None:
            return

        message_len = len(message)
        if message_len < 20:
            weight_multiple = self.get_short_message_weight_multiple(message_len)
        else:
            weight_multiple = 1

        word_count_save_list = []

        for word, weight in word_counts:
            if not check_standard_word(word):
                continue

            weight *= weight_multiple

            if weight > 1:
                weight = 1

            pos = jieba.posseg.lcut(word)[0].flag

            if pos in self.word_dicts:
                if word in self.word_dicts[pos]:
                    self.word_dicts[pos][word] += weight
                else:
                    self.word_dicts[pos][word] = weight

            word_count_save_list.append((word, weight))

        if word_count_save_list is None or word_count_save_list == []:
            return

        self.word_stack.append(word_count_save_list)

        self.counter += 1
        self.save_counter += 1

        sorted_word_counts = {}
        for pos, word_dict in self.word_dicts.items():
            sorted_word_counts[pos] = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)

        self.sorted_word_counts = sorted_word_counts
        # print(sorted_word_counts)

        if self.save_counter % 10 == 0:
            self.save_counter = 0
            self.save()

    def get_random_words(self, p):
        if p in self.sorted_word_counts:
            dict_len = len(self.sorted_word_counts[p])

            if not dict_len == 0:
                r = random.randint(0, int(2 * dict_len / 3))

                tuple_w = self.sorted_word_counts[p].pop(r)
                self.popped_word.append([p, tuple_w])
                return r, tuple_w
        return None

    def iupar_message(self, message, is_command=False):
        pair_list = jieba.posseg.lcut(message)

        keys = self.sorted_word_counts.keys()

        result = ""

        sorted_word_len_dict = {}
        for k, v in self.sorted_word_counts.items():
            sorted_word_len_dict[k] = len(v)

        for w, p in pair_list:
            r = random.randint(0, 30)

            if p in keys and r > 10 + 20 * self.iupar_check_len_num_success_p(sorted_word_len_dict[p]):
                random_tuple = self.get_random_words(p)
                if random_tuple is not None:
                    sorted_word_len_dict[p] -= 1

                    random_words = random_tuple[1][0]
                    result += random_words
                else:
                    result += w
            elif r == 9 or r == 10:
                rand_p = self.p_list[random.randint(0, len(self.p_list) - 1)]
                random_tuple = self.get_random_words(rand_p)
                if random_tuple is not None:
                    sorted_word_len_dict[rand_p] -= 1

                    random_words = random_tuple[1][0]
                    result += random_words
            else:
                result += w

        self.re_add_popped_word()

        if result == message:
            if is_command:
                print("sdvx waao")
                return self.iupar_message(message)
            return None

        return result

    def iupar_check_len_num_success_p(self, number):
        if number > 10:
            return 0
        elif 1 <= number <= 5:
            return 60 - (number - 1) * 5
        elif 6 <= number <= 10:
            return 20 - (number - 6) * 5
        elif number <= 0:
            # 30, randInt:[0,30], ->""
            return 100

    def save(self):
        data = {
            'sorted_word_counts': self.sorted_word_counts,
            'counter': self.counter,
            'word_stack': self.word_stack,
            'word_dicts': self.word_dicts
        }
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    def load(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.sorted_word_counts = data.get('sorted_word_counts', {})
                self.counter = data.get('counter', 0)
                self.word_stack = data.get('word_stack', [])
                self.word_dicts = data.get('word_dicts', {})

                self.save_counter = self.counter % 10
        except FileNotFoundError:
            print("IUPAR load error")

    def get_short_message_weight_multiple(self, message_len):
        return 1 / 400 * message_len ** 2

    def delete_word(self, word):
        for p, l in self.word_dicts.items():
            if word in l:
                del self.word_dicts[p][word]

                self.sorted_word_counts[p] = sorted(self.word_dicts[p].items(), key=lambda x: x[1], reverse=True)

                self.save()
                return "大概忘却了"
        return "果然还是无法忘记"

    def re_add_popped_word(self):
        for i in self.popped_word:
            self.sorted_word_counts[i[0]].append(i[1])
        self.popped_word = []
