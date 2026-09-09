import json
import os
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

router = Router()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'locales.json'), 'r', encoding='utf-8') as f:
    text_data = json.load(f)

def get_text(lang: str, key: str) -> str:
    if lang not in ['ru', 'en']:
        lang = 'ru'
    return text_data[lang].get(key, text_data['ru'][key])

def get_main_menu(lang: str) -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=get_text(lang, "btn_team"))],
        [KeyboardButton(text=get_text(lang, "btn_project"))],
        [KeyboardButton(text=get_text(lang, "btn_partner"))],
        [
            KeyboardButton(text=get_text(lang, "btn_about")),
            KeyboardButton(text=get_text(lang, "btn_lang"))
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_lang_menu() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_lang = message.from_user.language_code
    if user_lang not in ['ru', 'en']:
        user_lang = 'ru'

    welcome_text = get_text(user_lang, "welcome")
    menu_text = get_text(user_lang, "main_menu")

    await message.answer(welcome_text, parse_mode="Markdown")
    await message.answer(menu_text, reply_markup=get_main_menu(user_lang))

@router.message(F.text.in_([text_data['ru']['btn_about'], text_data['en']['btn_about']]))
async def about_handler(message: Message):
    lang = 'ru' if message.text == text_data['ru']['btn_about'] else 'en'
    await message.answer(get_text(lang, "about"), parse_mode="Markdown", disable_web_page_preview=True)

@router.message(lambda message: message.text and ("Change Language" in message.text or "Сменить язык" in message.text))
async def change_lang_handler(message: Message):
    lang = 'en' if "Change Language" in message.text else 'ru'
    await message.answer(get_text(lang, "choose_lang"), reply_markup=get_lang_menu())

@router.message(F.text.in_(["🇷🇺 Русский", "🇬🇧 English"]))
async def set_lang_handler(message: Message):
    lang = 'ru' if message.text == "🇷🇺 Русский" else 'en'
    menu_text = get_text(lang, "main_menu")
    await message.answer(menu_text, reply_markup=get_main_menu(lang))
