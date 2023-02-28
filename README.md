# WhatsAppBot and TelegramBot

This project consists of two chatbots: a WhatsAppBot and a TelegramBot. The bots provide information about cryptocurrencies, including their current rates, volumes, and fun facts.

## TelegramBot

The TelegramBot provides the following commands:

- `/price [symbol]`: Gets the current rate/USD of the specified cryptocurrency. Example: `/price BTC`.
- `/vol24h [symbol]`: Gets the 24-hour trading volume of the specified cryptocurrency.
- `/vol1mth [symbol]`: Gets the trading volume of the specified cryptocurrency in the last month.
- `/funfact [name]`: Gives a random fun fact about the specified cryptocurrency. Example: `/funfact bitcoin`.
- `/assets`: Shows a list of available assets and their symbols.
- `/help`: Displays this help message.

To use the TelegramBot, you need to provide the following secret keys:

- `OPENAI_API_KEY`: API key for OpenAI's services.
- `TELEGRAMBOT_API_KEY`: API key for Telegram's Bot API.
- `COINAPI_API_KEY`: API key for CoinAPI's services.

## WhatsAppBot

The WhatsAppBot uses Twilio's Programmable Messaging API to provide the same cryptocurrency information as the TelegramBot. To use the WhatsAppBot, you need to set up a Twilio account and provide the following information:

- `TWILIO_ACCOUNT_SID`: Your Twilio account SID.
- `TWILIO_AUTH_TOKEN`: Your Twilio account authentication token.
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number.

## Installation
To install the bot, follow these steps:

- Clone this repository to your local machine.
- Install the required Python packages by running pip install -r requirements.txt in the root directory of the project.
- Obtain an API keys. Check `env_example` file.
- Run the development server: `python manage.py runserver`
- Deploy site to pythonanywhere.com

## Usage

To use the bots, simply send a message with one of the commands to the corresponding bot (either on WhatsApp or Telegram).

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgments

This project was a mini task assigned to me by my boss, Michael, to test my skills on a larger project in the same field. It was made possible thanks to the services provided by OpenAI, Telegram, CoinAPI, and Twilio.
