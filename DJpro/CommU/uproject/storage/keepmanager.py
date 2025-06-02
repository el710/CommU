"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import os
import logging

from .bases import UtemBase
from .filestorage import FileStorage

from ..models.skill import USkill
from ..models.contract import UContract
from ..models.project import UProject


class KeepManager(UtemBase, FileStorage):
    '''
        Manager for sinchronize UtemBase & Storage
    '''
    
    def __init__(self, storage):
        self.base = UtemBase()
        self.storage = storage

    def save_utem(self, utem):
        self.base.add(utem)
        return self.storage.save(utem, overwrite = True)

    def read_utem(self, utem_id):
        pass

    def edit_utem(self, utem):
        pass

    def delete_utem(self, utem):
        pass


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
            if utem.get_state() == state or not state:
                if utem.get_classname() == 'USkill':
                    _list = skill_list
                elif utem.get_classname() == 'UContract':
                    _list = contract_list
                elif utem.get_classname() == 'UProject':
                    _list = project_list
                else:
                    _list = None
                
                try:
                    _list.append({"name":utem.name, "link":f"{utem.make_link()}"})
                except:
                    logging.info(f"wrong utem  {utem.get_classname()}\n")

        return {f"{state}_skills": skill_list,
                f"{state}_contracts": contract_list,
                f"{state}_project": project_list
            }
    
    def find_by_name(self, name):
        context = {}
        for cls, label in [(USkill, "find_skill"), (UContract, "find_contract"), (UProject, "find_project")]:
            utem = cls(name)
            # logging.info(f"find {utem} {key_name}")
            found = self.storage.load(utem)

            context[label] = [utem.name] if found else None
        
        # context["find_dealers"] = [user.partners] if user else public_dealers
        logging.info(f" return context {context}")
        return context
