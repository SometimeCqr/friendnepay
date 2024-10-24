import re

from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from pythonProject1.state.withdraw import Withdraw_Sum_State, Admin_State
from pythonProject1.utils.database import Database
from pythonProject1.utils.function import check_status
from pythonProject1.keyboards.profile_kb import old_profile_kb, admin_withdraw_kb, expired_profile_kb, new_profile_kb, admin_kb
import os
from re import findall
async def start_admin(message: Message, state: FSMContext, bot:Bot):
    await bot.send_message(message.from_user.id,f"Введите id пользователя которому вы собираетесь перевести деньги")
    await state.set_state(Admin_State.user_id)

async def got_user_id(message: Message, state: FSMContext, bot:Bot):
    await state.update_data(userId=message.text)
    user_data = await state.get_data()
    user_id = user_data.get('userId')
    db = Database(os.getenv("DATABASE_NAME"))
    first_admin = os.getenv("ADMIN_ID_1")
    second_admin = os.getenv("ADMIN_ID_2")

async def start_withdraw(message: Message, state:FSMContext, bot:Bot):
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_id(message.from_user.id)
    admins_online_id = db.get_online_admins_id()
    status = await check_status(message, bot)
    if (admins_online_id == 0):
        if(user[2]==0): #тут нет проверки на нового пользователя так как он просто не попадет сюда
            await bot.send_message(message.from_user.id,
            f"На данный момент нет администраторов, которые могут произвести выплату. Попробуйте позже.",
            reply_markup=expired_profile_kb())
        else:
            if(user[9]==1):
                await bot.send_message(message.from_user.id, f"На данный момент нет администраторов, которые могут произвести выплату. Попробуйте позже.", reply_markup=admin_kb())
            else:
                await bot.send_message(message.from_user.id,f"На данный момент нет администраторов, которые могут произвести выплату. Попробуйте позже.",reply_markup=old_profile_kb())
        await state.clear()
    else:
        if(user[3]>=200):
            await bot.send_message(message.from_user.id,f'Введите сумму которую вы хотите вывести.\n'
                                                        f'Минимальная сумма 200 рублей.\n'
                                                        f'Введите "Отмена" если хотите вернуться в главное меню')
            await state.set_state(Withdraw_Sum_State.withdraw_sum)
        else:
            if(status==2):
                await bot.send_message(message.from_user.id,"У вас недостаточно средств на балансе.", reply_markup=expired_profile_kb())
            elif(status==3):
                await bot.send_message(message.from_user.id,"У вас недостаточно средств на балансе.", reply_markup=old_profile_kb())
            elif (status == 4 or status == 5):
                await bot.send_message(message.from_user.id, "У вас недостаточно средств на балансе.",
                                       reply_markup=admin_kb())


async def get_cards(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_id(message.from_user.id)
    if (re.findall('^\d+$', message.text)):
        if (user[3] >= int(message.text) and int(message.text) >= 200):
            await state.update_data(withdraw_sum=message.text)
            await bot.send_message(message.from_user.id, f'Запрос на вывод {message.text} рублей принят \n'
                                                             f'Введите номер телефона:\n'
                                                         f'Например +79231231212 или 89231231212\n'
                                                             f'Введите "Отмена" если хотите вернуться в главное меню')
            await state.set_state(Withdraw_Sum_State.regCard)
        elif (user[3] == 0):
            await bot.send_message(message.from_user.id, "У вас нет средств на балансе!",
                                   reply_markup=old_profile_kb())
            await state.clear()
        elif (int(message.text) < 200):
            await bot.send_message(message.from_user.id, f"Минимальная сумма вывода 200 рублей!\n"
                                                             f"Попробуйте снова\n"
                                                             f'Введите "Отмена" если хотите вернуться в главное меню')
            await state.set_state(Withdraw_Sum_State.withdraw_sum)
        else:
            await bot.send_message(message.from_user.id, f'Недостаточно средств на балансе!\n'
                                                             f'Попробуйте снова\n'
                                                             f'Введите "Отмена" если хотите вернуться в главное меню')
            await state.set_state(Withdraw_Sum_State.withdraw_sum)
    elif (message.text == 'Отмена' or message.text == "отмена"):
        if (user[2] == 0):
            await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=expired_profile_kb())
        else:
            if (user[9] == 1):
                await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=admin_kb())
            else:
                await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=old_profile_kb())
            await state.clear()
    else:
        await bot.send_message(message.from_user.id, "Неверный формат числа\n"
                                                         "Попробуйте еще раз.\n"
                                                         'Введите "Отмена" если хотите вернуться в главное меню')
        await state.set_state(Withdraw_Sum_State.withdraw_sum)
