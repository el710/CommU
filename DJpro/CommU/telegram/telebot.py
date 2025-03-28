"""
    Copyright (c) 2024 Kim Oleg <theel710@gmail.com>
"""
"""
    Telegram bot module
"""
import os, sys

## basic...
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram.fsm.storage.memory import MemoryStorage

## for get <state>... to get, keep & use data of users
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

## outline menu buttons
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

## inline menu buttons
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram import F

import asyncio
import queue
import json

import logging

from .id_commu_bot import tel_token

from .telegramuser import TelegramUser    


text_button_sched = "Расписание"
text_button_add = "Добавить"
button_sched = KeyboardButton(text=text_button_sched)
button_add = KeyboardButton(text=text_button_add)
out_main_keyboard = ReplyKeyboardMarkup(keyboard=[[button_sched, button_add], ], resize_keyboard=True)
# out_main_keyboard. add(button_sched)
# out_main_keyboard.add(button_add)

text_button_cancel = "Отменить"
button_cancel = KeyboardButton(text=text_button_cancel)
out_cancel_menu = ReplyKeyboardMarkup(keyboard=[[button_cancel], ], resize_keyboard=True)
# out_cancel_menu.add(button_cancel)


# posts_query = CallbackData('button', 'button_id', 'action')

class EventCallBack(CallbackData, prefix="event"):
    user_id: int
    event_id: str

async def init_schedule_keyboard(events_list):
    # schedule = InlineKeyboardMarkup(row_width=1)
    schedule = InlineKeyboardBuilder()
    # print(f"init(): {events_list}")

    for event in events_list:
        # button = InlineKeyboardButton(f' {event["time"]} ({event["dealer"]}): {event["description"]}', callback_data=posts_query.new(button_id=str(event["event_id"]), action='push'))
        # schedule.insert(button)
        schedule.button(
            text=f' {event["time"]} ({event["dealer"]}): {event["description"]}',
            callback_data=EventCallBack(user_id=0, event_id=event['event_id']), 
        )    

    return schedule

# text_button_edit = "Изменить"
# text_button_delete = "Удалить"
# button_edit = InlineKeyboardButton(text_button_edit, callback_data='edit')
# button_delete = InlineKeyboardButton(text_button_delete, callback_data="delete")
# event_callback = CallbackData('event', 'id', 'action')

# async def init_event_keyboard(user_id, event_num):
#     event_menu = InlineKeyboardMarkup()
#     button_edit = InlineKeyboardButton(text_button_edit, callback_data=event_callback.new(id=f"{user_id}-{event_num}", action='edit'))
#     button_delete = InlineKeyboardButton(text_button_delete, callback_data=event_callback.new(id=f"{user_id}-{event_num}", action='delete'))

#     event_menu.insert(button_edit)
#     event_menu.insert(button_delete)
    
#     return event_menu

class MakeEvent(StatesGroup):
    date = State()
    time = State()
    dealer = State()
    description = State()

"""
    make dispetcher
"""

# dp = Dispatcher(bot, storage=MemoryStorage())
dp = Dispatcher(storage=MemoryStorage())

_main_queue = None
        
"""
    Handler for commands... </comm>
"""

"""
    Main menu
"""
@dp.message(F.text==text_button_sched)
async def show_schedule(message):
    """
        Show user's schedule  in keyboard style
    """
    t_user = TelegramUser.get_user(message)
    if t_user.login:
        await t_user.read_event()
        if t_user.schedule:
            schedule_menu = await init_schedule_keyboard(t_user.schedule)
            await message.answer(f"Сегодня:", reply_markup=schedule_menu)
        else:
            await message.answer(f"Сегодня событий не найдено:", reply_markup=out_main_keyboard)
    else:
        await message.answer(f"try /start...")


# """
#     Start new deal event State Machine
# """
# @dp.message_handler(text=text_button_add)
# async def start_new_event(message):
#     t_user = TelegramUser.get_user(message)
#     if t_user.login:
#         """
#            start StateMachine for new deal event
#         """
#         await message.answer(f"Укажите контакт: ", reply_markup = out_cancel_menu)
#         await MakeEvent.dealer.set()
#     else:
#         await message.answer(f"try /start...")

# @dp.message_handler(state=MakeEvent.dealer)
# async def get_event_dealer(message, state):
#     t_user = TelegramUser.get_user(message)
#     if t_user.login:
#         """
#            set deal event - start description
#         """
#         if message.text == text_button_cancel:
#            await message.answer(f"добавление отменено", reply_markup=out_main_keyboard)
#            await state.finish()
#         else:
#             await state.update_data(dealer=message.text)
#             await message.answer(f"Опишите событие: ", reply_markup = out_cancel_menu)
#             await MakeEvent.description.set()
#     else:
#         await message.answer(f"try /start...")

# @dp.message_handler(state=MakeEvent.description)
# async def get_event_description(message, state):
#     t_user = TelegramUser.get_user(message)
#     if t_user.login:
#         """
#            set description - start data
#         """
#         if message.text == text_button_cancel:
#            await message.answer(f"добавление отменено", reply_markup=out_main_keyboard)
#            await state.finish()
#         else:
#             await state.update_data(description=message.text)
#             await message.answer(f"Укажите дату: ", reply_markup = out_cancel_menu)
#             await MakeEvent.date.set()
#     else:
#         await message.answer(f"try /start...")

