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


# from pydantic import BaseModel
from slugify import slugify
import json

import os
import logging
from datetime import datetime

'''
    Data constants
'''
GUEST_USER = 'Guest'



class UObject():
    '''
        Common class for CommU atomic items: skill, contract, project (Utems)
    '''

    def __init__(self, name):

        ## name of object
        self.name = name  

        ## Author who create particular Utem
        self.author = None

        ## date & time
        ## when particular Utem has been created
        self.create_datetime = None

        ## geosocuim - dictionary of community depends on place (Earth, city/town, village, family, ...)
        ## in what community it works
        self.geosocium = None

        self.public = False


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
            if key in vars(self):
                if key == "create_datetime":
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
    
    def set_public(self):
        self.public = True
    
    def set_personal(self):
        self.public = False
    
    def get_token(self):
        return hash(f"{self.name}:{self.author}:{self.create_datetime}:{self.geosocium}")


    def make_link(self):
        return f"{slugify(self.name)}:{self.get_token()}" 


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
    
    def json(self):
        temp = vars(self) ## or <self.__dict__>  
        if isinstance(temp["create_datetime"], datetime):
            ## make dictionary from subobject 'dateTime'
            temp["create_datetime"] = temp["create_datetime"].isoformat()
        
        ## for USkill object
        if isinstance(self, USkill):
            if temp["_event"]:
                ## make dictionary from subobject 'event'
                temp["_event"] = vars(temp["_event"])
        return temp
    

    def save_as_template(self, over:bool=False, path=None):
        """
            Save structure of object as dictionary template
        """

        temp = self.json()
        
        logging.info(f"\ndict object: {temp} ")
        logging.info(f"dir: {os.getcwd()}\n")

        if path: 
            _name = os.path.join(path, self.get_file_name())
        else:
            _name = self.get_file_name()
        logging.info(f"file name {_name}")

        if not over:
            """IF file exists """
            if os.path.isfile(_name):
                return False
        
        with open(_name, mode='w', encoding='utf-8') as file:
            file.write(json.dumps(temp)) ## write dict as string
        
        return True


    def load_template(self, path=None):
        """
            Load template of object
        """
        if path:
            _name = os.path.join(path, self.get_file_name())
        else:
            _name = self.get_file_name()

        logging.info(f"trying to find template {_name}")
        
        try:
            with open(_name, mode='r', encoding='utf-8') as file:
                data = json.loads(file.read()) ## make dict from string

                self.set(**data)
            logging.info(f"has found template {_name}")

            return True
        except Exception as exc:
            logging.info(f"can't open template {_name} {exc}")
            return False

    def delete_template(self, path=None):
        """
            Delete template of object
        """
        if path:
            _name = os.path.join(path, self.get_file_name())
        else:
            _name = self.get_file_name()

        logging.info(f"trying to find template {_name}")
        
        try:
            ## !!! IT SHOULD BE REPLACE TO ARCHIVE
            os.remove(_name)
            logging.info(f"{_name} file deleted")

            return True
        except Exception as exc:
            logging.info(f"can't delete file {_name} {exc}")
            return False

def utemname_parse(args):
    '''
        find out is there a utem
        agrs: <type=name>
    '''
    if args:
        try:
            ## find out type & name of Uitem
            item = str.split(args,'=')
            logging.info(f"args: {item} size: {len(item)}\n")
            if item[0] =='skill': return type(USkill), item[1]
            if item[0] =='contract': return type(UContract), item[1]
            if item[0] =='project': return type(UProject), item[1]            
        except Exception as exc:
            logging.info(f" wrong args: {args} {exc}\n")

    return None, None


def isthere_utem(key_name, path=None):
    '''
        Search for urtems by name
    '''
    match type:
        case UTYPE_SKILL:
            return USkill(key_name).load_template(path=path)
        

    contract = UContract(key_name)
    project = UProject(key_name)

    return False


def find_utems(key_name, path=None, local_user=None, public_dealers=None):
    '''
        Find by <key_name> end return public utems
    '''
    context = {}

    logging.info(f"key {key_name}")
    if key_name:
        ## find skill templates    
        skill = USkill(key_name)
        if skill.load_template(path):
            context.update({"find_skills": [skill.get_slug_name()] })
            logging.info(f"has found skill {skill.get_slug_name()}")
        else:
            context.update({"find_skills": None})

        ## find project templates
        project = UProject(key_name)
        if project.load_template(path):
            context.update({"find_projects": project.get_file_name()})
        else:
            context.update({"find_projects": None})

        ## find contract templates
        contract = UContract(key_name)
        if contract.load_template(path):
            context.update({"find_contracts": contract.get_file_name()})
        else:
            context.update({"find_contracts": None})

        ## find public contacts
        user_dealers_list = []
        if local_user != None:
            # if isinstance(local_user, UUser):
            user_dealers_list.append(local_user.partners)
                
        if public_dealers:
            user_dealers_list.append(public_dealers)
                
        if len(user_dealers_list):
            context.update({"find_dealers": user_dealers_list})
        else: 
            context.update({"find_dealers": None})    
        
    return context


