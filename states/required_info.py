from telebot.handler_backends import State, StatesGroup


class UserInfoLow(StatesGroup):
     command = State()
     city = State()
     location_id = State()
     hotel_amt = State()
     date_arrival = State()
     date_depature = State()
     photo_amt = State()

class UserInfoSurvey(StatesGroup):
     command = State()
     city = State()
     location_id = State()
     hotel_amt = State()
     date_arrival = State()
     date_depature = State()
     photo_amt = State()

class UserInfoBest(StatesGroup):
     command = State()
     city = State()
     location_id = State()
     min_price = State()
     max_price = State()
     date_arrival = State()
     date_depature = State()
     hotel_amt = State()
     max_distance = State()
     photo_amt = State()

class UserInfoState(StatesGroup):
     country = State()
     city = State()
     check_in_date = State()
     check_out_date = State()
     need_photo = State()



