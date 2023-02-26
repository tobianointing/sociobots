import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAMBOT_API_KEY = os.environ.get('TELEGRAMBOT_API_KEY')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot.")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main():
    updater = Updater(token=TELEGRAMBOT_API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                      port=8000,
                      url_path=TELEGRAMBOT_API_KEY)
    updater.bot.setWebhook(url=f'https://YOUR_DOMAIN/{TELEGRAMBOT_API_KEY}')


if __name__ == '__main__':
    main()
