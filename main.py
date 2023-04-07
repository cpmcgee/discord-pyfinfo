import json
import discord
import yfinance
import textwrap

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
config = json.load(open('config.json'))
discord_token = config["discord_token"]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ticker '):
        ticker = message.content.split('$ticker ', 1)[1]
        info = get_ticker_info(ticker)
        await message.channel.send(info)


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

        return textwrap.dedent(res)
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


client.run(discord_token)