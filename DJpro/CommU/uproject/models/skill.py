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
    def __init__(self, name, description=None, resources=None, goal=None):
        super().__init__(name)
        self.description = description
        self.resources = resources
        self.goal = goal
        self._event = None
        self._duration = None
        self._state = "template"

    def get_file_name(self):
        # logging.info(f"Skill name: {self.name}")
        return f"{slugify(self.name)}.stp"

    def get_slug_name(self):
        return slugify(self.name)

    def sign(self, author, geosocium=None, public=False):
        self.author = author
        self.geosocium = geosocium
        self.public = public
        self.create_datetime = datetime.now()

    def set_event(self, user, event):
        self.executor = user
        self._event = event

