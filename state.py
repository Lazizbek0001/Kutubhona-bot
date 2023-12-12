from aiogram.dispatcher.filters.state import State, StatesGroup

class UserData(StatesGroup):
    text = State()
    check = State()
    
class Admin(StatesGroup):
    kitob_cat = State()
    kitob_name = State()
    kitob_photo = State()
    kitob_auth = State()
    kitob_desc = State()
    kitob_pdf = State()
    
    check_kitob = State()
    
    
    
    del_book_id = State()
    del_book_name = State()
    del_check = State()
    
    
    kat_name = State()
    
    
    
    del_kat_id = State()
    
    
    
    update_id = State()
    update_name = State()
    update_check = State()
    
    
    
    update_thing = State()
    update_photo = State()
    update_pdf = State()
    
    
class Admin_rek(StatesGroup):
    
    rek_photo = State()
    rek_text = State()
    rek_video = State()
    rek_check = State()
    
    rek_text1 = State()
    
    rek_next = State()
    rek_next1 = State()