"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

import logging
import copy

from .bases import UtemBase
from .uobject import UObject

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


    def init_storage(self, storage):
        self.storage = storage

    def init_utem_base(self, base:UtemBase, root:UObject=None):
        ## base of user's utems
        self.utems = base
        if isinstance(root, UObject):
            self.utems.add(copy.deepcopy(root))
            ## pointer to current skill from projects user is working with
            self.root_utem = self.utems.read(root.get_token())
        else:
            self.root_utem = None
    

    def add_utem(self, utem):
        if hasattr(self, "utems"):
            self.utems.add(copy.deepcopy(utem), self.root_utem.get_token())


        
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
    