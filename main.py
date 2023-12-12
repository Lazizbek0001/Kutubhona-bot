import logging
from data_base import kutubhona


from aiogram.dispatcher.filters import Text

from aiogram import Bot, Dispatcher, executor, types
from config import *
from buttons import *

from state import UserData, Admin, Admin_rek
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove


# import asyncio


db = kutubhona()
db.create_books_table()
db.create_category_table()
db.create_users_table()

storage = MemoryStorage()
bot =Bot(token=API_TOKEN)
dp=Dispatcher(bot, storage=storage)


logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.username)
    await message.answer("Kitoblar bot Hush kelibsiz", reply_markup= await gen_start())


@dp.callback_query_handler(text = "books")
async def send(call: types.CallbackQuery):
    await call.message.answer("Kategoriyalar",  reply_markup=await gen_category())

    await call.message.delete()
    
@dp.callback_query_handler(text = "back22")
async def send(call: types.CallbackQuery):
    await call.message.answer("Kitoblar bot Hush kelibsiz", reply_markup= await gen_start())

    await call.message.delete()    

    
@dp.callback_query_handler(text = "aloqa")
async def send(call: types.CallbackQuery):
    await call.message.answer("Taklif va murojatlar uchun @Laziznormatov ga murojat qiling", reply_markup=back1)
    await call.message.delete()

    
    
@dp.callback_query_handler(text = "search")
async def send(call: types.CallbackQuery):
    await call.message.answer("Qidirayotgan kitobni kiriting")
    await UserData.text.set()
    
    
@dp.message_handler(state=UserData.text)
async def sned(message: types.Message, state:FSMContext):
    await state.update_data(text = message.text)
    await message.answer("Marhamat kitoblar", reply_markup=await book_search(message.text))
    await UserData.check.set()
    
@dp.callback_query_handler(state= UserData.check)
async def send(call: types.CallbackQuery, state: FSMContext):
    book = db.select_book(call.data)

    text = f"""<b>{book[2]}</b>
        
    Muallif: {book[-4]}
        
    Izoh: {book[-1]}
        
    #<code>{book[0]}</code>
        """
    await call.message.answer_photo(photo=book[-3], caption=text, parse_mode="HTML")
    await call.message.answer_document(document=book[-2])
    await call.message.answer("Kitoblar bot Hush kelibsiz", reply_markup= await gen_start())

    
     

@dp.callback_query_handler(Text(startswith="Kat_"))
async def send(call: types.CallbackQuery):
    index_under = call.data.index("_")
    
    id = call.data[index_under+1:]  

    await call.message.answer("Kitoblar to'plami", reply_markup= await gen_books(id))

    await call.message.delete()




@dp.callback_query_handler(Text(startswith="book_"))
async def send(call: types.CallbackQuery):
    index_under = call.data.index("_")
    id = call.data[index_under+1:]
    
    if call.data == "book_back":
        await call.message.answer("Kitoblar to'plami", reply_markup= await gen_category())
        await call.message.delete()
    else:
        
        book = db.select_book_by_id(id)
        
        
    

        
        text = f"""<b>{book[2]}</b>
        
    Muallif: {book[-4]}
        
    Izoh: {book[-1]}
        
    #<code>{book[0]}</code>
        """
        await call.message.answer_photo(photo=book[-3], caption=text, parse_mode="HTML")
        await call.message.answer_document(document=book[-2], reply_markup=await back_btn(book[1]))
        

        await call.message.delete()


@dp.callback_query_handler(text = "main_back")
async def send(call: types.CallbackQuery):
    await call.message.answer("Kitoblar bot Hush kelibsiz", reply_markup= await gen_start())

    await call.message.delete()


@dp.callback_query_handler(Text(startswith="back_"))
async def send(call: types.CallbackQuery):
    index_under = call.data.index("_")
    id = call.data[index_under+1:]   

    await call.message.answer("Kitoblar to'plami", reply_markup= await gen_books(id))

    


#############         ADMIN PANEL




@dp.message_handler(commands='admin', user_id = admin)
async def send_welcome(message: types.Message):
    await message.answer("Hush kelibsiz nima qilmoqchisiz", reply_markup=await admin_menu())


    
    
    

@dp.callback_query_handler(text="update_book")
async def send(call:types.CallbackQuery):
    await call.message.answer("Kitob kategoriyasini kiriting")
    await Admin.update_id.set()
    await call.message.delete()
