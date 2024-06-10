import math
import random


class SpriteContinuous:
    class Sprite:
        def __init__(self, position, angle):
            self.x, self.y = position
            self.angle = angle

        def calculate_next_angle(self):
            self.angle += random.randint(-10, 10)

        def move(self, width, height, cur_move_x, cur_move_y):
            radius = math.radians(self.angle)

            self.x -= math.sin(radius) * cur_move_x
            self.y += math.cos(radius) * cur_move_y

            if self.x > width:
                self.x -= width
            elif self.x < 0:
                self.x += width

            if self.y > height:
                self.y -= height
            elif self.y < 0:
                self.y += height

    def __init__(self, bg_size):
        self.sprite_list = []
        self.width, self.height = bg_size

    def get_sprite(self, index, p_size):
        sprite = self.sprite_list[index]
        sprite.calculate_next_angle()

        move_x_length = int(max(self.width / 15, p_size[0] / 2))
        move_y_length = int(max(self.height / 15, p_size[1] / 2))

        cur_move_x = random.randint(int(move_x_length / 2), move_x_length)
        cur_move_y = random.randint(int(move_y_length / 2), move_y_length)

        sprite.move(self.width, self.height, cur_move_x, cur_move_y)
        return (int(sprite.x), int(sprite.y)), sprite.angle

    def append_sprite(self, position, angle):
        self.sprite_list.append(SpriteContinuous.Sprite(position, angle))
