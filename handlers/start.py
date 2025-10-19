from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from data.database import Database
from keyboards.reply import main

router = Router()

@router.message(CommandStart())
async def start(message: Message, db: Database):
    await message.answer('Выберете действие:', reply_markup=main)
