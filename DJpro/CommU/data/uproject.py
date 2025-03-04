"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
"""
    Data types to describe bussines
"""

from uevent import *
from slugify import slugify
import json

class USkill():
    """
        A simple skill that depends only on one person.
        The person do it by itself
    """

    def __init__(self, name:str, goal:str = None, event:UEvent = None, description:str = None):
        self.name = name ## "wake up"

        """how to do skill"""
        self.description = description 

        """object of process"""
        self.goal = goal ## "time"

        """moment to do """
        self.event = event ## at 5:00 AM....

        self.state = "offer" ## "offer" -> "deal" -> "done"
    
    def save_as_template(self):
        _name = f"{slugify(self.name)}.stp"
        with open(_name, mode='w', encoding='utf-8') as file:
            template = {
                "name": self.name,
                "description": self.description,
                "goal": self.goal,
                "event": self.event.dict()
            }
            file.write(json.dumps(template)) # use `json.loads` to do the reverse
            
    



class UContract():
    """
        Deal structure with other dealer
    """
    def __init__(self, owner_id, owner_type:str="parter", dealer_id = None):
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




class UProject():
    """
        Class of user data about its deals in some project
        Here are its deals where user is:
        - partner
        - customer
        - hired worker
        and lists of its:
            - partners
            - customers
            - hired workers
        in particulal project

        User can have many CommUProject() objects
    """

    def __init__(self, project_name, user_id):
        """ 
            initialisation project with:
            - project_name
            - user_id
            other attributes are None
        """
        self.name = project_name
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



    def __str__(self):
        return f"""Project '{self.name}' for user: {self.user_id}
partners: {self.partners}
customers: {self.customers}    
workers: {self.workers}
                ---
deals as partner: {self.partner_contracts}
deals as customer: {self.customer_contracts}
deals as worker: {self.worker_contracts}
                """

##-----------------------------------------------------

if __name__ == "__main__":

    import os
    os.system('cls')

    print("Testing class CommUProject()...\n")

    user = "Me"
    user_project = UProject("Daily health schedule", user)
    print(user_project)

    
    
    def termmake():
        print("Terminal maker of skills\n")
        name = input("Input name of skill: ")
            
        new_skill = USkill(name)
        new_skill.description = input(f"Describe skill '{new_skill.name}' in simple words: ")
        new_skill.goal = input(f"What goal(result) of skill '{new_skill.name}': ")
        new_skill.event = UEvent()

        return new_skill

    new_skill = termmake()
    new_skill.save_as_template()





