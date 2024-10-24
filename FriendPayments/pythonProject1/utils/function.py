import time
import datetime

from aiogram import Bot
from aiogram.types import Message
from pythonProject1.keyboards.profile_kb import prices_kb, withdraw_kb
from pythonProject1.keyboards.profile_kb import new_profile_kb, old_profile_kb,expired_profile_kb, polite_kb, admin_end_work_kb, admin_kb
from pythonProject1.utils.database import Database
import os



async def check_status(message:Message, bot:Bot): # Возвращает 0 при новом пользователе 1 при пользователе который есть в базе данных но без купленного когда либо тарифа 2 пользователь с просроченным тарифом, 3- есть тариф и он не просрочен, 4 - админ с просроченным тарифом, 5- админ с полноценным тарифом
    db = Database(os.getenv("DATABASE_NAME"))
    user = db.select_user_id(message.from_user.id)
    if(user):
        if(user[4]==0):
            return 0
        else:
            if(user[8] == 0):
                return 1
            else:
                user_sub = left_time(user[8])
                if(user_sub):
                    if(user[9]==1):
                        return 5
                    else:
                        return 3
                else:
                    db.pricing_edit(message.from_user.id, 0)
                    if(user[9]==1):
                        return 4
                    else:
                        return 2
    else:
        return 0

def check_today_time():
    db = Database(os.getenv("DATABASE_NAME"))
    time_now = int(time.time())
    left_time = time_now - int(db.get_today_const())
    if(left_time >= 24*60*60):
        delta_days = left_time // (24*60*60)
        delta_seconds = db.get_today_const() + delta_days * 24 * 60 * 60
        db.todays_const_edit(delta_seconds, 1)
        db.down_to_zero_all_number_referers()

async def subscribe_check(message:Message, bot:Bot): #Возвращает True если пользователь подписан на канал
    result = await bot.get_chat_member(chat_id='@testfaswdf', user_id=message.from_user.id)
    if (result.status == 'left'):
        return False
    else:
        return True

async def get_new_link(message: Message, bot:Bot):
    check_today_time()
    if(await subscribe_check(message,bot) == True):
        await bot.send_message(message.from_user.id, 'Этот бот предлагает пользователям возможность получать вознаграждение за приобретённые услуги другими пользователями, пользуясь ботом по вашей реферальной ссылке. Получая доступ к боту нашего сервиса или используя его, вы подтверждаете, что прочитали, поняли и согласны с настоящими Условиями.\nПользовательское соглашение https://telegra.ph/Polzovatelskoe-soglashenie-03-06-8',
                                reply_markup= new_profile_kb())


async def get_price(message: Message, bot:Bot):
    check_today_time()
    status = await check_status(message, bot)
    if(await subscribe_check(message,bot) == True):
        if (status != 0):
            await bot.send_message(message.from_user.id, 'Выберите тариф ', reply_markup=prices_kb())

async def wallet(message: Message, bot: Bot):
    check_today_time()
    status = await check_status(message,bot)
    if(await subscribe_check(message,bot) == True):
        if (status == 2 or status == 3 or status == 4 or status == 5):
            db = Database(os.getenv("DATABASE_NAME"))
            users = db.select_user_id(message.from_user.id)
            balance = users[3]
            await bot.send_message(message.from_user.id, f'Ваш баланс: {balance}', reply_markup=withdraw_kb())

async def change_pricing(message: Message, bot:Bot):
    check_today_time()
    status = await check_status(message, bot)
    if(await subscribe_check(message,bot) == True):
        if(status != 0):
            await bot.send_message(message.from_user.id, 'Выберите тариф ', reply_markup=prices_kb())

async def back(message: Message, bot:Bot):
    check_today_time()
    status = await check_status(message, bot)
    if(await subscribe_check(message,bot) == True):
        if(status == 0):
            await bot.send_message(message.from_user.id, 'Недостаточно прав')
        elif(status == 1):
            await bot.send_message(message.from_user.id, 'Чем могу помочь?',reply_markup=new_profile_kb())
        elif(status == 2):
            await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=expired_profile_kb())
        elif (status == 3):
            await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=old_profile_kb())
        elif (status == 4 or status ==5):
            await bot.send_message(message.from_user.id, "Чем могу помочь?", reply_markup=admin_kb())

async def agree(message: Message, bot:Bot):
    check_today_time()
    db = Database(os.getenv("DATABASE_NAME"))
    db.polite_edit(message.from_user.id, 1)
    await bot.send_message(message.from_user.id, 'Чем могу помочь?', reply_markup=new_profile_kb())

