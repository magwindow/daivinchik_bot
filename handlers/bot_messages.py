from aiogram import Router, F
from aiogram.types import Message

from data.database import DataBase

router = Router()

@router.message()
async def echo(message: Message, db: DataBase):
    if message.text.lower() == 'моя анкета':
        user = await db.get(message.from_user.id)
        pattern = {
            'photo': user.photo,
            'caption': f'{user.name} {user.age}, {user.city}\n{user.bio}'
        }
        await message.answer_photo(**pattern)