import pymongo

from models.wum_inventory import WumInventory

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["shaolan"]
collection = db["catchwum"]

def main():
    wum_inventory = WumInventory("3476365499")

    wum_inventory.delete_wum("wum守", 3)
    wum_inventory.delete_wum("wum什戴尔", 1)


if __name__ == "__main__":
    main()
