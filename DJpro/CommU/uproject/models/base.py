# --- file: models/base.py ---
from abc import ABC, abstractmethod
from datetime import datetime
from slugify import slugify


class Persistable(ABC):
    @abstractmethod
    def to_dict(self): pass

    @abstractmethod
    def from_dict(self, data: dict): pass

    @abstractmethod
    def get_file_name(self) -> str: pass


class UObject(Persistable):
    def __init__(self, name: str):
        self.name = name
        self.author = None
        self.create_datetime = None
        self.geosocium = None
        self.public = False

    def set_attributes(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, datetime.fromisoformat(value) if key == "create_datetime" else value)

    def get_token(self):
        return hash(f"{self.name}:{self.author}:{self.create_datetime}:{self.geosocium}")

    def make_link(self):
        return f"{slugify(self.name)}:{self.get_token()}"

    def to_dict(self):
        data = self.__dict__.copy()
        if isinstance(data.get("create_datetime"), datetime):
            data["create_datetime"] = data["create_datetime"].isoformat()
        return data

    def from_dict(self, data: dict):
        self.set_attributes(**data)

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"
