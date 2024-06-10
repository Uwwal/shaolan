import random

init_start = [(305, 350), (475, 395)]
init_end = [(245, 92), (570, 230)]


class WumContinuous:
    class Children:
        def __init__(self, gif_len):
            self.pos_list = []
            start = (random.randint(init_start[0][0], init_start[1][0]),
                     random.randint(init_start[0][1], init_start[1][1]))
            end = (random.randint(init_end[0][0], init_end[1][0]),
                   random.randint(init_end[0][1], init_end[1][1]))

            self.pos_list.append(start)

            sum_weight = 1
            t = 1
            for _ in range(gif_len - 2):
                sum_weight += t
                t *= 2

            delta = (end[0] - start[0], end[1] - start[1])
            t = 1
            for _ in range(gif_len - 2):
                weight = t / sum_weight
                self.pos_list.append((int(start[0] + delta[0] * weight), int(start[1] + delta[1] * weight)))
                t *= 2

            self.pos_list.append(end)

            self.angle_list = []

            self.angle_list.append(random.randint(-359, 359))

            acc_angle = random.randint(-20, 20)

            for i in range(gif_len):
                if i == 0:
                    continue

                self.angle_list.append(self.angle_list[i-1] + acc_angle)

        def get(self, index):
            return self.pos_list[index], self.angle_list[index]

    def __init__(self, num, gif_len):
        self.children_list = []

        for _ in range(num):
            self.children_list.append(WumContinuous.Children(gif_len))

    def get(self, wum_index, gif_index):
        return self.children_list[wum_index].get(gif_index)
