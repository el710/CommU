"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""
# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent /"." ))

import logging

from .uobject import get_hash
from .project import UProject

from ..constants.constants import *
from ..storage.keepmanager import KeepManager


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
        ## token is like a check sum of data
        self.origin_utem_token = None

        ## pointer to work project or contract
        self.root_utem = None

        ## pointer to choosen event
        self.pro_event = None
      
         ## list of all user's contacts - phone book
        self.contacts = None
        
        self.language = 'en'
        self.geosocium = DEFAULT_GEOSOCIUM
        self.using_file_storage = True

        self.root_utem = UProject(name=MAIN_PROJECT, author_id=self.commu_id, state=ROOT_PROJECT, hard_sign=self.commu_id)

        logging.info(f'make user: {self.commu_id} {self.geosocium}')

        self.root_utem.sign(author_id=self.commu_id, geosocium=self.geosocium)
          
        self.keep_manager = KeepManager(self.commu_id)

        if self.keep_manager.read_user(self.commu_id):
            load = self.keep_manager.upload_base(utem_patterns=['Uproject', 'UContract, USkill'])
            if load == 0:
                self.keep_manager.save_utem(self.root_utem)
        else:
            self.keep_manager.save_user(self.commu_id, profile=self.get_profile())
            

            






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
    