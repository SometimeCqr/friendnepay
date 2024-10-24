from aiogram import Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from pythonProject1.keyboards.profile_kb import  old_profile_kb, new_profile_kb
from pythonProject1.utils.function import days_to_seconds, left_time
import os
import time
import datetime

from pythonProject1.utils.database import Database


async def get_first_payment(call: CallbackQuery):
    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title='Покупка первого тарифа',
        description='Покупка первого тарифа',
        provider_token=os.getenv("PAYMENT_TOKEN"),
        payload='first',
        currency='rub',
        prices=[
            LabeledPrice(
                label='Покупка тарифа за 150 рублей',
                amount=15000
            )
        ],
        start_parameter='friendpaymentsbot',
        provider_data=None,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        reply_markup=None,
        request_timeout=60
    )

async def get_second_payment(call: CallbackQuery):
    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title='Покупка второго тарифа',
        description='Покупка второго тарифа',
        provider_token=os.getenv("PAYMENT_TOKEN"),
        payload='second',
        currency='rub',
        prices=[
            LabeledPrice(
                label='Покупка тарифа за 650 рублей',
                amount=65000
            )
        ],
        start_parameter='friendpaymentsbot',
        provider_data=None,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        reply_markup=None,
        request_timeout=60
    )

async def get_third_payment(call: CallbackQuery):
    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title='Покупка третьего тарифа',
        description='Покупка третьего тарифа',
        provider_token=os.getenv("PAYMENT_TOKEN"),
        payload='third',
        currency='rub',
        prices=[
            LabeledPrice(
                label='Покупка тарифа за 999 рублей',
                amount=99900
            )
        ],
        start_parameter='friendpaymentsbot',
        provider_data=None,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        reply_markup=None,
        request_timeout=60
    )

async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot:Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    print(pre_checkout_query)

async def success_payment(message:Message, bot:Bot):
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_id(message.from_user.id)

    #Проверка на наличие реферала и начисление ему суммы если таковой есть
    if(user[5] != 0):
        user_referer = db.select_user_id(user[5])
        user_referer_sub = left_time(user_referer[8])
        if(user_referer_sub): #Проверка на просроченность тарифа человека который выдал реферальную ссылку(если у него нет тарифа то user_referer_sub будет по прежнему False)
            new_referer_balance = user_referer[3]
            new_referer_attemts = user_referer[7]
            if (message.successful_payment.total_amount == 15000):
                new_referer_balance = user_referer[3] + 100
                new_referer_attemts = user_referer[7] + 1
            elif (message.successful_payment.total_amount == 65000):
                if (user_referer[2] == 1):
                    new_referer_balance = user_referer[3] + 100
                    new_referer_attemts = user_referer[7] + 1
                else:
                    new_referer_balance = user_referer[3] + 500
                    new_referer_attemts = user_referer[7] + 2
            elif (message.successful_payment.total_amount == 99900):
                if (user_referer[2] == 1):
                    new_referer_balance = user_referer[3] + 100
                    new_referer_attemts = user_referer[7] + 1
                elif(user_referer[2]==2):
                    new_referer_balance = user_referer[3] + 500
                    new_referer_attemts = user_referer[7] + 2
                else:
                    new_referer_balance = user_referer[3] + 800
                    new_referer_attemts = user_referer[7] + 3
            db.balance_edit(user[5], new_referer_balance)
            db.attempts_edit(user[5], new_referer_attemts)
        else:
            db.pricing_edit(user[5], 0)

    #Обработка покупки тарифа для самого покупателя
    balance = user[2] + message.successful_payment.total_amount // 100
    if(message.successful_payment.total_amount==15000):
        db.pricing_edit(message.from_user.id,1)
        db.attempts_edit(message.from_user.id, 1)
        timesub = int(time.time()) + days_to_seconds(31)
    elif(message.successful_payment.total_amount==65000):
        db.pricing_edit(message.from_user.id,2)
        db.attempts_edit(message.from_user.id, 2)
        timesub = int(time.time()) + days_to_seconds(90)
    elif(message.successful_payment.total_amount==99900):
        db.pricing_edit(message.from_user.id,3)
        db.attempts_edit(message.from_user.id, 3)
        timesub = int(time.time()) + days_to_seconds(180)
 #Получение времени покупки тарифа в секундах
    db.timesub_edit(message.from_user.id, timesub)


    await bot.send_message(message.from_user.id, 'Оплата прошла успешно!', reply_markup=old_profile_kb())

