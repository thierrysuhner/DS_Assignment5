from pysyncobj import SyncObj, SyncObjConf, replicated

class KVStorage(SyncObj):
    def __init__(self, selfAddress, partnerAddrs):
        conf = SyncObjConf()
        super(KVStorage, self).__init__(selfAddress, partnerAddrs, conf)
        self.__data = {}

    @replicated
    def put(self, key, value):
        print("put key: ", key, " with value: ", value)
        #Put operation, that sets the value of the key to be the provided value.
        if key is None:
            return
        self.__data[key] = list(value)

            
    @replicated        
    def append(self, key, value):
        print("append key: ", key, " with value: ", value)
        #Append operation, that adds the provided value to the value of the key.
        if key not in self.__data or self.__data[key] is None:
            self.__data[key] = list(value)
        else:
            self.__data[key].append(value)


    def get(self, key):
        print("get key: ", key)
        #Get operation, that retrieves the value of the provided key.
        return self.__data.get(key)


    def get_dumpfile(self):
        return self.dumpFile
