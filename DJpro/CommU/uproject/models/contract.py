"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

from slugify import slugify
from .uobject import UObject

class UContract(UObject):
    def __init__(self, name, holder_id=None, dealer_id=None):
        super().__init__(name)
        self.description = None
        self.holder_id = holder_id
        self.dealer_id = dealer_id
        self.status = "template" ## "offer", "deal", "closed"
        
        ## networkx - graph for dependence ???
        self.holder_credit_events = [] ## :  {event, dependence}
        self.holder_debet_events = [] ## :  {event, dependence}

        self.history = []
    
    def get_file_name(self, user:str=None):
        return f"{super().get_file_name(user)}.ctp"
    
    def get_title(self, dealer:str):
        return f"{dealer if dealer else 'contract'} '{self.name}'"