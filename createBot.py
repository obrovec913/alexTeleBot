from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from a import token
from aiogram.contrib.fsm_storage.memory import MemoryStorage


stor= MemoryStorage()
bt= Bot(token=token)
dp = Dispatcher(bt, storage=stor)