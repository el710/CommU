"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

from abc import ABC, abstractmethod
from datetime import datetime
from slugify import slugify

import hashlib

from ..constants.constants import *

def get_hash(data: str):
    return hashlib.shake_128(data.encode()).hexdigest(13)

class Persistable(ABC):
    @abstractmethod
    def get_file_name(self, user:str=None) -> str: pass

    @abstractmethod
    def get_title(self) -> str: pass



class UObject(Persistable):
    def __init__(self, name: str=None):
        self.name = name
        self.author = None
        self._create_datetime = None
        self.geosocium = None
        self.public = False
        self._state = TEMPLATE_UTEM

    def set_attributes(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, datetime.fromisoformat(value) if key == "_create_datetime" else value)

    def get_name(self):
        return self.name
    
    def get_token(self):
        str = f"{self.name}:{self.author}:{self._create_datetime}:{self.geosocium}"
        return get_hash(str)

    def get_state(self):
        return self._state
    
    def get_classname(self):
        return f"{self.__class__.__name__}"

    def make_link(self):
        return f"/{self.__class__.__name__}/{self.get_token()}".lower()
    
    def get_file_name(self):
        return f"{self.get_token()}".lower()

    def to_dict(self):
        data = self.__dict__.copy()
        if isinstance(data.get("_create_datetime"), datetime):
            data["_create_datetime"] = data["_create_datetime"].isoformat()
        return data

    def from_dict(self, data: dict):
        self.set_attributes(**data)

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"
    
    def info(self):
        return f"{self} staff: {vars(self)}\n"
    
    def get_title(self):
        return super().get_title()
    

