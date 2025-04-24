"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

from slugify import slugify
from .uobject import UObject
from .skill import USkill

class UProject(UObject):
    """
        Class of user's projects stock
        There are here its deals where user is:
        - partner
        - customer
        - hired worker
        and lists of its:
            - partners
            - customers
            - hired workers
        in every project

        User can have many Projects, 
        but there are always default project - "Life" project
    """    
    def __init__(self, starter_user, project_name=None):
        super().__init__(project_name or f"{starter_user}'s project")
        self.target = "Project's point"
        ## 'Do not" laws
        self.project_laws = {"base": "CommU laws", }
        self.partners = [starter_user]
        self.customers = []
        self.workers = []
        self.subprojects = []
        self.contracts = []
        ## events = skill + time
        self.events = []

    def get_file_name(self):
        return f"{slugify(self.name)}.ptp"

    def add_skill(self, skill: USkill):
        time_moment = skill._event['start_time'] if skill._event else 'unknown-time'
        new_item = {"name": f"{time_moment} {skill.name}", "link": skill.make_link()}
        self.skills.append(new_item)
