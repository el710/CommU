"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

from slugify import slugify
from .uobject import UObject
from .skill import USkill
from .contract import UContract

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
        but there is always main default project - "Life" project
    """    
    def __init__(self, starter_user_id, project_name=None, state:str="template"):
        super().__init__(project_name or f"{starter_user}'s project")

        self._state = state
        self.target = "Project's point"
        ## 'Do not" laws
        self.project_laws = {"base": "CommU laws"}
        self.partners = [starter_user_id]

        self.projects = [] ## list of ids
        self.contracts = []

        ## list of links to events(skill + time)
        self.events = []

    def get_file_name(self):
        return f"{super().get_file_name()}.ptp"
        
    def get_title(self):
        return f"project '{self.name}'"

    def add_event(self, skill_id:str):
        self.events.append(skill_id)

    def add_contract(self, contract_id:str):
        self.contracts.append(contract_id)

    def add_project(self, project_id:str):
        self.projects.append(project_id)