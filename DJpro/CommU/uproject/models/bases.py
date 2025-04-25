"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import copy
import logging

try:
    from skill import USkill
    from uobject import UObject
except:
    from .skill import USkill
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


    def add(self, utem:UObject, parent=None):
        '''
            Create & save 
        '''
        item = {"id": utem.get_token(),
                "value": copy.deepcopy(utem),
                'parent': parent
                }
        self._base.append(item)

    def read(self, id_hash):
        '''
            Find and return
        '''
        for item in self._base:
            if item["id"] == id_hash:
                # logging.info(f"found : {item}\n")
                return item["value"]
        return None

    def edit(self, id_hash, new_utem:UObject, parent=None):
        for item in self._base:
            if item["id"] == id_hash:
                item["id"] = new_utem.get_token()
                item["value"] = copy.deepcopy(new_utem)
                item["parent"] = parent if parent else None

    def delete(self, id_hash=None, link=None): ## !!! recursive
        if id_hash or link:
            for item in self._base:
                if item["id"] == id_hash or item["parent"] == link:
                    link = item["value"].make_link()
                    self.delete(self, link=link)
                    self._base.remove(item)
        return None


if __name__ == "__main__":
    '''
        Using annotation
    '''
    base = UtemBase()
    event_1 = USkill("test 1")
    event_2 = USkill("test 2")
    event_3 = USkill("test 3")
    
    base.add(event_1)
    base.add(event_2, event_1.make_link())
    base.add(event_3)
    print(f"{base.__next__()}")    

    ev = base.read(event_2.get_token())
    print(f" get item info: {ev.info()}\n")

    hash = ev.get_token()
    new_attr = {"name": "new name"}
    ev.set_attributes(**new_attr) 
    base.edit(hash, ev, event_1.make_link())
    ev = base.read(ev.get_token())
    print(f" get item info: {ev.info()}")    

    base.delete (event_1.get_token())

    for item in base: print(f"{item} - {item['value']}")




