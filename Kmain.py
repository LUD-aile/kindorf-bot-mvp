import os
import telebot
from telebot import types
import json

USER_LANGUAGES = {}  

TOKEN = os.getenv("BOT_TOKEN", "ТВОЙ_ТОКЕН_БОТА")
bot = telebot.TeleBot(TOKEN)

def load_locales():
    with open("locales.json", "r", encoding="utf-8") as f:
        return json.load(f)

LOCALES = load_locales()

def lang(chat_id):
    return USER_LANGUAGES.get(chat_id, 'ru')

def get_text(chat_id, key):
    user_lang = lang(chat_id)
    return LOCALES.get(user_lang, LOCALES['ru']).get(key, key)

def main_menu(chat_id):
    user_lang = lang(chat_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn_team = types.KeyboardButton(get_text(chat_id, "btn_join_team"))
    btn_settings = types.KeyboardButton(get_text(chat_id, "btn_settings"))
    markup.add(btn_team, btn_settings)
    
    bot.send_message(chat_id, get_text(chat_id, "welcome_back"), reply_markup=markup)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    btn_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_query_data="set_lang_ru")
    btn_en = types.InlineKeyboardButton("🇬🇧 English", callback_query_data="set_lang_en")
    markup.add(btn_ru, btn_en)
    bot.send_message(chat_id, "Выберите язык / Choose language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["set_lang_ru", "set_lang_en"])
def handle_language_change(call):
    chat_id = call.message.chat.id
    if call.data == "set_lang_ru":
        USER_LANGUAGES[chat_id] = 'ru'
        bot.answer_callback_query(call.id, "Язык изменен на Русский")
    elif call.data == "set_lang_en":
        USER_LANGUAGES[chat_id] = 'en'
        bot.answer_callback_query(call.id, "Language changed to English")
    
    main_menu(chat_id)

import handlers.team as team_handler
team_handler.register_handlers(bot, get_text, main_menu)

if __name__ == "__main__":
    print("Бот успешно запущен...")
    bot.polling(none_stop=True)
