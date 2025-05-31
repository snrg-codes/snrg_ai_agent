import telebot.async_telebot
import os
from dotenv import load_dotenv
from functions import Generate # Assuming Generate is in functions.py
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    load_dotenv()
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    gemini_api_token = os.getenv("GEMINI_API_TOKEN")

    if not telegram_bot_token:
        logging.critical("TELEGRAM_BOT_TOKEN is not set. Exiting.")
        return
    if not gemini_api_token:
        logging.critical("GEMINI_API_TOKEN is not set. Exiting.")
        return

    bot = telebot.async_telebot.AsyncTeleBot(telegram_bot_token)
    
    # Initialize your Generate instance once if it's truly stateless
    # or handle threading if it's stateful.
    # For a read-only knowledge base, initializing once is fine.
    try:
        namdu_generator = Generate(gemini_api_token, "namdu.json")
    except Exception as e:
        logging.critical(f"Failed to initialize AI generator: {e}. Exiting.")
        return

    @bot.message_handler(commands=['start'])
    async def send_welcome(message):
        logging.info(f"Received /start from {message.chat.id}")
        await bot.send_message(message.chat.id, "Salom! Men NamDU AI botman. Savollaringizga javob berishga tayyorman.")

    @bot.message_handler(func=lambda message: True)
    async def process_user_query(message):
        user_input = message.text
        chat_id = message.chat.id
        logging.info(f"Received message from {chat_id}: {user_input}")
        
        try:
            await bot.send_chat_action(chat_id, 'typing') # Show "typing..." status
            response_text = namdu_generator.generate(user_input)
            await bot.send_message(chat_id, response_text)
        except Exception as e:
            logging.error(f"Error processing message from {chat_id}: {e}")
            await bot.send_message(chat_id, "Kechirasiz, savolingizga javob berishda xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")

    logging.info("Bot ishga tushdi. So'rovlarni kutmoqda...")
    asyncio.run(bot.polling(non_stop=True)) # non_stop=True to keep polling

if __name__ == "__main__":
    main()