"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

import logging
from slugify import slugify
from datetime import datetime

try:
    from uobject import UObject
except:
    from .uobject import UObject

class USkill(UObject):
    """
        A simple skill that depends only on one person.
        The person do it by itself
    """    
    def __init__(self, name:str=None, description=None, resources=None, goal=None):
        super().__init__(name)
        self.description = description
        self.amount = 0
        self.event = None

    @property  
    def file_name(self):
        return f"{super().file_name()}.stp"

    @property
    def slug_name(self):
        return slugify(self.name)

    @property
    def event(self):
        return self.event
    
    def set_event(self, event):
        self.event = event   
    
    def set_executor(self, user):
        self._executor = user.commu_id
        
    @property
    def title(self):
        time_moment = self.get_event()['start_time'] if self.get_event() else 'in plan'
        return f"{time_moment} '{self.name}'"

