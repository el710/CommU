import logging

from database.db import read_users_events
 
class TMessage():
    def __init__(self, args):
        self.user = args[0]["user"]
        self.message_type = args[1]["pack"]

        if self.message_type == 'create_event':
            self.task = args[1]["description"]
            self.date = args[1]["date"]
            self.time = args[1]["time"]
            self.dealer = args[1]["dealer"]
        elif self.message_type == 'read_event':
             self.username = args[1]["username"]
             self.firstname = args[1]["firstname"]
             self.lastname = args[1]["lastname"]
             self.language = args[1]["language"]
             self.is_human = args[1]["is_human"]
             self.telegram_id = args[1]["telegram_id"]
        elif self.message_type == 'update_event':
            self.event_id = args[1]["event_id"]
            self.task = args[1]["description"]
            self.date = args[1]["date"]
            self.time = args[1]["time"]
            self.dealer = args[1]["dealer"]
        else:
            self.event_id = args[1]["event_id"]
    
    def __str__(self):
        return (str(self.__dir__()))
    
    def __del__(self):
        pass

    def set_user(self, user=None): self.user = user
    def get_user(self): return self.user
    def get_message_type(self): return self.message_type


def pack_schedule(user_id=None, events_list = []):
    '''
        Make message to telegram bot
        Return: dictionary {}
    '''
    if events_list: 
        volume = len(events_list)
    else:
        volume = 0
    if events_list: 
        return {"user": user_id,
                "events_count": volume,
                "schedule": events_list}


def make_telegram_data(user_id=None, events=None):
    if user_id is None or events is None:
        ## no user - send empty messaage
        ## user have no events - send empty message
        return pack_schedule(user_id, events)
    else:
        events_list = []
        for item in events:
            events_list.append({"event_id": item.id,
                                "date": item.date,
                                "time": item.time,
                                "dealer": item.dealer,
                                "description": item.task}
            )
        return pack_schedule(user_id, events_list=events_list)    

def get_user_events(user_id):
    if user_id:
       events = read_users_events(user_id) ## list of EventModel
       logging.info(f"get_user_events(): {user_id} - events -{len(events)}")    
    else: 
        events = None
        logging.info(f"get_user_events(): {user_id} - events -{events}")    

    

    return make_telegram_data(user_id, events)