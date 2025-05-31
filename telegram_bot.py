import telebot 
import os
from dotenv import load_dotenv            #
# from config import TELEGRAM_BOT_TOKEN, GEMINI_API_TOKEN      # 
from functions import Generate
load_dotenv()                             #

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
GEMINI_API_TOKEN = os.getenv("GEMINI_API_TOKEN")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Salom men NamDU AI botman")

@bot.message_handler(func=lambda message: True)
def javob_qaytarish(message):
    user_input = message.text
    namdu = Generate(GEMINI_API_TOKEN, "namdu.json")
    response = namdu.generate(user_input)
    bot.send_message(message.chat.id, response)

print("Bot ishga tushdi")
bot.polling()