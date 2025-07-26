"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""
import os
import logging
import copy

# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent /"." ))


from .uobject import get_hash

from uproject.constants.constants import *

from uproject.models.project import UProject

from uproject.storage.keepmanager import KeepManager
from uproject.storage.filestorage import FileStorage

class UUser():
    '''
        User's data
    '''
    def __init__(self, nickname:str):
        self.commu_id = UUser.make_userid(nickname) if nickname != GUEST_USER else None

        self.nickname = nickname
        self.password = None
        self.email = None

        self.firstname = None
        self.lastname = None

        self.timezone = None
     

        '''
            Working context
        '''
        ## keyword for searching utems
        self.search = None

        ## pointer on utem we work with
        self.work_utem = None

        ## utem that we opened for editing
        ## for checking if it was changed
        self.origin_utem_id = None

        ## pointer to work project or contract
        self.root_utem = None

        ## pointer to choosen event
        self.pro_event = None
      
         ## list of all user's contacts - phone book
        self.contacts = None
      
        self.keep_manager = KeepManager(self.commu_id)

        ## checkout is there any data of that user
        if self.keep_manager.connection:
            '''
                Load user data from database
            '''
            ## read profile
            # self.keep_manager.read_user(self.commu_id)

            self.root_utem = UProject(name=MAIN_PROJECT)
            self.keep_manager.read_utem(self.root_utem)

        else:
            '''
                No data - new user
            '''
            self.keep_manager.init_base(self.commu_id)

            self.language = 'en'
            self.geosocium = DEFAULT_GEOSOCIUM
            self.using_file_storage = True

            self.keep_manager.save_user(self.commu_id, self.get_profile())

            ## basic project Life for User
            self.root_utem = UProject(name=MAIN_PROJECT, starter_user_id=self.commu_id, state=ROOT_PROJECT, my_token=self.commu_id)
            self.root_utem.sign(self)
            self.keep_manager.save_utem(self.root_utem)


    @staticmethod
    def make_userid(username):
        return get_hash(username)

    def get_profile(self):
        return {
            'nickname': self.nickname,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'timezone': self.timezone,
            'language': self.language,
            'geosocium': self.geosocium,
            'using_file_storage': self.using_file_storage
        }


    def set_work_utem(self, utem):
        if not self.work_utem:
            self.work_utem = utem
        return self.work_utem
    
    def del_work_utem(self):
        self.work_utem = None
        

    



if __name__ == "__main__":

    user = UUser("test")
    print(vars(user))
    