@dp.message_handler(state=Admin.update_id)
async def send(message:types.Message, state:FSMContext):
    await message.answer("Kitob nomini kirting", reply_markup= await generate_book_btn(message.text))
    await Admin.update_name.set()    
    
    
    
@dp.callback_query_handler(state=Admin.update_name)
async def send(call:types.CallbackQuery, state:FSMContext):
    await state.update_data(update_name = call.data)
    await call.message.answer("Nimani yangilaysiz", reply_markup= await admin_update())
    await Admin.update_check.set()
    
    
    
    
@dp.callback_query_handler(state=Admin.update_check)
async def send(call : types.CallbackQuery,state: FSMContext):
    await state.update_data(update_check = call.data)
    if call.data == "photo_id":
        await call.message.answer("Jonating yangi rasmni")
        await Admin.update_photo.set()
    elif call.data == "back_ad_menu":
        await call.message.answer("Hush kelibsiz nima qilmoqchisiz", reply_markup=await admin_menu())
        await state.finish()
        await state.reset_data()
    elif call.data == "file_id":
        await call.message.answer("Jonating yangi faylni")
        await Admin.update_pdf.set()
    else:
        await call.message.answer("Yangi ma'lumotni kiriting")
        await Admin.update_thing.set()
        
    await call.message.delete()
 
@dp.message_handler(state=Admin.update_thing)
async def send(message : types.Message,state: FSMContext):
    await state.update_data(update_thing = message.text)

    data = await state.get_data()
    name_ = data.get('update_name')
    old_ = data.get('update_check')
    new_ = data.get('update_thing')
    
    
    db.update_books(name_,new_,old_)
 
 
 
    await message.answer("Yangi ma'lumotlar qo'shildi")
    await state.finish()
    await state.reset_data()
    await message.answer("Hush kelibsiz nima qilmoqchisiz", reply_markup=await admin_menu())

@dp.message_handler(content_types='document',state=Admin.update_pdf)
async def send(message : types.Message,state: FSMContext):
    file = message.document.file_id

    await state.update_data(update_pdf = file)
    data = await state.get_data()
    name_ = data.get('update_name')
    old_ = data.get('update_check')
    new_ = data.get('update_pdf')
    

    db.update_books(name_,new_,old_)
    await message.answer("Pdf fayl o'zgartirildi")
    await state.finish()
    await state.reset_data()
    await message.answer("Hush kelibsiz nima qilmoqchisiz", reply_markup=await admin_menu())


