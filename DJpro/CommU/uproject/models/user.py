"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

import logging
import copy

from .bases import EventBase

GUEST_USER = 'Guest'
class UUser():
    '''
        User's data
    '''
    def __init__(self, nickname):
        self.commu_id = None
        self.nickname = nickname
        self.password = None
        self.email = None

        self.firstname = None
        self.lastname = None
        self.language = 'en'

        self.geosocium = 'Earth'
        self.timezone = None

        ## list of all user's contacts - phone book
        self.contacts = None

        ## list of all user's projects
        self.projects = None

        '''
            Working context
        '''
        ## pointer on template utem - to make new, to load, to watch parameters, to add to project, work on index page
        self.temp_utem = None 

        ## base of all user's events = skill+time
        self.events = None ## EventBase()
        ## pointer to current skill from projects user is working with
        self.pro_event = None        

        

        ## pointer on current project user is working with - def as Life
        self.pro_project = None

        ## pointer to current contract from projects user is working with
        self.pro_contract = None
        
        ## searching utems
        self.search = None

    def add_eventbase(self, event_base:EventBase):
        self.events = event_base
                

    def add_project(self, project):
        if self.projects == None:
            self.projects = [project]
        else:
            self.projects.append(project)
        self.pro_project = len(self.projects) - 1


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

        self.events.add_event(skill, skill.get_token(), self.projects[self.pro_project])

        current_project = self.projects[self.pro_project]
        # logging.info(f" {current_project} : {type(current_project)}")

        ## save event to plan as tuple
        try:
            current_project.add_skill(skill)
        except Exception as exc:
            logging.exception(f"add new event error {exc}")

        logging.info(f"Project skills: {current_project.events} ")

        
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
    