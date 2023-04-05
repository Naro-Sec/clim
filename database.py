from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@hogeschoolutrecht.soh3npm.mongodb.net/?retryWrites=true&w=majority")
db = client.hogeschoolutrecht


class users:
    def __init__(self, collection):
        self.collection = collection

    def create(self, provider, naam, id, email, token, fqdn, time_creation_account, time_creation_record, time_update_record, time_deleted_record):
        data = {
            "provider": provider,
            "name": naam,
            "id": id,
            "email": email,
            "token": token,
            "fqdn": [fqdn],
            "time_creation_account": time_creation_account,
            "time_creation_record": time_creation_record,
            "time_update_record": time_update_record,
            "time_deleted_record": time_deleted_record
        }

        if self.collection.find({"token": token}):
            return "Appending user failed."

        return self.collection.insert_one(data).inserted_id

    def read_all(self):
        for x in self.collection.find({}):
            return x

    def read_id(self, id):
        return self.collection.find_one({"id": id})

    def read_token(self, name, token):
        return self.collection.find_one({"name": name, "token": token})

    def read_fqdn(self, id, fqdn):
        return self.collection.find_one({"id": id, "fqdn": fqdn})

    def update_fqdn(self, id, fqdn):
        return self.collection.update_one({ "id": id }, { "$addToSet": { "fqdn": fqdn }})

    def delete_fqdn(self, id, fqdn):
        return self.collection.update_one({ "id": id }, { "$pull": { "fqdn": fqdn }})

    def update_time_creation_record(self, id, new_date):
        return self.collection.update_one({ "id": id }, { "$set": { "time_creation_record": new_date }})

    def update_time_update_record(self, id, new_date):
        return self.collection.update_one({ "id": id }, { "$set": { "time_update_record": new_date }})

    def update_time_deleted_record(self, id, new_date):
        return self.collection.update_one({ "id": id }, { "$set": { "time_deleted_record": new_date }})

    def delete_one(self, id):
        return self.collection.delete_one({"id": id})

    def delete_all(self):
        return self.collection.delete_many({})

oauth = users(collection=db.users)