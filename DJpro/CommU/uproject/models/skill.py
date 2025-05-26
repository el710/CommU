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
        self.resources = resources
        self.goal = goal
        self._event = None
        self._duration = None

    def get_file_name(self):
        return f"{super().get_file_name()}.stp"

    def get_slug_name(self):
        return slugify(self.name)

    def sign(self, author, geosocium=None, public=False):
        self.author = author
        self.geosocium = geosocium
        self.public = public
        self._create_datetime = datetime.now()

    def set_event(self, event):
        self._event = event
    
    def set_executor(self, user):
        self._executor = user
        

    def get_title(self):
        time_moment = self._event['start_time'] if self._event else 'in plan'
        return f"{time_moment} '{self.name}'"

