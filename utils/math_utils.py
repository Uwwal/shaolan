import math

def intersection_with_vertical_line(x1, y1, a, k):
    if a % 90 == 0:
        return True, int(k), 0

    m = math.tan(math.radians(a))

    y_intersection = -(m * (k - x1)) + y1

    return False, int(k), int(y_intersection)


def find_symmetric_point(k, b, x1, y1):
    k = -k

    x_f = (x1 + k * (y1 - b)) / (1 + k * k)
    y_f = (k * (x1 + k * (y1 - b))) / (1 + k * k) + b

    x2 = 2 * x_f - x1
    y2 = 2 * y_f - y1

    return int(x2), int(y2)