async def disagree(message: Message, bot:Bot):
    check_today_time()
    await bot.send_message(message.from_user.id, 'Бот не может продолжить свою работу пока вы не согласитесь с настоящими Условиями.\nПользовательское соглашение https://telegra.ph/Polzovatelskoe-soglashenie-03-06-8', reply_markup=polite_kb())

async def create_link(message: Message, bot:Bot):
    check_today_time()
    status = await check_status(message, bot)
    if (status == 0):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!")
    elif (status == 1):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!", reply_markup=new_profile_kb())
    elif (status == 2):
        await bot.send_message(message.from_user.id, "Сначала нужно приобрести тариф!",
                               reply_markup=expired_profile_kb())
    else:
        if(await subscribe_check(message,bot) == True):
            if(status==3):
                await bot.send_message(message.from_user.id, f'Ваша реферальная ссылка: \n'
                                                                             f'https://t.me/{os.getenv("BOT_NAME")}?start={message.from_user.id} \n'
                                                                         f'Важная информация! \n'
                                                                         f'Реферальная система работает только на новых пользователей. Если по ней перейдет пользователь, который уже приобрел тариф, ничего не произойдёт.',reply_markup=old_profile_kb())

            elif(status==4 or status == 5):
                await bot.send_message(message.from_user.id, f'Ваша реферальная ссылка: \n'
                                                                    f'https://t.me/{os.getenv("BOT_NAME")}?start={message.from_user.id} \n'
                                                                    f'Важная информация! \n'
                                                                    f'Реферальная система работает только на новых пользователей. Если по ней перейдет пользователь, который уже приобрел тариф, ничего не произойдёт.',
                                            reply_markup=admin_kb())

async def my_profile(message: Message, bot: Bot):
    check_today_time()
    status = await check_status(message, bot)
    if (status == 0):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!")
    elif (status == 1):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!", reply_markup=new_profile_kb())
    else:
        if(await subscribe_check(message,bot) == True):
            db = Database(os.getenv("DATABASE_NAME"))
            user = db.select_user_id(message.from_user.id)
            referer_amount = user[6]
            user_sub = left_time(user[8])
            if (status == 2):
                await bot.send_message(message.from_user.id, f'Количество рефералов: {referer_amount} \n'
                                                         f'Количество попыток в игре: {user[7]} \n'
                                                         f'У вас нет тарифа!', reply_markup=expired_profile_kb())
            elif(status == 3):
                await bot.send_message(message.from_user.id, f'Количество рефералов: {referer_amount} \n'
                                                                f'Количество попыток в игре: {user[7]} \n'
                                                                f'До конца тарифа осталось: {user_sub}',reply_markup=old_profile_kb())
            elif (status == 4):
                await bot.send_message(message.from_user.id, f'Количество рефералов: {referer_amount} \n'
                                                                f'Количество попыток в игре: {user[7]} \n'
                                                                f'У вас нет тарифа',reply_markup=admin_kb())
            elif (status == 5):
                await bot.send_message(message.from_user.id, f'Количество рефералов: {referer_amount} \n'
                                                                f'Количество попыток в игре: {user[7]} \n'
                                                                f'До конца тарифа осталось: {user_sub}',reply_markup=admin_kb())