def get_utem_info(utem):
    '''
        Return dict with info about founded skill, contract or project...
    '''
    result = {}
    info = []
    if isinstance(utem, USkill):
        for key, value in utem.json().items():
            if (value != None) and (isinstance(value, str) and len(value) or not isinstance(value, str)):
                # logging.info(f"make dict of object: {key} : {value}")
                if key != 'name' and key[:1] != '_' :
                    info.append(f"{key}: {value}")
        utem_type = 'skill'

    elif isinstance(utem, UContract):
        utem_type = 'contract'
    elif isinstance(utem, UProject):
        utem_type = 'project'
    else:
        logging.info(f"wrong utem {utem}\n")
        
    logging.info(f"add object's info: {info}")
    if len(info):
        result = {"about_type": utem_type,
                  "about_name": utem.name,
                  "about_value": info
                }
        
    return result    
    


class USkill(UObject):
    """
        A simple skill that depends only on one person.
        The person do it by itself
    """
    public_skills = None
    find_static = None

    def __init__(self, name:str, description:str = None, resources:str = None, goal:str = None):
        super().__init__(name)
        
        ## how to do skill
        self.description = description 

        ## resources
        self.resources = resources

        ## object of process
        self.goal = goal ## "time"

        ## -advanced parameters

        """moment to do """
        self._event = None ## at 5:00 AM....

        """average duration"""
        self._duration = None
        
        self._state = "template" ## "offer" -> "deal" -> "done"

    
    def sign(self, author, geosocium = None, public = None):
        '''
            Sign skill at create
        '''
        self.author = author

        if geosocium:
            self.geosocium = geosocium

        ## should to save it in templates library
        if public:
            self.public = public

        self.create_datetime = datetime.now()
    
    def set_event(self, user, event):
        self.executor = user
        self._event = event
        
    
    ## overload '=='
    def __eq__(self, value):
        if value: 
            return (self.name == value.name and
                    self.resources == value.resources and
                    self.description == value.description and
                    self.goal == value.goal
                   )
        return False
    
    ## overload '!='
    def __ne__(self, value):
        if value:
            return (self.name != value.name or
                    self.resources != value.resources or
                    self.description != value.description or
                    self.goal != value.goal
                    )
        return True

    def get_slug_name(self):
        return f"{slugify(self.name)}"
    
    def load_public_skills(subdir=None):
        if USkill.find_static == None:
            os.chdir(subdir)
            USkill.find_static = os.curdir
        
        ## logging.info(f"dir {os.listdir()}")
        files = [f for f in os.listdir() if os.path.isfile(f) and ".stp" in os.path.splitext(f)]
        USkill.public_skills = [os.path.splitext(f)[0] for f in files]
    
    def get_public_skills():
        return USkill.public_skills
    

class UContract(UObject):
    """
        Deal structure for dealers
    """
    def __init__(self, contract_name, customer_id, provider_id):
        super().__init__(contract_name)
        
        ## should to save it in templates library
        self.public = False

        self.customer = customer_id
        self.provider = provider_id

        self.state = "template" ## "offer", "deal", "closed"

        ## Dealers skills
        self.customer_credit = []
        self.customer_debet = []

        self.provider_credit = []
        self.provider_debet = []

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

    def __init__(self, starter_user, project_name=None):
        """ 
            initialisation project with:
            - project_name
            - user_id
            other attributes are None
        """
        if project_name:
            super().__init__(project_name)
        else:
            super().__init__(f"{starter_user.nickname}'s project")

        self.target = "Project's point:..."
        self.project_laws = {} ## 'Do not" laws

        """Lists of other Users in project"""
        self.partners = [starter_user]
        self.customers = []
        self.workers = []
        
        """Lists of subprojects"""
        self.subprojects = [] ## list of class UProject() objects

        """Lists of contracts"""
        self.contracts = [] ## list of class UContract() objects
        
        """Lists of skills"""
        self.skills = None ## list of pair [utem.name, utem.link]

        ## should to save it in templates library
        self.public = False

        

    def add_skill(self, skill):
  
        time_moment = skill._event['start_time']

        new_item = {"name": f"{time_moment} {skill.name}", "link": skill.make_link()}

        if self.skills:
            self.skills.append(new_item)
        else:
            self.skills = [new_item]
        

        



##-----------------------------------------------------

if __name__ == "__main__":

    import os
    os.system('cls')

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: | %(module)s  %(funcName)s():   %(message)s") ##, filename="log.log")

    print("Testing class Comm UProject()...\n")

    user = "Me"
    user_project = UProject(user, "Daily health mode")
    print(user_project)

    user_contract = UContract(user)
    print(user_contract)

    
    
    def termmake(user):
        print("Terminal maker of skills\n")
        name = input("Input name of skill: ")
            
        new_skill = USkill(name=name)
        new_skill.description = input(f"Describe skill '{new_skill.name}' in simple words: ")
        new_skill.goal = input(f"What goal(result) of skill '{new_skill.name}': ")
        new_skill._event = UEvent()

        return new_skill

    new_skill = termmake(user)
    print(new_skill)
    

    new_skill.save_as_template()
    load_skill = USkill("anyone", new_skill.name)


    if load_skill.load_template():
        print(load_skill)

    # USkill.load_public_skills()
    # print(USkill.get_public_skills())




