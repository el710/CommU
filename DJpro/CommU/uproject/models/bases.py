"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

try:
    from uobject import UObject
except:
    from .uobject import UObject

class UtemBase():
    '''
        Operative base of utems for user
    '''
    def __init__(self, storage=None):
        self._base = []
        self.counter = 0
        ## for load from
        self.storage = storage

    
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


    def add(self, utem:UObject):
        '''
            Create & save 
        '''
        if self.read(utem.get_token()) == None:
            item = {"id": utem.get_token(),
                    "type": utem.__class__.__name__,
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
                return self._base[0]
            
        return None

    def edit(self, id_hash, new_utem:UObject):
        for item in self._base:
            if item["id"] == id_hash:
                item["id"] = new_utem.get_token()
                item["utem"] = new_utem
                

    def delete(self, id_hash=None):
        """
            Delete id_hash item
        """
        for item in self._base:
            if item["id"] == id_hash:
                self._base.remove(item)
    
    
        




