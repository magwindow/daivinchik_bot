from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.reply import main, rmk
from keyboards.builders import form_btn
from utils.states import Form
from utils.city import check
from data.database import DataBase

router = Router()

@router.message(CommandStart())
async def my_form(message: Message, state: FSMContext, db: DataBase):
    is_exists = await db.get(message.from_user.id, one=True)
    if is_exists is not None:
        data = await db.get(message.from_user.id)
        user = data.one()
        pattern = {
            "photo": user.photo,
            "caption": f"{user.name} {user.age}, {user.city}\n{user.bio}"
        }
        await message.answer_photo(**pattern, reply_markup=main)
    else:
        await state.set_state(Form.name)
        await message.answer("Отлично, введи своё имя", reply_markup=form_btn(message.from_user.first_name))
    

@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Теперь укажи свой возраст", reply_markup=rmk)
    

@router.message(Form.age)
async def form_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=int(message.text))
        await state.set_state(Form.city)
        await message.answer("В каком городе ты живешь?")
    else:
        await message.answer("Попробуй ещё раз")
        

@router.message(Form.city)
async def form_city(message: Message, state: FSMContext):
    if await check(message.text):
        await state.update_data(city=message.text)
        await state.set_state(Form.gender)
        await message.answer("Теперь давай определимся с полом", reply_markup=form_btn(["👨🏻Парень", "👩🏻Девушка"]))
    else:
        await message.answer("Попробуй ещё раз")
        

@router.message(Form.gender, F.text.casefold().in_(["👨🏻парень", "👩🏻девушка"]))
async def form_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Form.look_for)
    await message.answer("Кого будем искать?", reply_markup=form_btn(["👨🏻Парней", "👩🏻Девушек", "Мне все равно"]))
    

@router.message(Form.gender)
async def incorrect_form_gender(message: Message):
    await message.answer("Выбери один вариант")
    

@router.message(Form.look_for, F.text.casefold().in_(["👨🏻парней", "👩🏻девушек", "мне все равно"]))
async def form_look_for(message: Message, state: FSMContext):
    await state.update_data(look_for=message.text)
    await state.set_state(Form.bio)
    await message.answer("Напиши немного о себе", reply_markup=rmk)
    

@router.message(Form.look_for)
async def incorrect_form_look_for(message: Message):
    await message.answer("Выбери один вариант")
    

@router.message(Form.bio)
async def form_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await state.set_state(Form.photo)
    await message.answer("Пришли мне фото")
    

@router.message(Form.photo, F.photo)
async def form_photo(message: Message, state: FSMContext, db: DataBase):
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()
    data["user_id"] = message.from_user.id
    data["photo"] = photo_file_id
    await db.insert(**data)
    await state.clear()
    
    form_text = []
    [form_text.append(str(value)) for key, value in data.items() if key not in ["user_id", "photo"]]
    await message.answer_photo(photo_file_id, caption="\n".join(form_text))
    

@router.message(Form.photo, ~F.photo)
async def form_photo(message: Message):
    await message.answer("Отправь фото!")
    


    