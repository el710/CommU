"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

import logging
import copy

# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent /"." ))


from .uobject import get_hash

from uproject.constants.constants import *

class UUser():
    '''
        User's data
    '''
    def __init__(self, nickname:str):
        self.commu_id = get_hash(nickname) if nickname != GUEST_USER else None

        self.nickname = nickname
        self.password = None
        self.email = None

        self.firstname = None
        self.lastname = None
        self.language = 'en'

        self.geosocium = DEFAULT_GEOSOCIUM
        self.timezone = None
     

        '''
            Working context
        '''
        ## searching utem
        self.search = None

        ## pointer on utem work with
        self.work_utem = None
        self.origin_utem_id = None


        ## pointer to work project or contract
        self.root_utem = None

        ## pointer to choosen event
        self.pro_event = None
      
         ## list of all user's contacts - phone book
        self.contacts = None


    def init_storage(self, storage):
        ## Hard storage: files / DB
        self.storage = storage

    def init_utem_base(self, base):
        ## RAM base of user's utems
        self.utem_base = base
    
    def init_keep_manager(self, manager):
        self.keep_manager = manager




        
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
    