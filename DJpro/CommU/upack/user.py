"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

import logging
import copy


class UUser():
    '''
        User's data
    '''
    def __init__(self, nickname, main_project=None):
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

        ## list of all user's projects, include 'life' as default 
        # self.projects = [UProject(self.nickname, "Life"), ]
        self.projects = [main_project, ] if main_project else None

        '''
            Working context
        '''
        ## pointer on template utem - to make new, to load, to watch parameters, to add to project, work on index page
        self.temp_utem = None ## 

        ## pointer on current project user is working with - def as Life
        self.pro_project = 0

        ## pointer to current contract from projects user is working with
        self.pro_contract = None
        
        ## pointer to current skill from projects user is working with
        self.pro_skill = None

        ## searching utems
        self.search = None


    def copy_workutem(self):
        return copy.deepcopy(self.temp_utem)
    
    def get_project(self):
        return self.projects[self.pro_project]


    def save_event(self, event):
        logging.info(f'data: {event}\n')

        ## make copy of skill
        skill = self.copy_workutem()

        ## set executor & event
        skill.set_event(self, event)
        # logging.info(f" {skill} : {self.temp_utem}")

        current_project = self.get_project()
        # logging.info(f" {current_project} : {type(current_project)}")

        ## save event to plan as tuple
        try:
            current_project.add_skill(skill)
        except Exception as exc:
            logging.exception(f"add new event error {exc}")

        logging.info(f"Project skills: {current_project.skills} ")


            ## we  have got it all of these in form.cleaned_data {}
            # start_date = form.cleaned_data['start_date']
            # once = form.cleaned_data['start_date']
            # daily = form.cleaned_data['start_date']
            # work = form.cleaned_data['start_date']
            # weekly = form.cleaned_data['start_date']
            # atday = form.cleaned_data['start_date']
            # atweek = form.cleaned_data['start_date']
            # atweek = form.cleaned_data['start_date']
            # yearly = form.cleaned_data['start_date']
            # wdays = form.cleaned_data['start_date']
            # w_monday = form.cleaned_data['start_date']
            # w_tuesday = form.cleaned_data['start_date']
            # w_wednsday = form.cleaned_data['start_date']
            # w_thirsday = form.cleaned_data['start_date']
            # w_friday = form.cleaned_data['start_date']
            # w_saturday = form.cleaned_data['start_date']
            # w_sunday = form.cleaned_data['start_date']
            # start_time = form.cleaned_data['start_date']
            # end_time = form.cleaned_data['start_date']
            # duration = form.cleaned_data['start_date']
            # rem_5 = form.cleaned_data['start_date']
            # rem_15 = form.cleaned_data['start_date']
            # rem_30 = form.cleaned_data['start_date']
            # rem_1h = form.cleaned_data['start_date']
            # rem_1d = form.cleaned_data['start_date'] 


        
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
    