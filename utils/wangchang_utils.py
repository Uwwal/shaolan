from config.constant import wangchang_img_arg_name_list, side_length_list, middle_point_list, multi_scale_list
from utils.angle_utils import rotate_point


# def get_wangchang_resize_side(angle, img_type='wum'):
#     a = math.radians(angle % 45 - 45)
#
#     i = wangchang_img_arg_name_list.index(img_type)
#     return side_length_list[i] * math.sqrt(2) * math.cos(a)


def get_image_face_middle_point(img_type='wum'):
    i = wangchang_img_arg_name_list.index(img_type)

    c = side_length_list[i]

    x, y = middle_point_list[i]

    x_2 = x + c / 2
    y_2 = y + c / 2

    return x_2, y_2


def get_rotate_point(angel, c, n_c, img_type='wum'):
    i = wangchang_img_arg_name_list.index(img_type)
    o_c = side_length_list[i]

    m_x, m_y = get_image_face_middle_point(img_type)
    m_x *= c / o_c
    m_y *= c / o_c

    r_x, r_y = rotate_point((c / 2, c / 2), (m_x, m_y), angel)

    # n_c = get_wangchang_resize_side(angel,img_type)
    o = (n_c - c) / 2

    x, y = r_x + o, r_y + o

    # print(r_x, r_y)
    # print(o)

    return x, y


def get_multi_scale(img_type='wum'):
    i = wangchang_img_arg_name_list.index(img_type)
    return multi_scale_list[i]

# def test(angle = 60):
#     img = Image.open("./plugins/bigwangchang/nielian2.png")
#
#     w,h = img.size
#
#     img_ = img.rotate(angle, expand=True)
#
#     draw = ImageDraw.Draw(img_)
#
#     x_,y_ = get_image_face_middle_point("捏脸")
#
#     x__,y__ = rotate_point((w/2,w/2),(x_,y_) ,angle)
#
#     radius = 10
#
#     w_new,h_new = img_.size
#     xoffset, yoffset = (w_new - w) / 2, (h_new - h) / 2
#
#     x, y = x__ + xoffset, y__ + yoffset
#
#     print(x__,y__)
#     print(xoffset,yoffset)
#
#     left_up_point = (x - radius, y - radius)
#     right_down_point = (x + radius, y + radius)
#
#     draw.ellipse([left_up_point, right_down_point], outline="black", width=3)
#
#     img_.show()
#
#
# test()
#
# def test(angle=60):
#     img = Image.open("./plugins/bigwangchang/nielian2.png")
#
#     img__ = img.resize((800,800))
#
#     img_ = img__.rotate(angle, expand=True)
#
#     draw = ImageDraw.Draw(img_)
#
#     x, y = get_rotate_point(angle, img__.size[0], img_.size[0], "捏脸")
#
#     radius = 10
#
#     left_up_point = (x - radius, y - radius)
#     right_down_point = (x + radius, y + radius)
#
#     draw.ellipse([left_up_point, right_down_point], outline="black", width=3)
#
#     img_.show()
#
#
# test()