@dp.message_handler(content_types='photo',state=Admin.update_photo)
async def send(message : types.Message,state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(update_photo = photo)
    data = await state.get_data()
    name_ = data.get('update_name')
    old_ = data.get('update_check')
    new_ = data.get('update_photo')


    
    db.update_books(name_,new_,old_)
  
    await message.answer("Rasm fayl o'zgartirildi")
    await state.finish()
    await state.reset_data()
    await message.answer("Hush kelibsiz nima qilmoqchisiz", reply_markup=await admin_menu())






@dp.callback_query_handler(text = "del_kat")
async def send(call: types.CallbackQuery):
    await call.message.answer("Kategoriya nomini kiriting")
    await Admin.del_kat_id.set()
    await call.message.delete()


@dp.message_handler(state=Admin.del_kat_id)
async def send(message : types.Message,state: FSMContext):
    db.delete_category(message.text)
    await message.answer("Kategoriya o'chirildi va kategoriyaga tegishli barcha kitob o'chirildi")
    await state.finish()
    await state.reset_data()
    await message.answer("Hush kelibsiz nima qilmoqchisiz", reply_markup=await admin_menu())



@dp.callback_query_handler(text = "add_kat")
async def send(call: types.CallbackQuery):
    await call.message.answer("Kategoriya nomini kiriting")
    await Admin.kat_name.set()
    
    
@dp.message_handler(state=Admin.kat_name)
async def send(message : types.Message,state: FSMContext):
    await state.update_data(kat_name = message.text)
    data = await state.get_data()
    name_ = data.get('kat_name')
    
    db.insert_category1(name=name_)
    await message.answer("Yangi kategoriya yaratildi")
    await state.finish()
    await state.reset_data()
    await message.answer("Hush kelibsiz nima qilmoqchisiz", reply_markup=await admin_menu())

    



@dp.callback_query_handler(text = "del_book")
async def send(call: types.CallbackQuery):
    await call.message.answer("O'chirmoqchi bo'lgan kitob kategoriya nomini kiriting ")
    await Admin.del_book_id.set()
    await call.message.delete()
@dp.message_handler(state=Admin.del_book_id)
async def send(message: types.Message, state:FSMContext):
    await state.update_data(del_book_id = message.text)
    
    await message.answer("Kitob nomini kiriting ", reply_markup=await generate_book_btn(message.text))
    await Admin.del_book_name.set()


@dp.callback_query_handler(state=Admin.del_book_name)
async def exo(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(del_book_name = call.data)
    await call.message.answer("Iltimos tasdiqlang",reply_markup=ReplyKeyboardRemove())
    await call.message.answer("Kitobni o'chirmoqchimisiz", reply_markup=await admin_menu_del())
    await Admin.del_check.set()
    
    
@dp.callback_query_handler(state=Admin.del_check)
async def send(call: types.CallbackQuery, state: FSMContext):
    if call.data =="ha2":
        
        data = await state.get_data()
        name_ = data.get('del_book_name')
        
        db.delete_book(name_)
        
        
  
        await call.message.answer("Kitob bazadan o'chirildi")
        await call.message.delete()
        
    elif call.data =="yoq2":
        await call.message.answer("Bazadan o'chirilmadi")
        await call.message.delete()

    await state.finish()
    await state.reset_data()
    await call.message.delete()
    await call.message.answer("Hush kelibsiz nima qilmoqchisiz", reply_markup=await admin_menu())

    
    
    
        

    
    
@dp.callback_query_handler(text = "add_book")
async def send(call: types.CallbackQuery):
    await call.message.answer("Kitob kategoriyasini nomini kiriting ")
    await Admin.kitob_cat.set()
    await call.message.delete()
    
@dp.message_handler(state=Admin.kitob_cat)
async def send(message: types.Message, state:FSMContext):
    await state.update_data(kitob_cat = message.text)
    await message.answer("Kitob nomini kiriting ")
    await Admin.kitob_name.set()
    

@dp.message_handler(state=Admin.kitob_name)
async def send(message: types.Message, state:FSMContext):
    await state.update_data(kitob_name = message.text)
    await message.answer("Kitob rasmini jonating ")
    await Admin.kitob_photo.set() 



@dp.message_handler(content_types='photo', state=Admin.kitob_photo)
async def handle_pdf(message: types.Message, state: FSMContext):
    
    photo_file_id = message.photo[-1].file_id
    await state.update_data(kitob_photo = photo_file_id)
    await message.answer("Kitob muallifi ismini kiriting ")
    await Admin.kitob_auth.set()
    
    

@dp.message_handler(state=Admin.kitob_auth)
async def send(message: types.Message, state:FSMContext):
    await state.update_data(kitob_auth = message.text)
    await message.answer("Kitob haqida izoh yozing qisqacha")
    await Admin.kitob_desc.set() 
    
    


@dp.message_handler(state=Admin.kitob_desc)
async def send(message: types.Message, state:FSMContext):
    await state.update_data(kitob_desc = message.text)
    await message.answer("Kitobni jonating pdf ko'rinishida ")
    await Admin.kitob_pdf.set() 



@dp.message_handler(content_types='document', state=Admin.kitob_pdf)
async def handle_pdf(message: types.Message, state:FSMContext):
    
    pdf_file_id = message.document.file_id
    # You can now use pdf_file_id for further processing
    await state.update_data(kitob_pdf = pdf_file_id)
    
    data = await state.get_data()
    kat_ = data.get('kitob_cat')
    name_ = data.get('kitob_name')
    photo_ = data.get('kitob_photo')
    auther_ = data.get('kitob_auth')
    desc_ = data.get('kitob_desc')
    pdf_ = data.get('kitob_pdf')
    
    
    text = f"""{name_}
    
{auther_}

{desc_}"""
    
    await message.answer_photo(photo=photo_, caption=text)

    await message.answer_document(document=pdf_)

    await message.answer("Malumotlar to'grimi", reply_markup=await admin_menu_add())
    
    
    
    await Admin.check_kitob.set()
    
    




@dp.callback_query_handler(state=Admin.check_kitob)
async def send(call: types.CallbackQuery, state: FSMContext):
    if call.data =="ha":
        
        data = await state.get_data()
        kat_ = data.get('kitob_cat')
        name_ = data.get('kitob_name')
        photo_ = data.get('kitob_photo')
        auther_ = data.get('kitob_auth')
        desc_ = data.get('kitob_desc')
        pdf_ = data.get('kitob_pdf')
        cat = db.select_category_name(kat_)
        cat_ = cat[0]
        db.insert_books(cat_,name_,auther_,photo_,pdf_,desc_)
        await call.message.answer("Kitob bazaga qo'shildi")
        await call.message.delete()
        
    elif call.data =="yoq":
        await call.message.answer("Bazaga qoshilmadi")
        await call.message.delete()

    await state.finish()
    await state.reset_data()
    await call.message.answer("Hush kelibsiz nima qilmoqchisiz", reply_markup=await admin_menu())





@dp.callback_query_handler(text = "reklama")
async def send(call: types.CallbackQuery):
    await call.message.answer("Reklama fileni tanlang ", reply_markup=await reklama_p())
    await Admin_rek.rek_check.set()
    
    
@dp.callback_query_handler(state=Admin_rek.rek_check)
async def send(call: types.CallbackQuery):
    if call.data == 'photo':
        await call.message.answer("Rasmni jo'nating")
        await Admin_rek.rek_photo.set()
    
    
    else:
        await call.message.answer("Video jo'nating")
        await Admin_rek.rek_video.set()
    await call.message.delete()

@dp.message_handler(content_types='video', state=Admin_rek.rek_video)
async def send(message: types.Message, state: FSMContext):
    photo = message.video.file_id
    await state.update_data(rek_video = photo)
    await message.answer("Reklama matn jo'nating")
    await Admin_rek.rek_text1.set()
    
       
    
@dp.message_handler(content_types='photo', state=Admin_rek.rek_photo)
async def send(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(rek_photo = photo)
    await message.answer("Reklama matn jo'nating")
    await Admin_rek.rek_text.set()
    
    
    
    
@dp.message_handler(state=Admin_rek.rek_text1)
async def send(message: types.Message, state: FSMContext):
    
    await state.update_data(rek_text1 = message.text)
    await message.answer("Tekshiring")
    data = await state.get_data()
    vido_ = data.get('rek_video')
    await message.answer_video(video=vido_, caption=message.text, reply_markup= await reklama_choose())
    
    await Admin_rek.rek_next1.set()

@dp.message_handler(state=Admin_rek.rek_text)
async def send(message: types.Message, state: FSMContext):
    
    await state.update_data(rek_text = message.text)
    await message.answer("Tekshiring")
    data = await state.get_data()
    vido_ = data.get('rek_photo')
    await message.answer_photo(photo=vido_, caption=message.text, reply_markup= await reklama_choose())
    
    await Admin_rek.rek_next.set()
    
@dp.callback_query_handler(state=Admin_rek.rek_next)
async def sedn(call: types.CallbackQuery, state: FSMContext):
    
    users = db.select_all_user()
    if call.data == 'ha3':
        data = await state.get_data()
      
        spam_info = 0
        not_spm = 0
        for user in users:
            
            try:
                await bot.send_photo(chat_id=user[0], photo = data.get('rek_photo'), caption= data.get('rek_text')) 
                not_spm +=1
                
            except:
                spam_info +=1

        await bot.send_message(chat_id=admin, text = f"Xabar yetib bormaganlar: {spam_info}\nXabar yetib borganlar: {not_spm}")
        await call.message.answer("Admin hush kelibsiz", reply_markup=await admin_menu())
        await state.finish()
        await state.reset_data()
        await call.message.delete()

    else:
        await call.message.answer("Admin hush kelibsiz", reply_markup=await admin_menu())
        await state.finish()
        await state.reset_data()
        await call.message.delete()
     
        
        
@dp.callback_query_handler(state=Admin_rek.rek_next1)
async def sedn(call: types.CallbackQuery, state: FSMContext):
    
    users = db.select_all_user()
    if call.data == 'ha3':
        data = await state.get_data()
       
        spam_info = 0
        not_spm = 0
        for user in users:
            try:
                await bot.send_video(chat_id=user[0], video = data.get('rek_video'), caption= data.get('rek_text1')) 
                not_spm +=1
            
            except:
                spam_info +=1

        await bot.send_message(chat_id=admin, text = f"Xabar yetib bormaganlar: {spam_info}\nXabar yetib borganlar: {not_spm}")
        await call.message.answer("Admin hush kelibsiz", reply_markup=await admin_menu())
        await state.finish()
        await state.reset_data()
        await call.message.delete()


    else:
        await call.message.answer("Admin hush kelibsiz", reply_markup=await admin_menu())
        await state.finish()
        await state.reset_data()
        await call.message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)