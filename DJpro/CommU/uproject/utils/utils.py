"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import os
import logging

from ..models.uobject import UObject
from ..models.skill import USkill
from ..models.contract import UContract
from ..models.project import UProject
from ..models.user import UUser
from ..storage.filestorage import FileStorage
from ..models.bases import UtemBase

def upload_utembase(storage, base: UtemBase, file_list): 
    '''
        Fill UtemBase with file list
        Args:
            storage - file storage | DB
            base: UtemBase
            file_list - ['*.stp', ]
    '''
    utem = None

    for item in file_list:
        id = os.path.splitext(item)[0]
        ## check for uniq
        if base.read(id) == None:
            if '.stp' in os.path.splitext(item):
                utem = USkill()
            elif '.ctp' in os.path.splitext(item):
                utem = UContract()
            elif '.ptp' in os.path.splitext(item):
                utem = UProject()
            else:
                continue

            ## Load data of <utem> from file <item>
            if storage.load(utem, item):
                base.add(utem)


def make_template_context(base: UtemBase):
    skill_list = []
    contract_list = []
    project_list = []

    for item in base:
        utem = item['utem']
        print(f"template: {utem} {utem.get_state()} {utem.get_classname()}")
        if utem.get_state() == "template":
            if utem.get_classname() =="USkill":
                skill_list.append({"name":utem.name, "link":f"{utem.make_link()}"})
            elif utem.get_classname() == "UContract":
                contract_list.append({"name":utem.name, "link":f"{utem.make_link()}"})
            elif utem.get_classname() == "UProject":
                project_list.append({"name":utem.name, "link":f"{utem.make_link()}"})                

    return {'template_skills': skill_list,
            'template_contracts': contract_list,
            'template_project': project_list
        }
            
    
def parse_link(arg: str):
    try:
        type_str, name = arg.split("=")
        return type_str.lower(), name
    except ValueError:
        logging.info(f" wrong args: {arg}\n")
        return None, None


# def make_skill_context(skills: list, path="."):
#     context = []
#     storage = FileStorage(path)
#     for name in skills:
#         utem = USkill(name)
#         storage.load(utem)
#         context.append({"name": utem.name, "link": (f"{utem.__class__.__name__}={utem.get_slug_name()}").lower()})
    
#     return context
    

def find_utems(key_name, path="."):
    storage = FileStorage(path)
    context = {}

    for cls, label in [(USkill, "find_skills"), (UContract, "find_contracts"), (UProject, "find_projects")]:
        utem = cls(key_name)
        # logging.info(f"find {utem} {key_name}")
        found = storage.load(utem)
        
        context[label] = [utem.name] if found else None

    # context["find_dealers"] = [user.partners] if user else public_dealers
    logging.info(f" return context {context}")
    return context


def get_utem_info(utem):
    '''
        Return dict with info about founded utem
    '''    
    context = {}
    info = [f"{k}: {v}" for k, v in utem.to_dict().items() if k != 'name' and not k.startswith('_') and v]
    
    context.update({"about_type": utem.__class__.__name__.lower(),
                    "about_name": utem.name,
                    "about_value": info})
    return context


def get_project_tree(user: UUser):

    logging.info(f"root {user.root_utem}")

    root_path = [{"name": user.root_utem.name, "link": user.root_utem.make_link()}, ]

    context = {"root_path": root_path }

    context.update(walk_by_tree(user))

    return context


def walk_by_tree(user):

    base = user.utem_base
    root = user.root_utem

    if isinstance(root, UProject):
        if len(root.projects) > 0:
            sub_pro = []
            for item in root.projects:
                ##sub_pro.append(walk_by_tree(base, base.read(item)))
                obj = base.read(item)
                sub_pro.append({"name": obj.name, "link": obj.make_link})
        else:
            sub_pro = None
        
        if len(root.contracts) > 0:
            sub_con = []
            for item in root.contracts:
                #sub_con.append(walk_by_tree(base, base.read(item)))
                obj = base.read(item)
                sub_pro.append({"name": obj.name, "link": obj.make_link})
        else:
            sub_con = None

        if len(root.events) > 0:
            sub_ev = []
            for item in root.events:
                ##sub_ev.append(walk_by_tree(base, base.read(item)))
                obj = base.read(item)
                sub_pro.append({"name": obj.name, "link": obj.make_link})
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
                ##sub_ev.append(walk_by_tree(base, base.read(item)))
                obj = base.read(item)
                sub_pro.append({"name": obj.name, "worker": credit_worker, "link": obj.make_link})
        else:
            sub_credit_ev = None

        if len(root.debet_events) > 0:
            sub_debet_ev = []
            for item in root.debet_events:
                obj = base.read(item)
                sub_pro.append({"name": obj.name, "worker": debet_worker, "link": obj.make_link})
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