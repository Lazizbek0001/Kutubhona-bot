from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from data_base import kutubhona

db = kutubhona()

start = {
    "Kitoblar" : "books",
    "Qidirish" : "search",
    "Aloqa" : "aloqa"
}

async def gen_start():
    btn = InlineKeyboardMarkup(row_width=2)
    for key, value in start.items():
        btn.insert(InlineKeyboardButton(text=key, callback_data=value))
    return btn
        

async def gen_category():
    btn = InlineKeyboardMarkup(row_width=2)
    category = db.select_category()
    for i in category:
        btn.insert(InlineKeyboardButton(text=i[1], callback_data=f"Kat_{i[0]}"))
    btn.insert(InlineKeyboardButton(text="Ortga", callback_data="main_back"))
    return btn
        
        
        
async def gen_books(id):
    btn = InlineKeyboardMarkup(row_width=2)
    books = db.select_category_id(id)
    for i in books:
        
        btn.insert(InlineKeyboardButton(text=f'{i[2]}|{i[3]}', callback_data=f"book_{i[0]}"))
    btn.add(InlineKeyboardButton(text="Ortga", callback_data=f'book_back'))
    return btn



# async def back_book(id):
#     btn = InlineKeyboardMarkup(row_width=)


async def back_btn(id):
    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton(text="Ortga", callback_data=f"back_{id}"))
    return btn


admin1 = {"Kitob qo'shish" : "add_book",
         "Kitob o'chirish": "del_book",
         "Kategoriya qo'shish" : "add_kat",
         "Kategoriya o'chirish" : "del_kat",
         "Kitob yangilash" : "update_book",
         "Reklama": "reklama"
         }

async def admin_menu():
    btn = InlineKeyboardMarkup(row_width=2)
    for key, value in admin1.items():
        btn.insert(InlineKeyboardButton(text=key, callback_data=value))
    return btn

admin_update1 = {"Nomini o'zgartirish" : "name",
                "Kategoriyasini o'zgartirish": "category_id",
                "Muallifni o'zgartirish": "auther",
                "Rasmini o'zgartirish":"photo_id",
                "Izohni o'zgartirish":"comment",
                "Pdf fayl o'zgartirish": "file_id",
                "Ortga": "back_ad_menu"
                }


async def admin_update():
    btn = InlineKeyboardMarkup(row_width=2)
    for key, value in admin_update1.items():
        btn.add(InlineKeyboardButton(text=key, callback_data=value))
    return btn


choose = {"Ha": 'ha',"Yoq": 'yoq'}
async def admin_menu_add():
    btn = InlineKeyboardMarkup(row_width=2)
    for i,m  in choose.items():
        btn.insert(InlineKeyboardButton(text=i, callback_data=m))
    return btn



async def generate_book_btn(name):
    books = db.select_category_name(name)
    books = db.select_category_id(books[0])
    btn = InlineKeyboardMarkup(row_width=2)
    for i  in books:
        btn.insert(InlineKeyboardButton(text=i[2], callback_data=i[2]))
    return btn




choose1 = {"Ha": 'ha2',"Yoq": 'yoq2'}


async def admin_menu_del():
    btn = InlineKeyboardMarkup(row_width=2)
    for i,m  in choose1.items():
        btn.insert(InlineKeyboardButton(text=i, callback_data=m))
    return btn

async def book_search(text):
    btn = InlineKeyboardMarkup(row_width=3)
    books = db.search_book(text)
    for i in books:
        btn.insert(InlineKeyboardButton(text=i[2], callback_data=i[2]))
    return btn



back1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ortga", callback_data='back22')
        ]
    ]
)


choose2 = {"Ha": 'ha3',"Yoq": 'yoq3'}


async def reklama_choose():
    btn = InlineKeyboardMarkup(row_width=2)
    for i,m  in choose2.items():
        btn.insert(InlineKeyboardButton(text=i, callback_data=m))
    return btn


rek = {'Rasm':'photo', 'Video':'video'}


async def reklama_p():
    btn = InlineKeyboardMarkup(row_width=2)
    for i,m  in rek.items():
        btn.insert(InlineKeyboardButton(text=i, callback_data=m))
    return btn