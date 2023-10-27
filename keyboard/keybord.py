from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


butt1 = KeyboardButton("Генерация картинок!")
butt = KeyboardButton("Генерация аудио озвучки!")
butt2 = KeyboardButton("Генерация текста из аудио файла!")
butt3 = KeyboardButton("Подать заявку на дипфейк")
butt4 = KeyboardButton("Чат gpt")
butt5 = KeyboardButton('конвертер pdf в docx')

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(butt4).add(butt5).add(butt).add(butt2).row(butt3).row(butt1)

def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Создать профиль'))

    return kb


def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))