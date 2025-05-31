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
            if obj == 'Uproject':
              file_list.append(self.storage.find_all("*.ptp"))
            elif obj == 'UContract':
              file_list.append(self.storage.find_all("*.ctp"))
            elif obj == 'USkill':
              file_list.append(self.storage.find_all("*.stp"))
        
        if len(file_list) == 0: exit()

        logging.info(f"Load base from list: {file_list}\n")

        for item in file_list:
            id = os.path.splitext(item)[0]

            ## check is there such utem in base already
            if self.base.read(id) == None:
                if '.stp' in os.path.splitext(item):
                    utem = USkill()
                elif '.ctp' in os.path.splitext(item):
                    utem = UContract()
                elif '.ptp' in os.path.splitext(item):
                    utem = UProject()
            else:
                continue

            ## Load data of <utem> from file <item>
            if self.storage.load(utem, item):
                self.base.add(utem)