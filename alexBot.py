from createBot import dp
from aiogram.utils import executor
from handlera import klient,opshen,natasha


klient.registerKlient(dp)
natasha.registerNatasha(dp)
opshen.registerOpshen(dp)



executor.start_polling(dp, skip_updates=True)