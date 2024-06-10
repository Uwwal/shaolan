import os

from models.wum_inventory import WumInventory


def get_all_filenames(directory):
    try:
        # 获取文件夹下的所有文件和文件夹的名称
        entries = os.listdir(directory)

        # 过滤掉文件夹，只保留文件
        files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]

        return files
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def remove_extension(filename, extension=".json"):
    if filename.endswith(extension):
        return filename[:-len(extension)]
    return filename

def check_wum_data():
    files = get_all_filenames('./data/catchwum/data')

    for file in files:
        print(file)
        w = WumInventory(remove_extension(file))

check_wum_data()