async def got_withdraw_sum(message: Message, state:FSMContext, bot:Bot):
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_id(message.from_user.id)
    admin_1 = db.select_user_id(os.getenv("ADMIN_1_ID"))
    admin_2 = db.select_user_id(os.getenv("ADMIN_2_ID"))
    if(re.findall('^(?:\+79|89)\d{9}$', message.text)):
        await state.update_data(reg_card=message.text)
        with_data = await state.get_data()
        with_sum = with_data.get('withdraw_sum')
        card = with_data.get('reg_card')
        await bot.send_message(message.from_user.id, "Принято! Теперь введите пожалуйста ваше имя фамилию и ваш банк\n"
                                                     "Пример: Иван Синицын Сбербанк\n"
                                                     'Введите "Отмена" если хотите вернуться в главное меню')
        await state.set_state(Withdraw_Sum_State.addName)
    elif (message.text == 'Отмена' or message.text == "отмена"):
        if(user[2]==0):
            await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=expired_profile_kb())
        else:
            if(user[9]==1):
                await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=admin_kb())
            else:
                await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=old_profile_kb())
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, 'Неверный формат номера попробуйте еще раз. Примеры ввода:\n'
                                                     '+71231231212\n'
                                                     '81231231212\n'
                                                     'Введите "Отмена" если хотите вернуться в главное меню')
        await state.set_state(Withdraw_Sum_State.regCard)

async def got_name(message: Message, state:FSMContext, bot:Bot):
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_id(message.from_user.id)
    if(message.text=="Отмена" or message.text == "отмена"):
        if (user[2] == 0):
            await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=expired_profile_kb())
        else:
            if (user[9] == 1):
                await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=admin_kb())
            else:
                await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=old_profile_kb())
        await state.clear()
    else:
        await state.update_data(regName=message.text)
        with_data = await state.get_data()
        with_sum = with_data.get('withdraw_sum')
        card = with_data.get('reg_card')
        name = with_data.get('regName')
        admins_online_id = db.get_online_admins_id()
        number_of_withdraws = db.select_number_of_withdraws()
        amount_admins_online = int(len(admins_online_id))
        new_number_withdraws = number_of_withdraws % amount_admins_online
        await bot.send_message(admins_online_id[new_number_withdraws], f'Запрошен вывод {with_sum} на номер {card} пользователем {name}')
        db.number_of_admin_withdraws_edit(admins_online_id[new_number_withdraws], db.select_user_id(admins_online_id[new_number_withdraws])[10]+1)
        db.sum_of_admin_withdraws_edit(admins_online_id[new_number_withdraws],db.select_user_id(admins_online_id[new_number_withdraws])[11] + int(with_sum))
        db.balance_edit(message.from_user.id, user[3] - int(with_sum))
        if (user[2] == 0):
            await bot.send_message(message.from_user.id, f'Ваш запрос принят! И будет выполнен админом номер {db.select_admin_id(admins_online_id[new_number_withdraws])[0]}\n'
                                                                 f'У вас осталось {user[3] - int(with_sum)} рублей',
                                    reply_markup=expired_profile_kb())
        else:
            if(user[9]==1):
                await bot.send_message(message.from_user.id,
                                         f'Ваш запрос принят! И будет выполнен админом номер {db.select_admin_id(admins_online_id[new_number_withdraws])[0]}\n'
                                         f'У вас осталось {user[3] - int(with_sum)} рублей',
                                        reply_markup=admin_kb())
            else:
                await bot.send_message(message.from_user.id, f'Ваш запрос принят! И будет выполнен админом номер {db.select_admin_id(admins_online_id[new_number_withdraws])[0]}\n'
                                                              f'У вас осталось {user[3] - int(with_sum)} рублей',
                                        reply_markup=old_profile_kb())
        db.numbers_of_withdraws_edit(int(number_of_withdraws) + 1, 1)
        await state.clear()