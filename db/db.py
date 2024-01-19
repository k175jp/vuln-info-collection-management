from pymongo import MongoClient

class Error(Exception):
    pass

class MongoManager:
    def __init__(self, username, password):
        # self.client = MongoClient(f'mongodb://{username}:{password}@localhost:27017')
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['vuln']
    

    def set_collections(self, c):
        self.collections = self.db[c]

    def find(self, d):
        if not isinstance(d, dict):
            raise Error(f'only dict :{d}')
        return self.collections.find_one(d)
    
    def insert_data(self, d):
        self.collections.insert_one(d)
    
    def update_data(self, d1, d2):
        self.collections.update_one(d1, d2)
    
    def save(self, key, data):
        self.set_collections(key)
        for d in data:
            r = self.find({'cve_id': d.get("cve_id", "")})
            if not r:
                self.insert_data(d)
            else:
                self.update_data({'cve_id': d.get("cve_id", "")}, {'$set': d})
