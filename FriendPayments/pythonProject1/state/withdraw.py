from aiogram.fsm.state import State, StatesGroup

class Withdraw_Sum_State(StatesGroup):
    withdraw_sum = State()
    regCard = State()
    addName = State()

class Admin_State(StatesGroup):
    user_id = State()