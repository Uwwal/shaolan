import os

from PIL import Image


def main():
    cur_path = os.getcwd()
    cur_path = os.path.join(cur_path, "..")
    img_path = os.path.join(cur_path, "data\catchwum\wums\mope wum.png")

    img = Image.open(img_path)

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    alpha_channel = img.getchannel(3)

    alpha_channel = alpha_channel.point(lambda i: int(i * 0.4))

    Image.composite(img, Image.new('RGBA', img.size, (0, 0, 0, 0)), alpha_channel).show()


if __name__ == '__main__':
    main()