from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Моя анкета'),
            KeyboardButton(text='Статистика'),
        ]
    ], resize_keyboard=True
) 
