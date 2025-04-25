"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

import logging
import copy

from .bases import UtemBase

GUEST_USER = 'Guest'
class UUser():
    '''
        User's data
    '''
    def __init__(self, nickname):
        self.commu_id = hash(nickname) if nickname != GUEST_USER else None

        self.nickname = nickname
        self.password = None
        self.email = None

        self.firstname = None
        self.lastname = None
        self.language = 'en'

        self.geosocium = 'Earth'
        self.timezone = None
     

        '''
            Working context
        '''
        ## searching utem
        self.search = None

        ## pointer on template utem - to make new, to load, to watch parameters, to add to project, work on index page
        self.temp_utem = None 
      
         ## list of all user's contacts - phone book
        self.contacts = None


    def init_event_base(self, event_base:UtemBase):
        ## base of user's events (skill+time) single/from contracts/from projects
        self.events = event_base
        ## pointer to current skill from projects user is working with
        self.pro_event = None
    
    def init_contract_base(self, contract_base:UtemBase):
        self.contracts = contract_base
        ## pointer to current contract from projects user is working with
        self.pro_contract = None
    
    def init_project_base(self, project_base:UtemBase):
        self.projects = project_base
        ## pointer on current project user is working with - def as Life
        self.pro_project = None ## :UProject

    def add_project(self, project):
        if hasattr(self, "projects"):
            parent = self.pro_project.make_link() if self.pro_project else None
            self.pro_project = copy.deepcopy(project)
            self.projects.add(project, parent)
        


    def copy_workutem(self):
        return copy.deepcopy(self.temp_utem)
        
    def get_project_name(self):
        return self.projects[self.pro_project].name if self.pro_project != None else None 


    def save_event(self, event):
        logging.info(f'data: {event}\n')

        ## make copy of skill
        skill = self.copy_workutem()

        ## set executor & moment
        skill.set_event(self, event)
        # logging.info(f" {skill} : {self.temp_utem}")

        self.events.add(skill, self.pro_project.make_link())

        ## save event to plan as tuple
        try:
            self.pro_project.add_event(skill)
        except Exception as exc:
            logging.exception(f"add new event error {exc}")

        logging.info(f"Project skills: {self.pro_project.events} ")

        
class ClientUser(UUser):
    users = [] ## login + tokens

    def __init__(self):
        super().__init__()
        self.login = False ## is user login/logout

    def is_login(self):
        return self.login
    
    def log_in(self):
        self.login = True

    def log_out(self):
        self.login = False    


if __name__ == "__main__":

    user = UUser("test")
    print(vars(user))
    