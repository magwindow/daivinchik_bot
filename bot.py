import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
load_dotenv()

import handlers
from data.database import DataBase
from filters.url_filter import UrlInMessageCheck

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    db = DataBase()
    
    # dp.message.filter(UrlInMessageCheck()) # Фильтр на проверку ссылки в тексте.
    dp.startup.register(db.create) # Создаем БД при запуске бота.
    
    dp.include_routers( 
        handlers.questionaire.router, 
        handlers.search_user.router,
        handlers.bot_messages.router
        )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=db)

if __name__ == '__main__':
    asyncio.run(main())