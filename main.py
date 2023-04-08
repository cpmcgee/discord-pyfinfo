import json
import discord
import yfinance
import openai

# Create discord client
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Read in config
config = json.load(open('config.json'))
discord_token = config["discord_token"]
openai.api_key = config["openai_api_key"]


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif len(message.content) > 100:
        await message.channel.send("idk")
    elif message.content.startswith('$ticker '):
        ticker = message.content.split('$ticker ', 1)[1]
        info = get_ticker_info(ticker)
        await message.channel.send(info)
    elif message.content.startswith('$chat '):
        query = message.content.split('$chat ', 1)[1]
        response = get_chat_response(query)
        await message.channel.send(response)


def get_ticker_info(ticker):
    try:
        ticker = ticker.strip()
        info = yfinance.Ticker(ticker).fast_info

        last, open, high, low = format_prices(ticker, info['lastPrice'], info['open'], info['dayHigh'], info['dayLow'])

        res = f"""\
        \n{ticker.upper()}
        Last:  **{last}**
        Open: {open}
        High:  {high}
        Low:   {low}
        """

        return res
    except KeyError:
        return 'Cannot find ticker: ' + ticker.upper()


def format_prices(ticker, last, open, high, low):
    # check if ticker is crypto and not USD denominated
    is_crypto = ('-' in ticker.lower() and 'usd' not in ticker.lower())

    # round, add dollar sign if USD denominated
    last = "{:.10f}".format(last) if is_crypto else "$" + "{:.2f}".format(round(last, 2))
    open = "{:.10f}".format(open) if is_crypto else "$" + "{:.2f}".format(round(open, 2))
    high = "{:.10f}".format(high) if is_crypto else "$" + "{:.2f}".format(round(high, 2))
    low = "{:.10f}".format(low) if is_crypto else "$" + "{:.2f}".format(round(low, 2))

    return last, open, high, low


def get_chat_response(query):
    try:
        system_msg = {"role": "system", "content": "You must respond in less than 35 words"}
        user_msg = {"role": "user", "content": query}
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", max_tokens=50, messages=[system_msg, user_msg])
        return response.choices[0].message.content
    except:
        return "idk"


if __name__ == "__main__":
    client.run(discord_token)
