from createBot import dp
from aiogram.utils import executor
from handlera import klient,opshen
from db.cr__db import db_start

async def on_startup(_):
    await db_start()
 
klient.registerKlient(dp)
opshen.registerOpshen(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)