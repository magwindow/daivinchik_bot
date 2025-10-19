import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
load_dotenv()

import handlers
from data.database import Database

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    
    db = Database("users_db.sqlite", "users")
    # await db.create_table()
    dp.include_routers(
        handlers.start.router, 
        handlers.questionaire.router, 
        handlers.bot_messages.router
        )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=db)

if __name__ == '__main__':
    asyncio.run(main())