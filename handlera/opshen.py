
from aiogram  import types, Dispatcher
import string
import json
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models.profil_models import ProfileStatesGroup
from db.cr__db import  create_profile, edit_profile, prover_profile
from aiogram.dispatcher.filters import Text
from keyboard.keybord import kb, get_kb








def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))

    return kb


async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.reply('Вы прервали создание анкеты!',
                        reply_markup=get_kb())



async def cmd_start(messag: types.Message) -> None:
    if not await prover_profile(user_id=messag.from_user.id):
        await messag.answer('Добро пожаловать в alex_bot - создайте профиль для работы с ботом',
                         reply_markup=get_kb())
        await create_profile(user_id=messag.from_user.id)
    await messag.answer('Добро пожаловать в alex_bot - ',
                         reply_markup=kb)



async def cmd_create(message: types.Message) -> None:
    await message.reply("Let's create your profile! To begin with, send me your photo!",
                        reply_markup=get_cancel_kb())
    await ProfileStatesGroup.photo.set()  # установили состояние фото



async def check_photo(message: types.Message):
    await message.reply('Это не фотография!')



async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await message.reply('Теперь отправь своё имя!')
    await ProfileStatesGroup.next()



async def check_age(message: types.Message):
    await message.reply('Введите реальный возраст!')



async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Сколько тебе лет?')
    await ProfileStatesGroup.next()



async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text

    await message.reply('А теперь расскажи немного о себе!')
    await ProfileStatesGroup.next()



async def load_desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text

    await edit_profile(state, user_id=message.from_user.id)
    await message.reply('Ваша акнета успешно создана!',reply_markup=kb)
    await state.finish()



'''
async def noMat(messag: types.Message):
    if{mat.lower().strip().translate(str.maketrans("","", string.punctuation)) for mat in messag.text.split(" ")}\
        .intersection(set(json.load(open("matt.json", encoding="utf-8")))) != set():
        await messag.reply("маты у нас запрещены")
        await messag.delete()
        with open(f"{messag.from_user.id}.txt", "w", encoding="utf-8")as user:
            user.write(str(messag))
'''

def registerOpshen(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands=['cancel'], state='*')
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_create, Text(equals='Создать профиль', ignore_case=True))
    dp.register_message_handler(check_photo, lambda message: not message.photo, state=ProfileStatesGroup.photo)
    dp.register_message_handler(load_photo, content_types=['photo'], state=ProfileStatesGroup.photo)
    dp.register_message_handler(check_age, lambda message: not message.text.isdigit() or float(message.text) > 100, state=ProfileStatesGroup.age)
    dp.register_message_handler(load_name, state=ProfileStatesGroup.name)
    dp.register_message_handler(load_age, state=ProfileStatesGroup.age)
    dp.register_message_handler(load_desc, state=ProfileStatesGroup.description)