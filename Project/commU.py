"""
Project commU
"""
from os import system
from typing import Any


class Main():
    def __init__(self) -> None:
        self.stop = False
        self.context = 'main'

    def show_menu(self):
        if self.context == 'main':
            print('<ESC - exit> | <F1 - log in> | <F2 - reg in> \n')

    def show_table(self):
        if self.context == 'main':
            print('Welcome to commU\n')
        
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        
        while not self.stop:
            system('cls')

            self.show_menu()

            self.show_table()

            input('comm:> ')
            break
            

pro = Main()
pro()