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
    elif message.content.startswith('$') and (len(message.content)) > 200:
        await message.channel.send("idk")
    elif message.content.startswith('$ticker '):
        ticker = message.content.split('$ticker ', 1)[1]
        info = get_ticker_info(ticker)
        await message.channel.send(info)
    elif message.content.startswith('$chat '):
        query = message.content.split('$chat ', 1)[1]
        response = get_chat_response(query)
        await message.channel.send(response)
    elif message.content.startswith('$news '):
        ticker = message.content.split('$news ', 1)[1]
        response = get_latest_news(ticker, 5)
        await message.channel.send(**response)



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
    except:
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
        system_msg = {"role": "system", "content": "You must respond in less than 50 words"}
        user_msg = {"role": "user", "content": query}
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", max_tokens=65, messages=[system_msg, user_msg])
        return response.choices[0].message.content
    except:
        return "idk"
    
def get_latest_news(ticker, n):
    try:
        yfticker = yfinance.Ticker(ticker.strip())
        name = yfticker.info['shortName']
        articles = yfticker.news[0:n]
        embeds = list(map(lambda a: get_news_embed(a), articles))
        if not any(embeds):
            raise
        return {"content": "Latest news for " + name, "embeds": embeds}
    except:
        return {"content": 'Could not find news articles for ticker: ' + ticker.upper()}
    
def get_news_embed(article):
    embed = discord.Embed(title=article['title'], url=article['link'])

    ## Adding thumbnails takes up a lot of space in the chat, may re-enable after further command parameterization
    # thumbnails = article.get('thumbnail', {}).get('resolutions', {})
    # if thumbnails is not None:
    #     thumbnails = [t for t in thumbnails if t['tag'] == "140x140"]
    #     if any(thumbnails):
    #         thumbnail = thumbnails[0]['url']
    #         print(thumbnail)
    #         embed.set_thumbnail(url=thumbnail)
    
    return embed

def start():
    client.run(discord_token)

if __name__ == "__main__":
    start()
