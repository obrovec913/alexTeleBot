from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher


class Fsnatasha(StatesGroup):
    text= State()



async def startnata(messag: types.Message):
    await Fsnatasha.text.set()
    await messag.reply("введите текст для обработки")



async def prossNata(messag: types.Message, stat: FSMContext):
    async with stat.proxy() as  fi:
        fi["text"] = messag.text
    async with stat.proxy()as text:
        await messag.reply(str(text))
    await stat.finish()



def registerNatasha(dp: Dispatcher):
    dp.register_message_handler(startnata, commands=["САША"], state=None)
    dp.register_message_handler(prossNata, state=Fsnatasha.text)