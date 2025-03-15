"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""
"""
    Data types to describe moment in time
"""
import datetime
import json

EVERYDAY = 1
WORKDAY = 2

SUNDAY = 0
MONDAY = 1
THUESDAY = 2
WEDNESDAY = 3

class UEvent():
    def __init__(self):
        """ 
            Moments of event
            'None' means 'does not metter
            initialize as "every day"
        """

        """ start moment """
        self.start_year = None
        self.start_mounth = None
        self.start_day = None
        self.start_hour = None
        self.start_minute = None
        self.start_second = None

        """ end moment """
        self.end_year = None
        self.end_mounth = None
        self.end_day = None
        self.end_hour = None
        self.end_minute = None
        self.end_second = None

        """how to repeat"""
        ## {"once|None", "daily", "at work days", "weekly", "mounthly day", "mounth first week day", "yearly", "special"}
        self.repeat = None

        """when to remind"""
        ## {None, "5min, "15min", "30min", "1hour", "1day", }
        self.remind = None

    def __str__(self):
        return f"Event staff: {self.__dict__}"
    

if __name__ == "__main__":
    event = UEvent()
    print(event)