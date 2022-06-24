from aiogram import types, Dispatcher
from model.nata import fasta
from model.natanp import natanp


async def start(messag: types.Message):
    await messag.answer("/np + текст - выявляет именные группы \n /s + текст выводит полную  обработку текста наташей")


async def startSasha(messag: types.Message):
    await messag.reply(str(fasta(str(messag.text))))


async def startnp(messag: types.Message):
    await messag.reply(str(natanp(str(messag.text))))


def registerKlient(dp: Dispatcher):
    dp.register_message_handler(start, commands=["help"])
    dp.register_message_handler(startSasha, commands=["s"])
    dp.register_message_handler(startnp, commands=["np"])
