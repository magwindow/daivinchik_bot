from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.builders import form_btn
from utils.states import Form
from utils.city import check

router = Router()

@router.message(Command("form"))
async def my_form(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Отлично, введи своё имя", reply_markup=form_btn(message.from_user.first_name))
    

@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Теперь укажи свой возраст")
    

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
async def incorrect_gender(message: Message):
    await message.answer("Выбери один вариант")
    

@router.message(Form.look_for, F.text.casefold().in_(["👨🏻парней", "👩🏻девушек", "мне все равно"]))
async def form_look_for(message: Message, state: FSMContext):
    await state.update_data(look_for=message.text)
    await state.set_state(Form.about)
    await message.answer("Напиши немного о себе")
    

@router.message(Form.look_for)
async def incorrect_form_look_for(message: Message):
    await message.answer("Выбери один вариант")
    

@router.message(Form.about)
async def form_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await state.set_state(Form.photo)
    await message.answer("Пришли мне фото")
    

@router.message(Form.photo)
async def form_photo(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()
    await state.clear()
    frm_text = []
    [frm_text.append(f"{key}: {value}") for key, value in data.items()]
    await message.answer_photo(photo_file_id, caption="\n".join(frm_text))
    

@router.message(Form.look_for)
async def form_photo(message: Message):
    await message.answer("Отправь фото")
    