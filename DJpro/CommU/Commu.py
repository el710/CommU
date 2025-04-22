"""
    Copyright (c) 2025 Kim Oleg <theel710@gmail.com>
"""

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

import logging

import asyncio
from threading import Thread

import queue


from django.core.management import execute_from_command_line

from telegram.telebot import telebot_start

from database.base_dispatcher import start_base_dispatcher



def run_thread_agent(target_function, *args, add_link=False):
    """
        Function runs <func> as daemon thread.
        if add_link set in True it makes up 
        conection by two queues: "in" thread & "out" thread
        Return: in/out queues or None
    """
    logging.info(f"function {target_function}; args {args}; add_link {add_link}")
    if add_link: 
        in_queue = queue.Queue()
        out_queue = queue.Queue()
        logging.info(f"got queues: {in_queue} - {out_queue}")

        # params = (in_queue, out_queue, *args)
        # logging.info(f"run_thread_agent(): thread arguments {params}")

        thread = Thread(target=target_function,
                        args=(in_queue, out_queue, *args),
                        daemon=True
                       )
    else:
        thread = Thread(target=target_function, args=args, daemon=True )

    try:
        thread.start()
    except Exception as exc:
        logging.info(f"exception at start - {exc}")
        raise Exception
    
    if add_link:
        return in_queue, out_queue
    
    return None


if __name__ == '__main__':
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CommU.settings')
    
    os.system('cls')
    print("Vivat Academia")

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: | %(module)s  %(funcName)s():   %(message)s") ##, filename="log.log")
    
    # start thread with telegram bot
    # telegram_link = run_thread_agent(telebot_start, add_link=True)
    # logging.info(f"got telegram bot link {telegram_link}")


    # run_thread_agent(start_base_dispatcher, *telegram_link)

    args = ['manage.py', 'runserver']
    execute_from_command_line(args)

    # input("wait...\n")



    logging.info("exit CommU")
    

