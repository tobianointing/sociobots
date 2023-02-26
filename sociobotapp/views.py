import json
import os
import requests
import locale

from dotenv import load_dotenv
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot, Update
from telegram.ext import CommandHandler, Dispatcher, Filters, MessageHandler, Updater
import openai
import telegram
from twilio.twiml.messaging_response import MessagingResponse

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = os.getenv("OPENAI_API_KEY")
print(f"Api key {OPENAI_API_KEY}")

DEFAULT_MSG = """
Hey boss how you de, for any crypto info just holla me.
Just make sure your sentence start with `crypto:`.
Abeg you no go vex boss my response no go pass 30 words.
"""

# Create your views here.
@csrf_exempt
def whatsapp_bot(request):
    resp = MessagingResponse()
    msg = resp.message()
    if request.method == "POST":
        incoming_msg = request.POST.get('Body', '').lower()
        print(incoming_msg)
        resp = MessagingResponse()
        msg = resp.message()

        if 'hello' in incoming_msg:
            msg_to_send = DEFAULT_MSG
        elif "crypto" in incoming_msg:
            try:
                response = openai.Completion.create(model="text-curie-001", prompt=incoming_msg, temperature=0, max_tokens=30)
                msg_to_send = response["choices"][0]["text"]
            except:
                msg_to_send = "Boss no vex we no fit handle your request right now"
        else:
            msg_to_send = DEFAULT_MSG

        msg.body(msg_to_send)

    return HttpResponse(str(resp))



# Get API key from environment variables
TELEGRAMBOT_API_KEY = os.environ.get('TELEGRAMBOT_API_KEY')

# Create bot and dispatcher instances
bot = Bot(token=TELEGRAMBOT_API_KEY)
dispatcher = Dispatcher(bot, None, use_context=True)

# Define handler functions
@csrf_exempt
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey boss! Ask me anything about crypto.")
    
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey boss! Ask me anything about crypto.")

@csrf_exempt
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Add handlers to dispatcher
dispatcher.add_handler(MessageHandler(Filters.command, start))
dispatcher.add_handler(MessageHandler(Filters.text, echo))

# Define webhook view function
@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        update = Update.de_json(data, bot)
        dispatcher.process_update(update)
    return HttpResponse('okay')

# Set webhook
bot.setWebhook(url='https://tobianointing.pythonanywhere.com/telegram_webhook/')


COINAPI_API_KEY = os.environ.get('COINAPI_API_KEY')

def format_rate(price):
    formatted_price = locale.currency(price, grouping=True)
    return formatted_price

def get_rate(coin):
    url = f'https://rest.coinapi.io/v1/exchangerate/{coin.upper()}/USD'
    headers = {'X-CoinAPI-Key' : COINAPI_API_KEY}
    response = requests.get(url, headers=headers)
    response = response.json()
    price = response["rate"]
    price = format_rate(price)
    print(price)

get_rate("eth")