# --- file: models/skill.py ---
from slugify import slugify
from models.base import UObject
from datetime import datetime

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

