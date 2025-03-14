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
    start_moment: datetime
    end_moment: datetime

    repeat_var = {"once", "daily", "weekly"}
    set_repeat: str

    notification: str

    def dict(self):
        return {
            "start_moment": "*",
            "end_moment": "*",
            "repeat": "*",
            "notification": "*"
        }
    
    def __str__(self):
        return f"{json.dumps(self.dict)}"