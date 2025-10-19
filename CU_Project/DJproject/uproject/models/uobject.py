"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

from abc import ABC, abstractmethod
from datetime import datetime

import hashlib

from ..constants.constants import *

def get_hash(data: str):
    return hashlib.shake_128(data.encode()).hexdigest(13)

class Persistable(ABC):
    @abstractmethod
    def file_name(self) -> str: pass

    @abstractmethod
    def title(self) -> str: pass

    def sign(self, user) -> None: pass


class UObject(Persistable):
    def __init__(self, name: str=None):
        self.s_name = name
        self.public = False
        
        self.author = None
        self.geosocium = None
        
        ## private
        self._create_datetime = None        
        self._state = TEMPLATE_UTEM
        self._parent = None


    @property
    def name(self):
        return self.s_name
    
    @name.setter
    def name(self, name):
        self.s_name = name


    '''
        For public utems
    '''
    def sign(self, author_id, geosocium=None):
        self.author = author_id
        self.geosocium = geosocium
        self._create_datetime = datetime.now()

    def is_signed(self):
        if self.author and self.geosocium and self._create_datetime: return True
        return False

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        self._state = state

    @property
    def parent(self):
        return self._parent

    @parent.setter   
    def parent(self, parent_id):
        self._parent = parent_id

    def set_attributes(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, datetime.fromisoformat(value) if key == "_create_datetime" else value)
                try:
                    setattr(self, key, int(value) if key == "amount" else value)
                except:
                    setattr(self, key, 0)

    @property
    def token(self):
        str = f"{self.name}:{self.author}:{self._create_datetime}:{self.geosocium}"
        return f"{get_hash(str)}".lower()
    
    @property
    def classname(self):
        return f"{self.__class__.__name__}"

    @property
    def link(self):
        return f"/{self.classname}/{self.token}".lower()
    
    @property
    def file_name(self):
        return f"{self.token}".lower()

    def to_dict(self):
        data = self.__dict__.copy()
        if isinstance(data.get("_create_datetime"), datetime):
            data["_create_datetime"] = data["_create_datetime"].isoformat()
        if hasattr(self, "amount"):
            if not isinstance(data.get("amount"), str):
                data["amount"] = str(data["amount"])
        return data

    def from_dict(self, data: dict):
        self.set_attributes(**data)

    def __str__(self):
        return f"{self.classname}({self.name})"
    
    @property
    def info(self):
        return f"{self} staff: {vars(self)}\n"
    


    
    