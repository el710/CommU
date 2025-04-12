"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

try:
    from .uproject import UProject
except:
    from uproject import UProject

class UUser():
    '''
        User's data
    '''
    def __init__(self, nickname):
        self.commu_id = None
        self.nickname = nickname
        self.password = None
        self.email = None

        self.firstname = None
        self.lastname = None
        self.language = 'en'

        self.geosocium = 'Earth'
        self.timezone = None

        ## list of all user's contacts - phone book
        self.contacts = None

        self.partners = None

        ## list of all user's projects, include 'life' as default 
        self.projects = [UProject("Life"), ]

        '''
            Working context
        '''
        ## pointer on template utem - to make new, to load, to watch parameters, to add to project, work on index page
        self.temp_utem = None ## 

        ## pointer on current project user is working with - def as Life
        self.pro_project = 0

        ## pointer to current contract from projects user is working with
        self.pro_contract = None
        
        ## pointer to current skill from projects user is working with
        self.pro_skill = None

        ## searching utems
        self.search = None




        
class ClientUser(UUser):
    users = [] ## login + tokens

    def __init__(self):
        super().__init__()
        self.login = False ## is user login/logout

    def is_login(self):
        return self.login
    
    def log_in(self):
        self.login = True

    def log_out(self):
        self.login = False    


if __name__ == "__main__":

    user = UUser("test")
    print(user.projects[0])