async def minigame(message: Message, bot: Bot):
    check_today_time()
    status = await check_status(message, bot)
    if (status == 0):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!")
    elif (status == 1):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!", reply_markup=new_profile_kb())
    elif (status == 2):
        await bot.send_message(message.from_user.id, "Сначала нужно приобрести тариф!",
                               reply_markup=expired_profile_kb())
    elif (status == 4):
        await bot.send_message(message.from_user.id, "Сначала нужно приобрести тариф!",
                               reply_markup=admin_kb())
    else:
        if(await subscribe_check(message,bot) == True):
            db = Database(os.getenv("DATABASE_NAME"))
            user = db.select_user_id(message.from_user.id)
            if(user[7]!=0):
                if(status==3):
                    result: Message = await bot.send_dice(message.chat.id, emoji='🎰', reply_markup=old_profile_kb())
                elif(status==5):
                    result: Message = await bot.send_dice(message.chat.id, emoji='🎰', reply_markup=admin_kb())
                if (result.dice.value == 1 or result.dice.value == 22 or result.dice.value == 43):
                    await bot.send_message(message.from_user.id, f'Вы выиграли дополнительную попытку!\n'
                                                            f'Количество оставшихся попыток: {user[7]}')
                    db.attempts_edit(message.from_user.id, user[7] - 1) #ДОБАВЛЕНО ДЛЯ ТЕСТА СКОЛЬКО УХОДИТ ПОПЫТОК. ДЛЯ НОРМАЛЬНОЙ РАБОТЫ УБРАТЬ ЭТУ СТРОКУ
                elif (result.dice.value == 64):
                    db.balance_edit(message.from_user.id, user[3] + 2000)
                    db.attempts_edit(message.from_user.id, user[7] - 1)
                    await bot.send_message(message.from_user.id, f'Вы выиграли 2000!\n'
                                                                f'Количество оставшихся попыток: {user[7]-1}')
                else:
                    db.attempts_edit(message.from_user.id, user[7]-1)
                    await bot.send_message(message.from_user.id, f'Количество оставшихся попыток: {user[7]-1}')
            else:
                if(status==3):
                    await bot.send_message(message.from_user.id, f'У вас закончились попытки',reply_markup=old_profile_kb())
                elif(status==5):
                    await bot.send_message(message.from_user.id, f'У вас закончились попытки',reply_markup=admin_kb())



def days_to_seconds(days):
    return days * 24 * 60 * 60

def left_time(seconds):
    time_now = int(time.time())
    left_time = int(seconds) - time_now
    if(left_time <= 0):
        return False
    else:
        dt = str(datetime.timedelta(seconds=left_time))
        dt = dt.replace("days", "дней")
        dt = dt.replace("day", "день")
        return dt

async def start_work(message:Message, bot:Bot):
    check_today_time()
    status = await check_status(message, bot)

    if (status == 0):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!")
    elif (status == 1):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!", reply_markup=new_profile_kb())
    elif (status == 2):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!",
                               reply_markup=expired_profile_kb())
    elif (status == 3):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!",
                               reply_markup=old_profile_kb())
    elif(status==4 or status == 5):
        db = Database(os.getenv("DATABASE_NAME"))
        user = db.select_user_id(message.from_user.id)
        await bot.send_message(message.from_user.id, "Вы в онлайне!", reply_markup=admin_end_work_kb())
        db.is_online_edit(message.from_user.id,1)
        db.number_of_admin_withdraws_edit(message.from_user.id, 0)
        db.sum_of_admin_withdraws_edit(message.from_user.id, 0)


async def stop_work(message:Message, bot:Bot):
    check_today_time()
    status = await check_status(message, bot)
    if (status == 0):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!")
    elif (status == 1):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!", reply_markup=new_profile_kb())
    elif (status == 2):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!",
                               reply_markup=expired_profile_kb())
    elif (status == 3):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!",
                               reply_markup=old_profile_kb())
    elif(status==4 or status == 5):
        db = Database(os.getenv("DATABASE_NAME"))
        user = db.select_user_id(message.from_user.id)
        if(user[10]==0):
            await bot.send_message(message.from_user.id,f"Вы приняли 0 выводов средств. Суммарно вы вывели 0.",reply_markup=admin_kb())
        elif(user[10]==1):
            await bot.send_message(message.from_user.id,
                                f"Вы приняли {user[10]} вывод средств. Суммарно вы вывели {user[11]}!",
                                reply_markup=admin_kb())
        else:
            await bot.send_message(message.from_user.id, f"Вы приняли {user[10]} выводов средств. Суммарно вы вывели {user[11]}! Хорошая работа!", reply_markup=admin_kb())
        db.is_online_edit(message.from_user.id, 0)
        db.number_of_admin_withdraws_edit(message.from_user.id, 0)
        db.sum_of_admin_withdraws_edit(message.from_user.id, 0)


async def get_balances_sum(message:Message, bot:Bot):
    check_today_time()
    status = await check_status(message, bot)
    if (status == 0):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!")
    elif (status == 1):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!", reply_markup=new_profile_kb())
    elif (status == 2):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!",
                               reply_markup=expired_profile_kb())
    elif (status == 3):
        await bot.send_message(message.from_user.id, "У вас недостаточно прав!",
                               reply_markup=old_profile_kb())
    elif(status==4 or status == 5):
        db = Database(os.getenv("DATABASE_NAME"))
        user = db.select_user_id(message.from_user.id)
        await bot.send_message(message.from_user.id, f"Всего на балансе у пользователей {db.get_balances_sum()}₽", reply_markup=admin_kb())
