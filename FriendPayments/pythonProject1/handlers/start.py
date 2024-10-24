from aiogram import Bot
from aiogram.types import Message
from pythonProject1.keyboards.profile_kb import new_profile_kb, old_profile_kb,expired_profile_kb, channels_kb, polite_kb, admin_kb
from pythonProject1.utils.database import Database
from pythonProject1.utils.function import left_time, check_today_time
import os

async def get_start(message: Message, bot:Bot):
    check_today_time()
    db = Database(os.getenv("DATABASE_NAME"))
    users = db.select_user_id(message.from_user.id)
    result = await bot.get_chat_member(chat_id='@testfaswdf', user_id=message.from_user.id)
    # Проверка на наличие пользователя в базе данных
    if (users):
        if(users[9] == 1): #Проверка на админа
            await bot.send_message(message.from_user.id, "Чем могу помочь админ?", reply_markup=admin_kb())
        else:
            user_polite = users[4]
            # Проверка политики конфиденциальности
            if (user_polite==0):
                await bot.send_message(message.from_user.id,
                                       'Этот бот предлагает пользователям возможность получать вознаграждение за приобретённые услуги другими пользователями, пользуясь ботом по вашей реферальной ссылке. Получая доступ к боту нашего сервиса или используя его, вы подтверждаете, что прочитали, поняли и согласны с настоящими Условиями.\nПользовательское соглашение https://telegra.ph/Polzovatelskoe-soglashenie-03-06-8',
                                       reply_markup=polite_kb())
            # Сюда мы попадаем если пользователь согласился с  политикой конфиденциальности
            else:
                pricing = users[2]
                # Проверка подписки на канал
                if (result.status == 'left'):
                    await bot.send_message(message.from_user.id, 'Вы не подписаны на канал', reply_markup=channels_kb())
                else:
                    #Проверка есть ли у пользователя тариф
                    if(pricing!=0):
                        if (left_time(users[8])):  # Проверка тарифа на просроченность
                            await bot.send_message(message.from_user.id, 'Чем могу помочь?', reply_markup=old_profile_kb())
                        else:  # Сюда мы попадем если у пользователя просрочился тариф
                            db.pricing_edit(message.from_user.id, 0)
                            await bot.send_message(message.from_user.id, "Время действия вашей подписки истекло.",reply_markup=expired_profile_kb())
                    else:
                        #Проверка перед нами пользователь с просроченным тарифом или новый
                        if(users[8]==0):
                            #Добавление id реферала в базу данных
                            referer_id = str(message.text[7:])
                            if (referer_id and referer_id!=users[2]):
                                referer = db.select_user_id(referer_id)
                                if(referer):
                                    if(referer[12]<15):
                                        db.referer_edit(message.from_user.id, int(referer_id))
                                        referer = db.select_user_id(referer_id)
                                        new_referer_amount = referer[6] + 1
                                        new_today_referer_amount = referer[12] + 1
                                        db.referer_amount_edit(referer_id, new_referer_amount)
                                        db.number_of_referers_today_edit(referer_id, new_today_referer_amount)
                                    else:
                                        await bot.send_message(message.from_user.id, "Исчерпан ежедневный лимит приглашений по данной ссылке.")
                                else:
                                    await bot.send_message(message.from_user.id, f"Неверная реферальная ссылка")
                            await bot.send_message(message.from_user.id, 'Чем могу помочь?', reply_markup=new_profile_kb())
                        else:
                            await bot.send_message(message.from_user.id, 'Чем могу помочь?', reply_markup=expired_profile_kb())
    #Перед нами новый пользователь
    else:
        if(message.text):
            #При подписке на канал вызывается функция старт и если не сделать эту проверку вызывается ошибка так как "Я подписался" инлайн кнопка
            referer_id = str(message.text[7:])
            #Добавление id реферала
            if (referer_id):
                db = Database(os.getenv("DATABASE_NAME"))
                referer = db.select_user_id(referer_id)
                if(referer):
                    if(referer[12]<15):
                        db.add_user(message.from_user.id)
                        db.referer_edit(message.from_user.id, int(referer_id))
                        new_referer_amount = referer[6] + 1
                        new_referer_today_amount = referer[12] + 1
                        db.referer_amount_edit(referer_id, new_referer_amount)
                        db.number_of_referers_today_edit(referer_id,new_referer_today_amount)
                        await bot.send_message(message.from_user.id,
                                               'Этот бот предлагает пользователям возможность получать вознаграждение за приобретённые услуги другими пользователями, пользуясь ботом по вашей реферальной ссылке. Получая доступ к боту нашего сервиса или используя его, вы подтверждаете, что прочитали, поняли и согласны с настоящими Условиями.\nПользовательское соглашение https://telegra.ph/Polzovatelskoe-soglashenie-03-06-8',
                                            reply_markup=polite_kb())
                    else:
                        await bot.send_message(message.from_user.id, "Исчерпан ежедневный лимит приглашений по данной ссылке.")
                else:
                    await bot.send_message(message.from_user.id, f"Неверная реферальная ссылка")
            else:
                await bot.send_message(message.from_user.id, "Регистрация в боте возможна только по реферальной ссылке!")


async def start_subscriber(message:Message,bot:Bot): #Функция старт после нажатия "Я подписался на канал"
    check_today_time()
    result = await bot.get_chat_member(chat_id='@testfaswdf', user_id=message.from_user.id)
    db = Database(os.getenv("DATABASE_NAME"))
    users = db.select_user_id(message.from_user.id)
    if (result.status == 'left'): #Проверка подписки на канал
        await bot.send_message(message.from_user.id, 'Вы не подписаны на канал', reply_markup=channels_kb())
    else:
        if(users[2]!=0): # Тут идут проверки на то, кто перед нами: новый юзер старый юзер или юзер с просроченным тарифом
            await bot.send_message(message.from_user.id, 'Чем могу помочь?', reply_markup=old_profile_kb())
        else:
            if(users[8]!=0):
                await bot.send_message(message.from_user.id, 'Чем могу помочь?', reply_markup=expired_profile_kb())
            else:
                await bot.send_message(message.from_user.id, 'Чем могу помочь?', reply_markup=new_profile_kb())