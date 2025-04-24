"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import logging

from ..models.skill import USkill
from ..models.contract import UContract
from ..models.project import UProject
from ..models.user import UUser
from ..storage.storage import FileStorage


def parse_utemname(arg: str):
    try:
        type_str, name = arg.split("=")
        return type_str.lower(), name
    except ValueError:
        logging.info(f" wrong args: {arg}\n")
        return None, None


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
        Return dict with info about founded skill, contract or project...
    '''    
    result = {}
    info = [f"{k}: {v}" for k, v in utem.to_dict().items() if k != 'name' and not k.startswith('_') and v]
    
    result.update({"about_type": utem.__class__.__name__.lower(), 
                   "about_name": utem.name, 
                   "about_value": info})
    return result

def get_life_tree(user: UUser):

    event_list = [{"name": event["event"].name, "link": event["event"].make_link} for event in user.events]


    context = {"user_project": "Life", ## chain to current user's project, starts with "Life"
               
               ## elements type annotation: {"name": , "link": }
               ## list of projects with "parent" = "Life"
               "life_projects": [{"name": "pro_1", "link": "pro_1"},
                                 {"name": "pro_2", "link": "pro_2"},
                                ],  
                
                ## list of contracts with "parent" = "Life" 
               "life_contracts": [{"name": "deal_1", "link": "deal_1"},
                                  {"name": "deal_2", "link": "deal_2"},
                                 ],
                
                ## list of events with "parent" = "Life"                                 
               "life_events": event_list                      
               }

            

    return context