"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
"""
    Data types to describe bussines
"""
try:
    from .uevent import *
except:
    from uevent import *


from slugify import slugify
import json

import logging

class UObject():
    def info(self):
        if isinstance(self, USkill):
            pred = "Skill"
        elif isinstance(self, UContract):
            pred = "Contract"
        elif isinstance(self, UProject):
            pred = "Project"
        else:
            pred = "UObject"

        return f"\n{pred} staff: {vars(self)}"
    
    def __str__(self):
        return self.info()
    
    def set(self, **kwargs):
        """
            Set means of object's attributes by names
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_file_name(self):
        """
            Define file name with extension
        """
        _name = f"{slugify(self.name)}"

        if isinstance(self, USkill):
            _name = _name + ".stp"
        elif isinstance(self, UContract):
            _name = _name + ".ctp"
        elif isinstance(self, UProject):
            _name = _name + ".ptp"
        else:
            _name = _name + ".otp"

        return _name

    def save_as_template(self):
        """
            Save structure of object as dictionary template
        """
        temp = self.__dict__

        if isinstance(self, USkill):
            temp["event"] = None
        
        _name = self.get_file_name()
        
        with open(_name, mode='w', encoding='utf-8') as file:
            file.write(json.dumps(temp)) 


    def load_template(self):
        """
            Load template of object
        """
        _name = self.get_file_name()

        try:
            with open(_name, mode='r', encoding='utf-8') as file:
                data = json.loads(file.read())
                self.set(**data)
            return True
        except:
            return False


class USkill(UObject):
    """
        A simple skill that depends only on one person.
        The person do it by itself
    """

    def __init__(self, name:str, goal:str = None, description:str = None, resources:str = None):
        self.name = name ## "wake up"

        """resources"""
        self.resources = resources

        """how to do skill"""
        self.description = description 

        """object of process"""
        self.goal = goal ## "time"

        """moment to do """
        self.event = None ## at 5:00 AM....

        """average duration"""
        self.duration = None
        
        self.state = "template" ## "offer" -> "deal" -> "done"
        

class UContract(UObject):
    """
        Deal structure with other dealer
    """
    def __init__(self, owner_id, owner_type:str="partner", dealer_id = None):
        self.owner_id = owner_id

        if dealer_id == None:
            self.dealer_id = owner_id
        else:
            self.dealer_id = dealer_id

        self.owner_part = owner_type ## "partner", "customer", "worker"

        self.state = "template" ## "offer", "deal", "closed"

        """owner owe to dealer"""
        self.credit_offers = [] ## offers are waiting for acception
        self.credit_skills = [] ## 

        """owner demand from dealer"""
        self.debet_offers = [] ## offers are waiting for acception
        self.debet_skills = []

        """deals history"""
        self.history = []



class UProject(UObject):
    """
        Class of user's projects store
        Here are its deals where user is:
        - partner
        - customer
        - hired worker
        and lists of its:
            - partners
            - customers
            - hired workers
        in every project

        User can have many CommUProject() objects
        but there are always default project - life project
    """

    def __init__(self, project_name, user_id):
        """ 
            initialisation project with:
            - project_name
            - user_id
            other attributes are None
        """
        self.name = project_name
        self.target = "The point of project is: ..."
        self.project_laws = {} ## 'Do not" laws
        self.user_id = user_id


        """Lists of user contracts"""
        self.partner_contracts = None ## list of class UContract() objects
        self.customer_contracts = None ## list of class UContract() objects
        self.worker_contracts = None ## list of class UContract() objects

        """Lists of other Users in project"""
        self.partners = None
        self.customers = None
        self.workers = None

    def add_(self):
        """
            Add deals...
        """
        pass



##-----------------------------------------------------

if __name__ == "__main__":

    import os
    os.system('cls')

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: | %(module)s     %(message)s")

    print("Testing class Comm UProject()...\n")

    user = "Me"
    user_project = UProject("Daily health mode", user)
    print(user_project)

    user_contract = UContract(user)
    print(user_contract)

    
    
    def termmake():
        print("Terminal maker of skills\n")
        name = input("Input name of skill: ")
            
        new_skill = USkill(name)
        new_skill.description = input(f"Describe skill '{new_skill.name}' in simple words: ")
        new_skill.goal = input(f"What goal(result) of skill '{new_skill.name}': ")
        new_skill.event = UEvent()

        return new_skill

    new_skill = termmake()
    print(new_skill)

    new_skill.save_as_template()
    load_skill = USkill(new_skill.name)

    if load_skill.load_template():
        print(load_skill)





