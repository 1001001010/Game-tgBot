from aiogram.dispatcher.filters.state import State, StatesGroup

class UsersCoupons(StatesGroup):
    here_coupon = State()
    
class UsersBet(StatesGroup):
    bet = State()
    type_bet = State()
    game = ()

class UsersGame(StatesGroup):
    bet = State()
    type_bet = State()
    game = State()
    msg = State()
    
class UserCube(StatesGroup):
    cube = State()
    type_bet = State()
    bet = State()
    
class UserPayment(StatesGroup):
    amount = State()
    method = State()