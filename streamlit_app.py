import telebot

bot_token = '5772105476:AAGXwZ6JWaEH4NFeRIg6F3oxahAgrXI2cPU'
bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello! Send me a file, and I will provide you with a direct download link.')

@bot.message_handler(content_types=['document'])
def file_sent(message):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file_link = bot.get_file_url(file_id)
    bot.send_message(message.chat.id, f"Download link for {file_name}: {file_link}")

bot.polling()
