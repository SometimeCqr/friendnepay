from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, WebAppInfo
from aiogram import Bot
from aiogram.types import Message
import datetime

def new_profile_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Приобрести тариф")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выберите действие ")

def prices_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Подписка 150₽", callback_data='first')
    kb.button(text="Подписка 650₽",callback_data='second')
    kb.button(text="Подписка 999₽",callback_data='third')
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def channels_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Канал", url="https://t.me/Friend_Pay")
    kb.button(text="Я подписался", callback_data='channel')
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def old_profile_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Мой профиль")
    kb.button(text="Пригласить друга")
    kb.button(text="Сменить тариф")
    kb.button(text="Кошелек")
    kb.button(text="Игра")
    kb.adjust(2,2,1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def expired_profile_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Мой профиль")
    kb.button(text="Пригласить друга")
    kb.button(text="Купить тариф")
    kb.button(text="Кошелек")
    kb.button(text="Игра")
    kb.adjust(2,2,1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
def withdraw_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Вывести деньги", callback_data='withdraw_start')
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def polite_kb():
    kb=ReplyKeyboardBuilder()
    kb.button(text="Согласен")
    kb.button(text="Не согласен")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def admin_withdraw_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Взяться за вывод",callback_data='admin_withdraw')
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def admin_kb():
    kb=ReplyKeyboardBuilder()
    kb.button(text="Мой профиль")
    kb.button(text="Пригласить друга")
    kb.button(text="Сменить тариф")
    kb.button(text="Кошелек")
    kb.button(text="Игра")
    kb.button(text="Начать работу")
    kb.button(text="Сумма балансов")
    kb.adjust(2,2,2,1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def admin_end_work_kb():
    kb=ReplyKeyboardBuilder()
    kb.button(text="Завершить работу")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
