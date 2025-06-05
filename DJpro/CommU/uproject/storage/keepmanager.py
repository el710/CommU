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
        return self.base.read(utem_id)

    def edit_utem(self, utem_id, new_utem):
        self.base.edit(id_hash=utem_id, new_utem=new_utem)
        return self.storage.save(new_utem, overwrite = True)

    def delete_utem(self, utem):
        self.storage.delete(utem)
        self.base.delete(utem.get_token())


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

        for item in self.base:
            if name == item['utem'].get_name():
                label = f"find_{item['type']}"
                context[label] = {"name": item['utem'].get_name(), "link": item['utem'].make_link()}
                
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

        root_path = [{"name": user.root_utem.name, "link": user.root_utem.make_link()}, ]
        
        context = {"root_path": root_path }
        context.update(self.walk_by_tree(user))

        return context
 

    def walk_by_tree(self, user):
        base = self.base
        root = user.root_utem

        if isinstance(root, UProject):
            if len(root.projects) > 0:
                sub_pro = []
                for item in root.projects:
                    obj = base.read(item)
                    sub_pro.append({"name": obj.name, "link": obj.make_link})
            else:
                sub_pro = None
        
            if len(root.contracts) > 0:
                sub_con = []
                for item in root.contracts:
                    obj = base.read(item)
                    sub_con.append({"name": obj.name, "link": obj.make_link})
            else:
                sub_con = None

            if len(root.events) > 0:
                sub_ev = []
                for item in root.events:
                    obj = base.read(item)
                    sub_ev.append({"name": obj.name, "link": obj.make_link})
            else:
                sub_ev = None

        elif isinstance(root, UContract):
            if user.commu_id == root.holder_id:
                credit_worker = None
                debet_worker = root.dealer_id
            else:
                credit_worker = user.nickname
                debet_worker = None
            
            if len(root.credit_events) > 0:
                sub_credit_ev = []
                for item in root.credit_events:
                    obj = base.read(item)
                    sub_credit_ev.append({"name": obj.name, "worker": credit_worker, "link": obj.make_link})
            else:
                sub_credit_ev = None

            if len(root.debet_events) > 0:
                sub_debet_ev = []
                for item in root.debet_events:
                    obj = base.read(item)
                    sub_debet_ev.append({"name": obj.name, "worker": debet_worker, "link": obj.make_link})
            else:
                sub_debet_ev = None
            
            sub_ev = sub_credit_ev + sub_debet_ev
            sub_pro = None
            sub_con = None

        elif isinstance(root, USkill):
            sub_pro = None
            sub_con = None
            sub_ev = None
    
        context = { "name": root.get_title(), "link": root.make_link(),
                    "projects": sub_pro, ## [context, context, ...]
                    "contracts": sub_con, ## [context, context, ...]
                    "events": sub_ev  ## [context, context, ...]
                }
        
        return context