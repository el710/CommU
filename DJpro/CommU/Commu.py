#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import logging

import asyncio
from threading import Thread
import time
import queue
from queue import Empty

from django.core.management import execute_from_command_line

from telegram.telebot import telebot_start
from telegram.bot_api import TMessage, get_user_events

from data.data import CreateUser, CreateEvent
from database.db import (create_base_user, read_base_user,
                         create_base_event, update_base_event, 
                         delete_base_event)


def run_thread_agent(func, add_link: bool=False):
    """
        Function runs <func> as daemon thread.
        if add_link set in True it makes up 
        conection by two queues: "in" thread & "out" thread
        Return: in/out queues or None
    """
    if add_link: 
        in_queue = queue.Queue()
        out_queue = queue.Queue()
        thread = Thread(target=func,
                        args=[in_queue, out_queue],
                        daemon=True
                       )
    else:
        thread = Thread(target=func, daemon=True )

    try:
        thread.start()
    except Exception as exc:
        print(f"run_thread_agent: exception {exc}")
        raise Exception
    
    if add_link:
        return {"in": in_queue, "out": out_queue}
    
    return None

def django_pro_start():
    args = ['manage.py', 'runserver']
    execute_from_command_line(args)


if __name__ == '__main__':
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CommU.settings')
    
    os.system('cls')
    print("Vivat Academia")

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: | %(module)s     %(message)s",
                        filename="log.log")
    
    # start thread with telegram bot
    telegram_link = run_thread_agent(telebot_start, add_link=True)

    run_thread_agent(django_pro_start)

    user_schedule = {}
        
    # main work cycle
    while True:
        # print("Main(): wait...")
        try:
            event_query = telegram_link["out"].get(timeout=1)
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
            
            telegram_link["in"].put(user_schedule)
            ##print(f"\nMain() put: send schedule {user_schedule}")

        except Empty:
            ## in case no message from telegram
            ## free proccess time
            time.sleep(3)




    logging.info("exit CommU")
    

