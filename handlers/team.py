import json
import os
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import ADMIN_ID

router = Router()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'locales.json'), 'r', encoding='utf-8') as f:
    text_data = json.load(f)

class TeamForm(StatesGroup):
    name = State()
    country = State()
    main_direction = State()
    additional_directions = State()
    experience = State()
    skills = State()
    interests = State()
    availability = State()

def make_kb(buttons: list, lang: str = "ru") -> ReplyKeyboardMarkup:
    cancel_text = text_data[lang]["btn_cancel"]
    kb = []
    for row in buttons:
        kb.append([KeyboardButton(text=b) for b in row])
    kb.append([KeyboardButton(text=cancel_text)])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(F.text.in_([text_data['ru']['btn_cancel'], text_data['en']['btn_cancel']]))
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    user_lang = message.from_user.language_code
    lang = user_lang if user_lang in ['ru', 'en'] else 'ru'
    from handlers.common import get_main_menu, get_text
    await message.answer(get_text(lang, "main_menu"), reply_markup=get_main_menu(lang))

@router.message(F.text.in_(["🤝 Хочу в команду", "🤝 Join the Team"]))
async def start_team_form(message: Message, state: FSMContext):
    lang = "en" if "Join the Team" in message.text else "ru"
    await state.update_data(user_lang=lang)
    await state.set_state(TeamForm.name)
    await message.answer(text_data[lang]["q_name"], reply_markup=make_kb([], lang))

@router.message(TeamForm.name)
async def process_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(name=message.text)
    await state.set_state(TeamForm.country)
    await message.answer(text_data[lang]["q_country"], reply_markup=make_kb([], lang))

@router.message(TeamForm.country)
async def process_country(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(country=message.text)
    await state.set_state(TeamForm.main_direction)

    dir_buttons = [
        [text_data[lang]["dir_1"], text_data[lang]["dir_2"]],
        [text_data[lang]["dir_3"], text_data[lang]["dir_4"]],
        [text_data[lang]["btn_all"]]
    ]
    await message.answer(text_data[lang]["q_main_dir"], reply_markup=make_kb(dir_buttons, lang))

@router.message(TeamForm.main_direction)
async def process_main_direction(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(main_direction=message.text)
    await state.set_state(TeamForm.additional_directions)

    sub_buttons = [
        [text_data[lang]["sub_1"], text_data[lang]["sub_2"]],
        [text_data[lang]["sub_3"], text_data[lang]["sub_4"]],
        [text_data[lang]["sub_5"]]
    ]
    await message.answer(text_data[lang]["q_sub_dir"], reply_markup=make_kb(sub_buttons, lang))

@router.message(TeamForm.additional_directions)
async def process_additional(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(additional_directions=message.text)
    await state.set_state(TeamForm.experience)
    await message.answer(text_data[lang]["q_exp"], reply_markup=make_kb([], lang))

@router.message(TeamForm.experience)
async def process_experience(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(experience=message.text)
    await state.set_state(TeamForm.skills)
    await message.answer(text_data[lang]["q_skills"], reply_markup=make_kb([], lang))

@router.message(TeamForm.skills)
async def process_skills(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(skills=message.text)
    await state.set_state(TeamForm.interests)
    await message.answer(text_data[lang]["q_interests"], reply_markup=make_kb([], lang))

@router.message(TeamForm.interests)
async def process_interests(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(interests=message.text)
    await state.set_state(TeamForm.availability)
    await message.answer(text_data[lang]["q_time"], reply_markup=make_kb([], lang))

@router.message(TeamForm.availability)
async def process_availability(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.clear()
    lang = user_data.get("user_lang", "ru")
    user_username = f"@{message.from_user.username}" if message.from_user.username else "No username"

    notification_text = (
        "🆕 **New KINDORF Member**\n\n"
        f"Name: {user_data['name']}\n"
        f"Country: {user_data['country']}\n"
        f"Main direction: {user_data['main_direction']}\n"
        f"Additional directions: {user_data['additional_directions']}\n"
        f"Experience: {user_data['experience']}\n"
        f"Skills: {user_data['skills']}\n"
        f"Interested in: {user_data['interests']}\n"
        f"Availability: {message.text}\n\n"
        f"Contact Link: {user_username}"
    )

    try:
        await message.bot.send_message(chat_id=ADMIN_ID, text=notification_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error: {e}")

    from handlers.common import get_main_menu
    await message.answer(text_data[lang]["team_success"], reply_markup=get_main_menu(lang))
