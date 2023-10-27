from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv


load_dotenv()
stor= MemoryStorage()
bt= Bot(token=getenv('TOKENAPIT'))
dp = Dispatcher(bt, storage=stor)