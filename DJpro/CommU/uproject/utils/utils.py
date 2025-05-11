"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import os
import logging

from ..models.skill import USkill
from ..models.contract import UContract
from ..models.project import UProject
from ..models.user import UUser
from ..storage.filestorage import FileStorage


def parse_link(arg: str):
    try:
        type_str, name = arg.split("=")
        return type_str.lower(), name
    except ValueError:
        logging.info(f" wrong args: {arg}\n")
        return None, None

def find_public_skills(subdir=None):
    os.chdir(subdir)
    # match type:
    #     case 'skill': ext = '.stp'
    #     case 'contract': ext = '.ctp'
    #     case 'project': ext = '.ptp'
    #     __: ext = ''

    files = [f for f in os.listdir() if os.path.isfile(f) and '.stp' in os.path.splitext(f)]
    os.chdir('..')
    return [os.path.splitext(f)[0] for f in files]

def make_skill_context(skills: list, path="."):
    context = []
    storage = FileStorage(path)
    for name in skills:
        utem = USkill(name)
        storage.load(utem)
        context.append({"name": utem.name, "link": (f"{utem.__class__.__name__}={utem.get_slug_name()}").lower()})
    
    return context
    

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

    root_path = "recursive by tree"

    if isinstance(user.root_utem, UContract):
        link = f"/contract/{user.root_utem.make_link()}"
    elif isinstance(user.root_utem, UProject):
        link = f"/project/{user.root_utem.make_link()}"
    else:
        link = "/"

    root = {"name": user.root_utem.get_title(), "link": link}

    event_list = [{"name": event['utem'].get_title(), "link": f"/event/{event['utem'].make_link()}"} for event in user.utems 
                  if isinstance(event['utem'], USkill) and event['parent'] == user.root_utem.get_token()]


    context = { "root_path": root_path,
                "root": root, ## current user's project
               
               ## elements type annotation: {"name": , "link": }
               ## list of projects with "parent" = "Life"
               "projects": [{"name": "pro_1", "link": "/project/pro_1"},
                                 {"name": "pro_2", "link": "/project/pro_2"},
                                ],  
                
                ## list of contracts with "parent" = "Life" 
               "contracts": [{"name": "deal_1", "link": "/contract/deal_1"},
                                  {"name": "deal_2", "link": "/contract/deal_2"},
                                 ],
                
                ## list of events with "parent" = "Life"                                 
               "events": event_list                      
               }

            

    return context