# @dp.message_handler(state=MakeEvent.date)
# async def get_event_date(message, state):
#     t_user = TelegramUser.get_user(message)
#     if t_user.login:
#         """
#            set date - start time
#         """
#         if message.text == text_button_cancel:
#            await message.answer(f"добавление отменено", reply_markup=out_main_keyboard)
#            await state.finish()
#         else:
#             await state.update_data(date=message.text)
#             await message.answer(f"Укажите время: ", reply_markup = out_cancel_menu)
#             await MakeEvent.time.set()
#     else:
#         await message.answer(f"try /start...")

# @dp.message_handler(state=MakeEvent.time)
# async def get_event_time(message, state):
#     t_user = TelegramUser.get_user(message)
#     if t_user.login:
#         """
#            set time - end machine
#         """
#         if message.text == text_button_cancel:
#            await message.answer(f"добавление отменено", reply_markup=out_main_keyboard)
#            await state.finish()
#         else:
#             await state.update_data(time=message.text)
#             data = await state.get_data()                       
#             """
#                 CREATE: send new event to main
#             """
#             if await t_user.create_event(**data):
#                 await message.answer("Новое событие: отправлено...", reply_markup=out_main_keyboard)
#             else:
#                 await message.answer("Новое событие: не отправлено...", reply_markup=out_main_keyboard)

#             await state.finish() 
#     else:
#         await message.answer(f"try /start...")

# """
#     Events handler
# """

# @dp.callback_query(posts_query.filter(action='push'))
# async def open_event(call):
#     """
#         Work with Event
#     """
#     user_id = call.from_user['id']
#     t_user = TelegramUser.find_user(user_id)

#     if t_user:
#         event_id = int(call.data.split(":")[1])
#         event_menu = await init_event_keyboard(user_id, event_id)

#         event = None    
#         for item in t_user.schedule:
#             if item["event_id"] == event_id:
#                 event = item 
        
#         if event:
#             await call.message.answer(f'''
#                                       id: {event_id} контакт: {event["dealer"]}\n
#             время: {event["time"]}\n
#             событие: {event["description"]}
#                                       ''', reply_markup = event_menu)
#         else:
#             await call.message.answer(f" событие не найдено", reply_markup = out_main_keyboard)


#     await call.answer()
    
# @dp.callback_query(event_callback.filter(action='edit'))
# async def edit_event(call):
#     """
#         Edit Event
#     """
#     user_id = call.from_user['id']
#     t_user = TelegramUser.find_user(user_id)
#     if t_user:
#         id_data = call.data.split(":")[1]
#         event_id = id_data.split("-")[1]

#         # logging.info(f"edit_event(): event: {event_id}")

#         params = {"event_id": event_id,
#                   "date": "date",
#                   "time": "time",
#                   "dealer": "dealer",
#                   "description": "desc"
#                 }
#         # logging.info(f"edit_event(): message: {params}")

#         if await t_user.update_event(**params):
#             await call.message.answer(f"User: {user_id} - event: {event_id} отправлено", reply_markup=out_main_keyboard)
#         else:
#             await call.message.answer(f"User: {user_id} - event: {event_id} не отправлено", reply_markup=out_main_keyboard)

#     await call.answer()

# @dp.callback_query_handler(event_callback.filter(action='delete'))
# async def delete_event(call):
#     """
#         Delete Event
#     """
#     user_id = call.from_user['id']
#     t_user = TelegramUser.find_user(user_id)
#     if t_user:
#         id_data = call.data.split(":")[1]
#         event_id = id_data.split("-")[1]
#         if await t_user.delete_event(event_id):
#             await call.message.answer(f"User: {user_id} - event: {event_id} отправлено", reply_markup=out_main_keyboard)
#         else:
#             await call.message.answer(f"User: {user_id} - event: {event_id} не отправлено", reply_markup=out_main_keyboard)
        
#     await call.answer()

# @dp.message_handler(commands=['start'])
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    """
        Login new user
    """
    user_id = message.from_user.id
    logging.info(f"command_start_handler(): user: {user_id}")
    
    t_user = TelegramUser.get_user(message)
    
    if not t_user.login:
        await message.answer(f"Hello {t_user.firstname} {t_user.lastname}! Nice to see you", reply_markup=out_main_keyboard)
        await t_user.activate()
    else:
        await message.answer(f"use menu...", reply_markup=out_main_keyboard)    

    # await message.answer(f"Hello, {message.from_user.full_name}!")


@dp.message()
async def all_message(message: Message):
   """
        handler for unexpected messages
   """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`

   await command_start_handler(message)
#    await message.answer(f"Hello, {message.from_user.full_name}! Use '/start' command...")


async def botloop():
    """
        Main cycle for bot dispatcher
    """

    bot = Bot(token=tel_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    while True:
        # await dp.start_polling() ## 2.0
        await dp.start_polling(bot)
        # dp.run_polling(bot)

        logging.info("start_polling has ended...")

        asyncio.sleep(0.1)

def telebot_start(*args):
    """
        Telegram bot thread
    """
    
    TelegramUser.set_queue(args[0], args[1])
    
    try:
        asyncio.run(botloop())
    except Exception as e:
        print(f"Error: {e}")
    
if __name__ == "__main__":
    print("telegram bot...")
    
    
    
    