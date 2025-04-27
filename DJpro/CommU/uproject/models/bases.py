"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import copy
import logging

try:
    from uobject import UObject
except:
    from .uobject import UObject

class UtemBase():
    '''
        Operative base of events for user
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


    def add(self, utem:UObject, parent_id=None):
        '''
            Create & save 
        '''
        item = {"id": utem.get_token(),
                "utem": utem,
                'parent': parent_id
                }
        self._base.append(item)

    def read(self, id_hash):
        '''
            Find and return
        '''
        for item in self._base:
            if item["id"] == id_hash:
                # logging.info(f"found : {item}\n")
                return item["utem"]
        return None

    def edit(self, id_hash, new_utem:UObject, parent_id=None):
        for item in self._base:
            if item["id"] == id_hash:
                item["id"] = new_utem.get_token()
                item["utem"] = new_utem
                if parent_id:  item["parent"] = parent_id

    def delete(self, id_hash=None, parent_id=None): ## !!! recursive
        if id_hash or parent_id:
            for item in self._base:
                if item["id"] == id_hash or item["parent"] == parent_id:
                    next = item["id"]
                    self.delete(self, parent_id=next)
                    self._base.remove(item)
        return None


if __name__ == "__main__":

    from skill import USkill

    '''
        Using annotation
    '''
    base = UtemBase()
    event_1 = USkill("test 1")
    event_2 = USkill("test 2")
    event_3 = USkill("test 3")
    
    base.add(event_1)
    base.add(event_2, event_1.get_token())
    base.add(event_3)

    print(f"Take first: {base.__next__()}\n")  

    for item in base: print(f"{item} - {item['utem']}")


    ev = base.read(event_2.get_token())
    print(f"\n get item: {ev.info()}")
    
    hash = event_2.get_token()
    new_attr = {"name": "new name"}
    event_2.set_attributes(**new_attr) 
    base.edit(hash, event_2)
    print("\n change:")
    for item in base: print(f"{item} - {item['utem']}")


    base.delete(event_1.get_token())
    print("\n delete recursive: event_1")
    for item in base: print(f"{item} - {item['utem']}")




