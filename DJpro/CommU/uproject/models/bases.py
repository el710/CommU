"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import copy
import logging

from .skill import USkill

class EventBase():
    '''
        Operative base of events for user
    '''
    def __init__(self):
        self._base = []
    
    def __iter__(self):
        self.counter = 0
        return self
    
    def __next__(self):
        if self.counter < len(self._base):
            ind = self.counter
            self.counter += 1
            return self._base[ind]
                
        raise StopIteration() ## method 'for' will catch this exception


    def add_event(self, event:USkill, id_hash, parent=None):
        '''
            Create event 
        '''
        item = {"id": str(id_hash),
                "event": copy.deepcopy(event),
                'parent': parent
                }
        self._base.append(item)

    def read_event(self, id_hash):
        '''
            Find and return event
        '''
        for item in self._base:
            if item["id"] == str(id_hash):
                # logging.info(f"found : {item}\n")
                return item["event"]
        return None

    def edit_event(self, id_hash, event:USkill, newid_hash, parent=None):
        utem = self.read_event(id_hash)
        if utem:
            utem["id"] = str(newid_hash)
            utem["event"] = copy.deepcopy(event)
            utem["parent"] = parent if parent else None

    def del_event(self, id_hash):

        utem = self.read_event(id_hash)
        if utem:
            self._base.remove(utem)
        
        return None







