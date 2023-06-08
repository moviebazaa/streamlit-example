import telebot

bot = '5772105476:AAGXwZ6JWaEH4NFeRIg6F3oxahAgrXI2cPU'
bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands['start'])
def send_welcome(message):
    bot.replay_to(message, 'hello world')

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
