"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
import logging

from ..models.skill import USkill
from ..models.contract import UContract
from ..models.project import UProject
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
    result = {}
    info = [f"{k}: {v}" for k, v in utem.to_dict().items() if k != 'name' and not k.startswith('_') and v]
    utem_type = utem.__class__.__name__.lower()
    result.update({"about_type": utem_type, "about_name": utem.name, "about_value": info})
    return result
