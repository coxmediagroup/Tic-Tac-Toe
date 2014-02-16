"""
class to store moves and results in mongodb and provide a dict-like interface
"""
import pymongo
import copy

mongoConfig = None#or make it {'host':serverAddress,'port':portNum}

class MoveCache:

    def __init__(self, collectionName='moveCache',config=mongoConfig):
        if config==None:
            self.client = pymongo.MongoClient()
        else:
            self.client = pymongo.MongoClient(config['host'], config['port'])
        self.database = self.client.moveCache
        self.collection = self.database[collectionName]
        self.collection.ensure_index('boardHash',unique=True)

    def __getitem__(self, boardHash):
        retrieved = self.collection.find_one({'boardHash': boardHash})
        if retrieved == None:
            raise KeyError(boardHash)
        else:
            return retrieved

    def get(self, boardHash, defaultVal):
        try:
            retVal = self.__getitem__(boardHash)
        except KeyError:
            retVal = defaultVal
        return retVal
       
    def __setitem__(self, boardHash, value):
        document = copy.deepcopy(value)
        document['boardHash'] = boardHash
        self.collection.update({'boardHash':boardHash},document,True)

    def clear(self):
        self.database.drop_collection(self.collection)
             
