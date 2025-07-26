"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import logging
class UtemBase():
    '''
        RAMemory base of utems for user
    '''
    def __init__(self):
        self._base = []
        self.counter = 0

    
    def __iter__(self):
        self.counter = 0
        return self
    
    def __next__(self):
        if self.counter < len(self._base):
            ind = self.counter
            self.counter += 1
            return self._base[ind]
                
        raise StopIteration() ## method 'for' will catch this exception

    def len(self):
        return len(self._base)


    def add(self, utem):
        '''
            Create & save 
        '''
        if self.read(utem.token) == None:
            item = {"id": utem.token,
                    "type": utem.classname,
                    "utem": utem,
                    }
            self._base.append(item)

    def read(self, id_hash=None):
        '''
            Find and return
        '''
        if id_hash:
            for item in self._base:
                if item["id"] == id_hash:
                    return item["utem"]
        else:
            if self.len() > 0:
                return self._base[0]["utem"]
            
        return None

    def edit(self, id_hash, new_utem):
        for item in self._base:
            if item["id"] == id_hash:
                item["id"] = new_utem.token
                item["type"] = new_utem.classname
                item["utem"] = new_utem
                

    def delete(self, id_hash=None):
        """
            Delete id_hash item
        """
        for item in self._base:
            if item["id"] == id_hash:
                self._base.remove(item)
    
    
        




