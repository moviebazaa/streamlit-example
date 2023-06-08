import telebot
import pyshorteners
import time

bot_token = '5772105476:AAGXwZ6JWaEH4NFeRIg6F3oxahAgrXI2cPU'
bot = telebot.TeleBot(token=bot_token)

def short(url):
    return pyshorteners.Shortener().tinyurl.short(url)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello, world!')

@bot.message_handler(content_types=['photo', 'document'])
def file_sent(message):
    try:
        bot.send_message(message.chat.id, short(bot.get_file_url(message.document.file_id)))
    except AttributeError:
        pass

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
