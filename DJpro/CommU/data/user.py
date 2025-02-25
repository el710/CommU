"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""

class UUser():
    def __init__(self):
        self.commu_id = None
        self.nickname = None
        self.password = None
        self.email = None

        self.firstname = None
        self.lastname = None
        self.language = 'en'
        
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
