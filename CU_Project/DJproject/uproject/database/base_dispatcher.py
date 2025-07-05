"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

import logging
import time
import queue
from queue import Empty

from  telegram.bot_api import TMessage, get_user_events

from .data import CreateUser, CreateEvent
from .db import (create_base_user, read_base_user,
                 create_base_event, update_base_event,
                 delete_base_event)

user_schedule = {}

def start_base_dispatcher(*args):
    # main work cycle

    cycle_start = True

    if args :
        logging.info(f"start_base_dispatcher(): get link {args[0]} - {args[1]}")
        client_in = args[0] ## get 'in client' queue descriptor
        client_out = args[1] ## get 'client out' queue descriptor
    else:
        cycle_start = False
        logging.info("start_base_dispatcher(): there are no arguments")

    while cycle_start:
        # print("Main(): wait...")
        try:
            event_query = client_out.get(timeout=1)
            # print(f"\nMain() get: {event_query}")

            ## parse message
            mess = TMessage(event_query)
            
            logging.info(f"get message: {mess.get_message_type()}")

            match mess.get_message_type():
                case "create_event":
                    logging.info("add event")
                    tmp_user = read_base_user(mess.get_user())
                    logging.info(f"{tmp_user.__str__()}")

                    if tmp_user:
                        new_event = CreateEvent(task = mess.task,
                                                date = mess.date,
                                                time = mess.time,
                                                owner_id = tmp_user.id,
                                                dealer = mess.dealer
                                            )
                        create_base_event(new_event)

                case "read_event":
                    logging.info("read & login user")
                    
                    tmp_user = read_base_user(mess.get_user())
                    logging.info(f"user: {tmp_user}")

                    if tmp_user is None:
                        tmp_user = CreateUser(username = mess.username,
                                              firstname = mess.firstname,
                                              lastname = mess.lastname,
                                              email = 'user@mail',
                                              language = mess.language,
                                              is_human = mess.is_human,
                                              telegram_id = mess.telegram_id
                                             )
                        
                        logging.info(f"create user: {tmp_user}")    
                        create_base_user(tmp_user)

                case "update_event":
                    logging.info("update event")
                    tmp_user = read_base_user(mess.get_user())
                    
                    if tmp_user:
                        new_event = CreateEvent(task = mess.task,
                                                date = mess.date,
                                                time = mess.time,
                                                owner_id = tmp_user.id,
                                                dealer = mess.dealer)
                        # logging.info(f"{mess.get_user()} update event {mess.event_id}:  {new_event}")
                        update_base_event(mess.event_id, new_event)


                case "delete_event":
                    logging.info("delete event")

                    delete_base_event(mess.event_id)
                
                case _:
                    ## wrong message - set None user
                    mess.set_user()

            ## send user schedule as answer
            user_schedule = get_user_events(mess.get_user())
            
            client_in.put(user_schedule)
            ##print(f"\nMain() put: send schedule {user_schedule}")

        except Empty:
            ## in case no message from telegram
            ## free proccess time
            time.sleep(3)


if __name__ == "__main__":
    start_base_dispatcher()