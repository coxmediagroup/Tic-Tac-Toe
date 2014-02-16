"""
class to store moves and results in mongodb and provide a dict-like interface
"""
import pymongo
import copy

mongoConfig = None#or make it {'host':serverAddress,'port':portNum}

class MoveCache:
    """
    provides dict-like interface to mongodb moveCache
    moveCache is indexed by boardhash, so looking up moves should be fast
    you can think of it as a dictionary like:
        {<boardHash1>:<moveVals>, <boardHash2>:<moveVals> ...}
    edit mongoConfig variable in this file to reflect local mongodb configuration,
    or set it to None to just create the client with pymongo's defaults.
    A config object may also be passed in to __init__ rather than editing this file
    """


    def __init__(self, collectionName='moveCache',config=mongoConfig):
        """
        collectionName is the name of the collection to use (useful for not clobbering it in testing)
        config is either a dict like {'host':serverAddress,'port':serverPort} specifying mongodb settings,
        or None, in which case MongoClient is created using pymongo defaults
        """
        if config==None:
            self.client = pymongo.MongoClient()
        else:
            self.client = pymongo.MongoClient(config['host'], config['port'])
        self.database = self.client.moveCache
        self.collection = self.database[collectionName]
        self.collection.ensure_index('boardHash',unique=True)

    def __getitem__(self, boardHash):
        """
        gets item with boardHash, throws KeyError if it doesn't exist
        """
        retrieved = self.collection.find_one({'boardHash': boardHash})
        if retrieved == None:
            raise KeyError(boardHash)
        else:
            return retrieved

    def get(self, boardHash, defaultVal=None):
        """
        same as dict.get - return value if it exists, otherwise return defaultVal
        """
        try:
            retVal = self.__getitem__(boardHash)
        except KeyError:
            retVal = defaultVal
        return retVal
       
    def __setitem__(self, boardHash, value):
        """
        will insert or update, depending on whether boardHash already exists
        """
        document = copy.deepcopy(value)
        document['boardHash'] = boardHash
        self.collection.update({'boardHash':boardHash},document,True)

    def clear(self):
        self.database.drop_collection(self.collection)
             
