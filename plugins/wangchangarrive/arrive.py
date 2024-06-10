import gc
import math
from io import BytesIO

import cv2
import numpy as np
from PIL import Image

from utils.angle_utils import calculate_angle
from utils.image_utils import mirror_image, base64_to_message_segment
from utils.math_utils import intersection_with_vertical_line, find_symmetric_point
from utils.wangchang_utils import get_multi_scale, get_rotate_point

face_cascade_3 = cv2.CascadeClassifier('./plugins/wangchangarrive/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('./plugins/wangchangarrive/lbpcascade_animeface.xml')
# eye_cascade = cv2.CascadeClassifier('./plugins/wangchangarrive/haarcascade_eye.xml')
eye_cascade = cv2.CascadeClassifier('./plugins/wangchangarrive/anime-eyes-cascade.xml')


def true_eyes_detect(eyes, face):
    x, y, w, h = face
    mid_y = y + int(0.3 * h)

    eye_distances = []
    for (ex, ey, ew, eh) in eyes:
        eye_center_y = ey + eh // 2
        distance_to_mid = abs(eye_center_y - mid_y)
        eye_distances.append((distance_to_mid, (ex, ey, ew, eh)))

    eye_distances.sort(key=lambda x: x[0])
    true_eyes = [eye[1] for eye in eye_distances[:2]]

    return true_eyes


async def wangchang_arrive(image, p, img_type):
    numpy_image = np.array(image)

    cv2_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=30, minSize=(20, 20))

    faces_num = len(faces)

    if faces_num == 0:
        faces = face_cascade_3.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=30, minSize=(20, 20))
        faces_num = len(faces)
        if faces_num == 0:
            del cv2_image
            gc.collect()
            return None

    # image = image.resize((1080, int(image.size[1] * 1080 / image.size[0])), Image.Resampling.LANCZOS)

    f_wangchang = Image.open(p)
    for (x, y, w, h) in faces:
        face_region = gray[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(face_region)

        eyes_num = len(eyes)

        if eyes_num < 2:
            f_wangchang_resized = f_wangchang.resize((w, h), Image.Resampling.LANCZOS)

            paste_y = y
            if img_type == '捏脸':
                paste_y += int(h * 0.7)

            image.paste(f_wangchang_resized, (x, paste_y), f_wangchang_resized)
        else:
            if eyes_num > 2:
                eyes[0], eyes[1] = true_eyes_detect(eyes, (x, y, w, h))

            if eyes[0][0] < eyes[1][0]:
                left_eye = eyes[0]
                right_eye = eyes[1]
            else:
                left_eye = eyes[1]
                right_eye = eyes[0]
            # draw = ImageDraw.Draw(image)
            # draw.rectangle([x, y, x + w, y + h], outline="blue", width=2)

            # for (ex, ey, ew, eh) in eyes:
            #     draw.rectangle([x + ex, y + ey, x + ex + ew, y + ey + eh], outline="green", width=2)

            middle_point_left_eye_x = (left_eye[0] * 2 + left_eye[2]) / 2
            middle_point_left_eye_y = (left_eye[1] * 2 + left_eye[3]) / 2
            middle_point_right_eye_x = (right_eye[0] * 2 + right_eye[2]) / 2
            middle_point_right_eye_y = (right_eye[1] * 2 + right_eye[3]) / 2

            angle = calculate_angle(middle_point_left_eye_x, middle_point_left_eye_y, middle_point_right_eye_x,
                                    middle_point_right_eye_y)

            middle_point_x = (middle_point_left_eye_x + middle_point_right_eye_x) / 2 + x
            middle_point_y = (middle_point_left_eye_y + middle_point_right_eye_y) / 2 + y

            # draw.ellipse([(middle_point_x - 10, middle_point_y - 10), (middle_point_x + 10, middle_point_y + 10)],
            #              outline="black", width=3)

            f_wangchang_ = f_wangchang.resize((h, h), Image.Resampling.LANCZOS)

            f_wangchang_rotated = f_wangchang_.rotate(angle, expand=True)
            side = f_wangchang_rotated.size[0]

            wc_middle_point = get_rotate_point(angle, h, side, img_type)

            w_1 = int(w * get_multi_scale(img_type))
            h_1 = int(h * get_multi_scale(img_type))

            f_wangchang_resized = f_wangchang_rotated.resize((w_1, h_1), Image.Resampling.LANCZOS)
            wc_middle_point_resized = wc_middle_point[0] * w_1 / side, wc_middle_point[1] * h_1 / side

            nielian_delta_x = 0
            nielian_delta_y = 0
            if img_type == '捏脸':
                nielian_delta_x += int(math.sin(math.radians(angle)) * (x + w - middle_point_x) * 0.4)
                nielian_delta_y += int(math.cos(math.radians(angle)) * (y + h - middle_point_y) * 0.4)

            image.paste(f_wangchang_resized,
                        (round(middle_point_x - wc_middle_point_resized[0] + nielian_delta_x),
                         round(middle_point_y - wc_middle_point_resized[1] + nielian_delta_y)),
                        f_wangchang_resized)

            # draw.ellipse(
            #     [(round(middle_point_x - wc_middle_point[0]) - 10,
            #       round(middle_point_y - wc_middle_point[1]) - 10),
            #      (round(middle_point_x - wc_middle_point[0]) + 10,
            #       round(middle_point_y - wc_middle_point[1]) + 10)],
            #     outline="purple", width=4)
            #
            # draw.ellipse(
            #     [(round(middle_point_x - wc_middle_point[0]) + wc_middle_point[0] - 10,
            #       round(middle_point_y - wc_middle_point[1]) + wc_middle_point[1] - 10),
            #      (round(middle_point_x - wc_middle_point[0]) + wc_middle_point[0] + 10,
            #       round(middle_point_y - wc_middle_point[1]) + wc_middle_point[1] + 10)],
            #     outline="red", width=3)

    buf = BytesIO()
    image.save(buf, format='PNG')

    del cv2_image
    gc.collect()
    return await base64_to_message_segment(buf)


async def wangchang_arrive_mirror(image, reverse=False):
    # start_time = time.time()

    numpy_image = np.array(image)

    width, height = image.size

    # draw = ImageDraw.Draw(image)

    cv2_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=30, minSize=(20, 20))

    faces_num = len(faces)

    faces_middle_line_list = []

    if faces_num == 0:
        image = await mirror_image(image, reverse)

        buf = BytesIO()
        image.save(buf, format='PNG')

        del cv2_image
        gc.collect()
        return await base64_to_message_segment(buf)

    for (x, y, w, h) in faces:
        face_region = gray[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(face_region)

        eyes_num = len(eyes)

        if eyes_num < 2:
            faces_middle_line_list.append(((x + w // 2, 0), 90))
        else:
            if eyes_num > 2:
                eyes[0], eyes[1] = true_eyes_detect(eyes, (x, y, w, h))

            if eyes[0][0] < eyes[1][0]:
                left_eye = eyes[0]
                right_eye = eyes[1]
            else:
                left_eye = eyes[1]
                right_eye = eyes[0]

            middle_point_left_eye_x = (left_eye[0] * 2 + left_eye[2]) / 2
            middle_point_left_eye_y = (left_eye[1] * 2 + left_eye[3]) / 2
            middle_point_right_eye_x = (right_eye[0] * 2 + right_eye[2]) / 2
            middle_point_right_eye_y = (right_eye[1] * 2 + right_eye[3]) / 2

            angle = calculate_angle(middle_point_left_eye_x, middle_point_left_eye_y, middle_point_right_eye_x,
                                    middle_point_right_eye_y)

            middle_point_x = (middle_point_left_eye_x + middle_point_right_eye_x) / 2 + x
            middle_point_y = (middle_point_left_eye_y + middle_point_right_eye_y) / 2 + y

            faces_middle_line_list.append(((middle_point_x, middle_point_y), angle + 90))

    faces_middle_line_list.sort(key=lambda x: x[0][0])

    # for i in faces_middle_line_list:
    #     await draw_ray(image, i[0], i[1])

    for i in range(len(faces_middle_line_list)):
        cur = faces_middle_line_list[i]
        cur_x = cur[0][0]
        cur_y = cur[0][1]
        angle = cur[1]

        left_boundary = 0 if i == 0 else (faces_middle_line_list[i - 1][0][0] + faces_middle_line_list[i][0][0]) // 2
        right_boundary = width if i == len(faces_middle_line_list) - 1 else (faces_middle_line_list[i][0][0] +
                                                                             faces_middle_line_list[i + 1][0][0]) // 2

        # draw.rectangle([(left_boundary, 0), (right_boundary, height)], outline="red", width=2)

        start = intersection_with_vertical_line(cur_x, cur_y, angle, left_boundary)

        end = intersection_with_vertical_line(cur_x, cur_y, angle, right_boundary)

        # draw.line([start, end], fill="green", width=2)

        # draw.line([(cur_x,0), (cur_x,height)], fill="green", width=2)

        # draw.ellipse([(cur_x - 10, cur_y - 10), (cur_x + 10, cur_y + 10)], outline="purple", width=4)

        await paste_mirror(image, (width, height), (cur_x, cur_y), start[1], end[1], angle, reverse)

        # image.paste(copy_img_rotated, (cur_x, cur_y), mask)

    buf = BytesIO()
    image.save(buf, format='PNG')

    # end_time = time.time()

    # print(end_time - start_time)

    del cv2_image
    gc.collect()
    return await base64_to_message_segment(buf)


async def paste_mirror(image, image_size, line_point, start_x, end_x, angle, reverse=False):
    width, height = image_size
    x1, y1 = line_point

    k = math.tan(math.radians(angle))
    b = -(k * (0 - x1)) + y1

    for x in range(width):
        if x < start_x or x > end_x:
            continue

        y_intersection = intersection_with_vertical_line(x1, y1, angle, x)
        for y in range(height):
            if not reverse:
                if not y_intersection[0] and y < y_intersection[2]:
                    tar_x, tar_y = find_symmetric_point(k, b, x, y)

                    if tar_x < start_x or tar_y < 0 or tar_x >= end_x or tar_y >= height:
                        continue

                    pixel_value = image.getpixel((x, y))

                    image.putpixel((tar_x, tar_y), pixel_value)
                elif y_intersection[0] and y_intersection[2] == 0 and x < x1:
                    tar_x = 2 * x1 - x
                    tar_y = y

                    if tar_x < start_x or tar_y < 0 or tar_x >= end_x or tar_y >= height:
                        continue

                    pixel_value = image.getpixel((x, y))

                    image.putpixel((tar_x, tar_y), pixel_value)
            elif reverse:
                if not y_intersection[0] and y > y_intersection[2]:
                    tar_x, tar_y = find_symmetric_point(k, b, x, y)

                    if tar_x < start_x or tar_y < 0 or tar_x >= end_x or tar_y >= height:
                        continue

                    pixel_value = image.getpixel((x, y))

                    image.putpixel((tar_x, tar_y), pixel_value)
                if y_intersection[0] and y_intersection[2] == 0 and x > x1:
                    tar_x = 2 * x1 - x
                    tar_y = y

                    if tar_x < start_x or tar_y < 0 or tar_x >= end_x or tar_y >= height:
                        continue

                    pixel_value = image.getpixel((x, y))

                    image.putpixel((tar_x, tar_y), pixel_value)
