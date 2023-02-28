import json
import os
import time
import locale
import requests

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
                msg_to_send = response["choices"][0]["text"].strip()
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

HELP_TEXT = """
Hello, I can help you with info about cryptos.
Here are some of the commands to get apt answers:

/price [symbol] - this is to get you the current
rate/usd of the crypto e.g /price BTC

/vol24h [symbol] - cypto volume in the last 24 hours

/vol1mth [symbol] - cypto volume in the last 1 month

/funfact [name] - gives a random fun fact about symbol. e.g /funfact bitcoin

/assets - to see list of available assets. You can get the symbols here

/help - display this help message
"""

ASSESTS = """
Bitcoin (BTC)
Ethereum (ETH)
Cardano (ADA)
Polygon (MATIC)
Dogecoin (DOGE)
Solana (SOL)
Binance Coin (BNB)
"""

COINAPI_API_KEY = os.environ.get('COINAPI_API_KEY')


def api_apdater(endpoint, callback, **kwargs):
    BASE_URL = "https://rest.coinapi.io/v1"
    url = f'{BASE_URL}/{endpoint}/'
    headers = {'X-CoinAPI-Key' : COINAPI_API_KEY}
    response = requests.get(url, headers=headers)
    print(url)
    print(dir(response))
    print(response.status_code)
    if response.status_code == 200:
        if kwargs:
            return callback(response.json(), kwargs["vol_type"])
        return callback(response.json())
    return "Sorry, we are unable to process your request right now try again later."

def get_vol(resp, vol_type):
    return format_rate(resp[0][vol_type])

def format_rate(price):
    formatted_price = locale.currency(price, grouping=True)
    return formatted_price

def get_rate(resp):
    price = resp["rate"]
    price = format_rate(price)
    return price


def handle_incoming_msg(incoming_msg):
    incoming_msg_list = incoming_msg.split(" ")
    if len(incoming_msg_list) == 2:
        symbol = incoming_msg_list[1].upper()
        return {"status": True, "msg": symbol}
    return {"status": False, "msg": "Please enter the right command. Type `/help` for help."}

    return "Please enter the right command. Type `/help` for help."

@csrf_exempt
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey boss! Ask me anything about crypto.")

@csrf_exempt
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_TEXT)

@csrf_exempt
def assests(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=ASSESTS)

@csrf_exempt
def price(update, context):
    incoming_msg = update.message.text
    resp = handle_incoming_msg(incoming_msg)
    outgoing_msg = ""
    if resp["status"]:
        symbol = resp["msg"]
        endpoint = f"exchangerate/{symbol}/USD"
        outgoing_msg = api_apdater(endpoint, get_rate)
    else:
        outgoing_msg = resp["msg"]

    context.bot.send_message(chat_id=update.effective_chat.id, text=outgoing_msg)

@csrf_exempt
def vol24h(update, context):
    incoming_msg = update.message.text
    resp = handle_incoming_msg(incoming_msg)
    outgoing_msg = ""
    if resp["status"]:
        symbol = resp["msg"]
        endpoint = f"assets/{symbol}"
        outgoing_msg = api_apdater(endpoint, get_vol, vol_type="volume_1day_usd")
    else:
        outgoing_msg = resp["msg"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=outgoing_msg)

@csrf_exempt
def vol1mth(update, context):
    incoming_msg = update.message.text
    resp = handle_incoming_msg(incoming_msg)
    outgoing_msg = ""
    if resp["status"]:
        symbol = resp["msg"]
        endpoint = f"assets/{symbol}"
        outgoing_msg = api_apdater(endpoint, get_vol, vol_type="volume_1mth_usd")
    else:
        outgoing_msg = resp["msg"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=outgoing_msg)

@csrf_exempt
def funfact(update, context):
    incoming_msg = update.message.text
    resp = handle_incoming_msg(incoming_msg)
    outgoing_msg = ""
    if resp["status"]:
        symbol = resp["msg"]
        symbol = handle_incoming_msg(incoming_msg)
        prompt = f"give one fun fact about {symbol} cryptocurrency"
        response = openai.Completion.create(model="text-curie-001", prompt=prompt, temperature=0.5, max_tokens=30)
        outgoing_msg = response["choices"][0]["text"].strip()
    else:
        outgoing_msg = resp["msg"]

    context.bot.send_message(chat_id=update.effective_chat.id, text=outgoing_msg)


@csrf_exempt
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I don't get this 😐. Type `/help` for help")

# Add handlers to dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("funfact", funfact))
dispatcher.add_handler(CommandHandler("vol24h", vol24h))
dispatcher.add_handler(CommandHandler("vol1mth", vol1mth))
dispatcher.add_handler(CommandHandler("assets", assests))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("price", price))
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



