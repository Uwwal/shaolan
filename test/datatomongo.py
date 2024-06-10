import json
import os

import pymongo


def remove_extension(filename, extension=".json"):
    if filename.endswith(extension):
        return filename[:-len(extension)]
    return filename


def read_json_files_from_directory(directory_path):
    files_content = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    content = json.load(file)
                    files_content.append({
                        "id": remove_extension(filename),
                        "content": content
                    })
                except json.JSONDecodeError as e:
                    print(f"Error reading JSON file {file_path}: {e}")

    return files_content


def write_to_mongodb(documents):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["shaolan"]
    collection = db["catchwum"]

    # 插入多个文档
    if documents:
        collection.insert_many(documents)
        print("Documents inserted successfully.")
    else:
        print("No valid JSON documents to insert.")


def main():
    directory_path = "../data/catchwum/data"
    documents = read_json_files_from_directory(directory_path)
    write_to_mongodb(documents)
    # wum_inventory = WumInventory("3476365499")
    # a = wum_inventory.data["last_time"]
    # wum_inventory.catch_wum(save=True)
    # wum_inventory.save()
    # wum_inventory = WumInventory("3476365499")
    # wum_inventory.save()
    # b = wum_inventory.data["last_time"]
    # print(a,b)



if __name__ == "__main__":
    print(os.getcwd())
    main()
