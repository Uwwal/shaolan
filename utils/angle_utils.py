import math


def calculate_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y1 - y2

    angle_rad = math.atan2(dy, dx)

    angle_deg = math.degrees(angle_rad)

    return angle_deg


def rotate_point(origin, pt, angle):
    x, y = pt
    offset_x, offset_y = origin
    radians = math.radians(angle)

    adjusted_x = x - offset_x
    adjusted_y = y - offset_y

    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)

    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y

    return qx, qy
