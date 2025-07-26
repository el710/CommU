"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import os
import logging

from ..constants import DEFAULT_DIRECTORY

from .bases import UtemBase
from .filestorage import FileStorage
from ..database.db import *

from ..models.uobject import get_hash

from ..models.skill import USkill
from ..models.contract import UContract
from ..models.project import UProject

class UserProfile():
    def __init__(self, owner, **kwargs):
        self.file_name = f"{owner}.utp"
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        return self.__dict__.copy()

class KeepManager(UtemBase, FileStorage):
    '''
        Manager for sinchronize UtemBase & Storage
        UtemBase - RAM data
        Storage: files & DataBase

    '''
    _work_path = None

    @classmethod
    def get_work_path(cls):
        """
            Get default working directory for file storage
            Returns:
                path to directory
        """
        if cls._work_path is None:
            return os.path.join(os.getcwd(), DEFAULT_DIRECTORY)
        return cls._work_path

    @classmethod
    def set_work_path(cls, value):
        """
            Set default working directory for file storage
            Args:
                value - path to directory
        """
        cls._work_path = value
        logging.info(f"Set work directory: {cls._work_path}")
 


    def __init__(self, owner):
        '''
            find owner in database
        '''
        temp_storage = FileStorage(KeepManager.get_work_path(), f"{owner}")

        # if there is user:
        #     self._conection = True
        # else:
        self._conection = False
        
        self.base = UtemBase()


    def init_base(self, owner):
        self.storage = FileStorage(KeepManager.get_work_path(), f"{owner}")
        self._conection = True


    @property
    def connection(self):
        return self._conection
        

    def save_user(self, user_id, profile):
        '''
            Save user profile to storage
            Args:
                PROFILE - dict with user data
        '''
        if not self._conection:
            logging.info("No connection to storage")
            return False
        
        user_profile = UserProfile(user_id, **profile)
        logging.info(f"Save user: {user_profile}")

        return self.storage.save(user_profile, overwrite=True)

    def read_user(self, user_id):
        pass

############  Utems CRUD
    def save_utem(self, utem):
        self.base.add(utem)
        return self.storage.save(utem, overwrite = True)

    def read_utem(self, utem_id):
        return self.base.read(utem_id)

    def edit_utem(self, utem_id, new_utem):
        self.base.edit(id_hash=utem_id, new_utem=new_utem)
        return self.storage.save(new_utem, overwrite = True)

    def delete_utem(self, utem):
        self.storage.delete(utem)
        self.base.delete(utem.token)


    def upload_base(self, utem_patterns=['Uproject']):
        '''
            Fill UtemBase with file list
            Args:
                utem_patterns - ['UProject', ...]
        '''
        utem = None
        file_list = []

        for obj in utem_patterns:
            if obj == 'UProject':
              file_list.extend(self.storage.find_all("*.ptp"))
            elif obj == 'UContract':
              file_list.extend(self.storage.find_all("*.ctp"))
            elif obj == 'USkill':
              file_list.extend(self.storage.find_all("*.stp"))
        
        if len(file_list) == 0: return

        # logging.info(f"Load base from list: {file_list}\n")

        for file in file_list:
            id = os.path.splitext(file)[0]

            ## check is there such utem in base already
            if self.base.read(id) == None:
                if '.stp' in os.path.splitext(file):
                    utem = USkill()
                elif '.ctp' in os.path.splitext(file):
                    utem = UContract()
                elif '.ptp' in os.path.splitext(file):
                    utem = UProject()
            else:
                continue

            ## Load data of <utem> from file
            if self.storage.load(utem, file):
                self.base.add(utem)
    
    def find_by_state(self, state=None):
        '''
            Make list of utems with state == pattern
            Args:
                pattern = type of utem's state (constants.constants)
        '''
        skill_list = []
        contract_list = []
        project_list = []
        
        for item in self.base:
            utem = item['utem']
            if utem.state == state or not state:
                if utem.classname == 'USkill':
                    _list = skill_list
                elif utem.classname == 'UContract':
                    _list = contract_list
                elif utem.classname == 'UProject':
                    _list = project_list
                else:
                    _list = None
                
                try:
                    _list.append({"name":utem.name, "link":f"{utem.link}"})
                except:
                    logging.info(f"wrong utem  {utem.classname}\n")

        return {f"{state}_skills": skill_list,
                f"{state}_contracts": contract_list,
                f"{state}_project": project_list
            }
    
    def find_by_name(self, name):
        context = {}

        for item in self.base:
            if name == item['utem'].name:
                label = f"find_{item['type']}"
                context[label] = {"name": item['utem'].name, "link": item['utem'].link}
                
        # for cls, label in [(USkill, "find_skill"), (UContract, "find_contract"), (UProject, "find_project")]:
        #     utem = cls(name=name)
        #     # logging.info(f"find {utem} {key_name}")
        #     found = self.storage.load(utem)
        #     context[label] = [utem.name] if found else None
        
        # context["find_dealers"] = [user.partners] if user else public_dealers
        logging.info(f" return context {context}")
        return context

    def get_tree(self, user):
        logging.info(f"root {user.root_utem}")

        root_path = [{"name": user.root_utem.name, "link": user.root_utem.link}, ]
        
        context = {"root_path": root_path }
        context.update(self.walk_by_tree(user))

        return context
 

    def walk_by_tree(self, user):
        base = self.base
        root = user.root_utem

        if isinstance(root, UProject):
            if len(root.projects) > 0:
                sub_projects = []
                for item in root.projects:
                    obj = base.read(item)
                    sub_projects.append({"name": obj.name, "link": obj.link})
            else:
                sub_projects = None
        
            if len(root.contracts) > 0:
                sub_contracts = []
                for item in root.contracts:
                    obj = base.read(item)
                    sub_contracts.append({"name": obj.name, "link": obj.link})
            else:
                sub_contracts = None

            if len(root.events) > 0:
                sub_events = []
                for item in root.events:
                    obj = base.read(item)
                    sub_events.append({"name": obj.name, "link": obj.link})
            else:
                sub_events = None

        elif isinstance(root, UContract):
            if user.commu_id == root.holder_id:
                credit_worker = None
                debet_worker = root.dealer_id
            else:
                credit_worker = user.nickname
                debet_worker = None
            
            if len(root.credit_events) > 0:
                sub_credit_events = []
                for item in root.credit_events:
                    obj = base.read(item)
                    sub_credit_events.append({"name": obj.name, "worker": credit_worker, "link": obj.link})
            else:
                sub_credit_events = None

            if len(root.debet_events) > 0:
                sub_debet_events = []
                for item in root.debet_events:
                    obj = base.read(item)
                    sub_debet_events.append({"name": obj.name, "worker": debet_worker, "link": obj.link})
            else:
                sub_debet_events = None
            
            sub_events = sub_credit_events + sub_debet_events
            sub_projects = None
            sub_contracts = None

        elif isinstance(root, USkill):
            sub_projects = None
            sub_contracts = None
            sub_events= None
    
        context = { "name": root.title, "link": root.link,
                    "projects": sub_projects, ## [context, context, ...]
                    "contracts": sub_contracts, ## [context, context, ...]
                    "events": sub_events  ## [context, context, ...]
                }
        
        return context