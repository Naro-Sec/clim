from pymongo import MongoClient

db_url = "mongodb+srv://admin:admin@clim.bjojlvf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(db_url)
db = client["clim"]
collection = db["hu"]

collection.insert_one({"name": "test"})