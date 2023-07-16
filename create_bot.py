from aiogram import Bot, Dispatcher, types
from database import DataBase
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage


db = DataBase('academy.db')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())