from bson import ObjectId

from config.global_object import steal_history_collection


async def insert_steal_wum_new_record(record):
    return steal_history_collection.insert_one(record).inserted_id


async def query_steal_wum_record(record_id):
    r_id = ObjectId(record_id)

    record = steal_history_collection.find_one({"_id": r_id})

    return record
