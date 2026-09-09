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

class ProjectForm(StatesGroup):
    project_name = State()
    description = State()
    current_stage = State()
    request = State()

def make_project_kb(lang: str = "ru") -> ReplyKeyboardMarkup:
    cancel_text = text_data[lang]["btn_cancel"]
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=cancel_text)]], resize_keyboard=True)

@router.message(F.text.in_([text_data['ru']['btn_cancel'], text_data['en']['btn_cancel']]), ProjectForm)
async def cancel_project_form(message: Message, state: FSMContext):
    await state.clear()
    user_lang = message.from_user.language_code
    lang = user_lang if user_lang in ['ru', 'en'] else 'ru'
    from handlers.common import get_main_menu, get_text
    await message.answer(get_text(lang, "main_menu"), reply_markup=get_main_menu(lang))

@router.message(F.text.in_(["💡 Предложить проект", "💡 I Have a Project"]))
async def start_project_form(message: Message, state: FSMContext):
    lang = "en" if "I Have a Project" in message.text else "ru"
    await state.update_data(user_lang=lang)
    await state.set_state(ProjectForm.project_name)
    await message.answer(text_data[lang]["q_proj_name"], reply_markup=make_project_kb(lang))

@router.message(ProjectForm.project_name)
async def process_project_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(project_name=message.text)
    await state.set_state(ProjectForm.description)
    await message.answer(text_data[lang]["q_proj_desc"], reply_markup=make_project_kb(lang))

@router.message(ProjectForm.description)
async def process_description(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(description=message.text)
    await state.set_state(ProjectForm.current_stage)
    await message.answer(text_data[lang]["q_proj_stage"], reply_markup=make_project_kb(lang))

@router.message(ProjectForm.current_stage)
async def process_stage(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(current_stage=message.text)
    await state.set_state(ProjectForm.request)
    await message.answer(text_data[lang]["q_proj_req"], reply_markup=make_project_kb(lang))

@router.message(ProjectForm.request)
async def process_request(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.clear()
    lang = user_data.get("user_lang", "ru")
    user_username = f"@{message.from_user.username}" if message.from_user.username else "No username"

    notification_text = (
        "💡 **New Project Proposal!**\n\n"
        f"Project: {user_data['project_name']}\n"
        f"Description: {user_data['description']}\n"
        f"Stage: {user_data['current_stage']}\n"
        f"Request: {message.text}\n\n"
        f"Author: {user_username}"
    )

    try:
        await message.bot.send_message(chat_id=ADMIN_ID, text=notification_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error: {e}")

    from handlers.common import get_main_menu
    await message.answer(text_data[lang]["proj_success"], reply_markup=get_main_menu(lang))
