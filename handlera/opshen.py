from aiogram  import types, Dispatcher
import string
import json


async def noMat(messag: types.Message):
    if{mat.lower().strip().translate(str.maketrans("","", string.punctuation)) for mat in messag.text.split(" ")}\
        .intersection(set(json.load(open("matt.json", encoding="utf-8")))) != set():
        await messag.reply("маты у нас запрещены")
        await messag.delete()
        with open(f"{messag.from_user.id}.txt", "w", encoding="utf-8")as user:
            user.write(str(messag))


def registerOpshen(dp: Dispatcher):
    dp.register_message_handler(noMat)