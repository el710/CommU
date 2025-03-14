"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""
try:
    from .uproject import UProject
except:
    from uproject import UProject

class UUser():
    def __init__(self, nickname):
        self.commu_id = None
        self.nickname = nickname
        self.password = None
        self.email = None

        self.firstname = None
        self.lastname = None
        self.language = 'en'

        ## list of all user's life partners - phone book
        self.partners = [] 
        ## list of all user's projects, include 'life' as default 
        self.projects = [UProject("Life", self.nickname), ]
        
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