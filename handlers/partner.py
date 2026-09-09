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

class PartnerForm(StatesGroup):
    company_name = State()
    proposal = State()

def make_partner_kb(lang: str = "ru") -> ReplyKeyboardMarkup:
    cancel_text = text_data[lang]["btn_cancel"]
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=cancel_text)]], resize_keyboard=True)

@router.message(F.text.in_([text_data['ru']['btn_cancel'], text_data['en']['btn_cancel']]), PartnerForm)
async def cancel_partner_form(message: Message, state: FSMContext):
    await state.clear()
    user_lang = message.from_user.language_code
    lang = user_lang if user_lang in ['ru', 'en'] else 'ru'
    from handlers.common import get_main_menu, get_text
    await message.answer(get_text(lang, "main_menu"), reply_markup=get_main_menu(lang))

@router.message(F.text.in_(["💎 Партнерство", "💎 Partnership Proposal"]))
async def start_partner_form(message: Message, state: FSMContext):
    lang = "en" if "Partnership Proposal" in message.text else "ru"
    await state.update_data(user_lang=lang)
    await state.set_state(PartnerForm.company_name)
    await message.answer(text_data[lang]["q_part_name"], reply_markup=make_partner_kb(lang))

@router.message(PartnerForm.company_name)
async def process_company(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("user_lang", "ru")
    await state.update_data(company_name=message.text)
    await state.set_state(PartnerForm.proposal)
    await message.answer(text_data[lang]["q_part_prop"], reply_markup=make_partner_kb(lang))

@router.message(PartnerForm.proposal)
async def process_proposal(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await state.clear()
    lang = user_data.get("user_lang", "ru")
    user_username = f"@{message.from_user.username}" if message.from_user.username else "No username"

    notification_text = (
        "💎 **New Partnership Proposal!**\n\n"
        f"Company: {user_data['company_name']}\n"
        f"Proposal: {message.text}\n\n"
        f"Contact: {user_username}"
    )

    try:
        await message.bot.send_message(chat_id=ADMIN_ID, text=notification_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error: {e}")

    from handlers.common import get_main_menu
    await message.answer(text_data[lang]["part_success"], reply_markup=get_main_menu(lang))
