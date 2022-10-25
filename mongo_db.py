import pymongo
import pymongo.errors

class MyMongoClient:
    def __init__(self,col):
        self.myclient = pymongo.MongoClient("127.0.0.1:27017")
        self.mydb = self.myclient['doubanmovie']
        self.mycol = self.mydb[col]

    def insert_one(self, item):
        try:
            self.mycol.insert_one(item)
        except pymongo.errors.WriteError as e:
            pass
        except Exception as e:
            print(e.__traceback__.tb_lineno,e)
    def insert_many(self, itemlist):
        self.mycol.insert_many(itemlist)

    def findall(self):
        return self.mycol.find({})

    def find(self,tags):
        return self.mycol.find({"tags":tags})

