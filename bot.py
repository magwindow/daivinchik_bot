import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
load_dotenv()

import handlers
from data.database import DataBase

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    
    db = DataBase()
    dp.startup.register(db.create) # Создаем БД при запуске бота.
    
    dp.include_routers( 
        handlers.questionaire.router, 
        handlers.bot_messages.router
        )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=db)

if __name__ == '__main__':
    asyncio.run(main())