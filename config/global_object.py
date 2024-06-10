import os

import pymongo

from config.constant import wums_dir, wum_rarity_num
from models.ftwc_config import FTWCConfig
from models.message_counter import MessageCounter
from models.wum import Wum
from utils.docs_utils import extract_docstrings

ftwc_config = FTWCConfig()

message_counter = MessageCounter()

docs_list = extract_docstrings()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["shaolan"]
catchwum_collection = db["catchwum"]
steal_history_collection = db["steal_history"]

wum_png_list = [f for f in os.listdir(wums_dir) if os.path.isfile(os.path.join(wums_dir, f))]
global_wum_dict = {wum.name: wum for wum in (Wum(f) for f in wum_png_list)}
global_wum_name_list = list(global_wum_dict.keys())

wum_rarity_dict_list = {f + 1: [] for f in range(wum_rarity_num)}
for wum_ in global_wum_dict.values():
    wum_rarity_dict_list[wum_.rarity].append(wum_)

print("LOG::INIT\t\tGLOBAL OBJECT INIT DONE")
