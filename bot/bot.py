from aiogram import Bot, Dispatcher, Router
from config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
router = Router()