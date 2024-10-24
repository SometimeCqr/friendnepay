from aiogram import Bot, Dispatcher, F
import asyncio
import os
from dotenv import load_dotenv


from state.withdraw import Withdraw_Sum_State, Admin_State
from utils.commands import set_commands
from utils.function import get_new_link, get_price,wallet,  change_pricing,back,agree, disagree,create_link, my_profile, minigame,start_work,stop_work,get_balances_sum
from handlers.start import get_start, start_subscriber
from handlers.payment import get_first_payment,success_payment,process_pre_checkout_query,get_second_payment,get_third_payment
from handlers.withdraw import start_withdraw, got_withdraw_sum, get_cards, start_admin, got_user_id, got_name
from aiogram.filters import Command



load_dotenv()

#6772011586:AAG5f70HOk5Up9dbZb4T-AsZ5x4K8tgmV2E старый токен настоящего бота
token = '6109727813:AAHfbeVBjA25HV1Qok79iJhKitGAJzWNZ20'
admin_id = os.getenv('ADMIN_ID_1')

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher()

dp.callback_query.register(start_withdraw,F.data.startswith('withdraw_start'))
dp.message.register(got_withdraw_sum, Withdraw_Sum_State.regCard)
dp.message.register(get_cards, Withdraw_Sum_State.withdraw_sum)
dp.message.register(got_name, Withdraw_Sum_State.addName)

dp.message.register(got_user_id, Admin_State.user_id)


dp.message.register(get_start, Command(commands='start'))
dp.message.register(get_price, F.text=='Приобрести тариф')
dp.message.register(get_new_link, F.text=='Инструкция использования')
dp.message.register(create_link, F.text=='Пригласить друга')
dp.message.register(start_work, F.text=='Начать работу')
dp.message.register(stop_work, F.text=='Завершить работу')
dp.message.register(my_profile, F.text=='Мой профиль')
dp.message.register(get_balances_sum, F.text=='Сумма балансов')
dp.message.register(back, F.text=='Назад')
dp.message.register(minigame, F.text=="Игра")
dp.message.register(agree, F.text=='Согласен')
dp.message.register(disagree, F.text=='Не согласен')
dp.message.register(wallet, F.text=='Кошелек')
dp.callback_query.register(start_admin, F.data.startswith('admin_withdraw'))
dp.message.register(change_pricing, F.text=='Сменить тариф')
dp.message.register(change_pricing, F.text=='Купить тариф')
dp.callback_query.register(start_subscriber, F.data.startswith('channel'))
dp.callback_query.register(get_first_payment, F.data.startswith('first'))
dp.callback_query.register(get_second_payment, F.data.startswith('second'))
dp.callback_query.register(get_third_payment, F.data.startswith('third'))
dp.pre_checkout_query.register(process_pre_checkout_query)
dp.message.register(success_payment, F.successful_payment)
async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot,skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())