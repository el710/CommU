"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

from slugify import slugify
from .uobject import UObject
from .skill import USkill
from .contract import UContract
from ..constants.constants import *

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
    def __init__(self, name=None, starter_user_id=None, state:str=TEMPLATE_UTEM, my_token:str=None):
        
        if not name:
            name = "New Project"
        super().__init__(name)

        if starter_user_id:
            self.partners = [starter_user_id]
        else:
            self.partners = []

        self._state = state
        ## constant token = user_id
        self.hard_token = my_token

        self.target = "Project's point"
        ## 'Do not" laws
        self.project_laws = {"base": "CommU laws"}
        
        self.projects = [] ## list of ids
        self.contracts = []

        ## list of links to events(skill + time)
        self.events = []

    @property
    def token(self):
        if self.hard_token: return self.hard_token
        else:
            return super().token

    @property     
    def title(self):
        return f"project '{self.name}'"
    
    @property
    def file_name(self):
        return f"{super().file_name}.ptp"

    def add_event(self, skill_id:str):
        self.events.append(skill_id)

    def add_contract(self, contract_id:str):
        self.contracts.append(contract_id)

    def add_project(self, project_id:str):
        self.projects.append(project_id)