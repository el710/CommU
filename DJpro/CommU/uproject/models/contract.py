"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

from slugify import slugify
from .uobject import UObject

class UContract(UObject):
    def __init__(self, name, customer_id=None, provider_id=None):
        super().__init__(name)
        self.description = None
        self.customer = customer_id
        self.provider = provider_id
        self.state = "template" ## "offer", "deal", "closed"
        self.eventchain = [] ## :  {event, customer, provider, dependence}
        self.history = []
    
    def get_file_name(self, user:str=None):
        return f"{super().get_file_name(user)}.ctp"
    
    def get_title(self, contragent:str):
        return f"{contragent if contragent else ''} {self.name}"