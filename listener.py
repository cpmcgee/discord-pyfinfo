import discord
import yfinance
import openai
from datetime import datetime
import traceback
from chains.competitive_analysis_chain import CompetitiveAnalysisChain

# Create discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Runtime config (passed from main thread)
config = None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith('$') and (len(message.content)) > config['max_bot_query_length']:
        await message.channel.send("Your message is too long.")
    elif message.content.startswith('$price '):
        symbol = message.content.split('$price ', 1)[1]
        info = get_price_info_msg(str(symbol).upper().strip())
        await message.channel.send(info)
    elif message.content.startswith('$chat '):
        query = message.content.split('$chat ', 1)[1]
        response = get_chat_response_msg(query)
        await message.channel.send(response)
    elif message.content.startswith('$news '):
        symbol = message.content.split('$news ', 1)[1]
        response = get_latest_news_msg(str(symbol).upper().strip(), config['num_news_articles'])
        await message.channel.send(**response)
    elif message.content.startswith('$ca '):
        params = message.content.split(' ', 2)
        print(params)
        symbol = str(params[1]).upper().strip()
        market = params[2]
        response = get_competitive_analysis_msg(str(symbol).upper().strip(), market)
        await message.channel.send(response)


def get_price_info_msg(symbol):
    try:
        yfticker = yfinance.Ticker(symbol)
        info = yfticker.fast_info

        last, open, high, low = format_prices(symbol, info['lastPrice'], info['open'], info['dayHigh'], info['dayLow'])

        res = f"""\
        \n{yfticker.info['shortName']}
        Last:  **{last}**
        Open: {open}
        High:  {high}
        Low:   {low}
        """

        return res
    except Exception as e:
        traceback.print_exc()
        return 'Cannot find symbol: ' + symbol.upper()


def format_prices(symbol, last, open, high, low):
    # check if symbol is crypto and not USD denominated
    is_crypto = ('-' in symbol.lower() and 'usd' not in symbol.lower())

    # round, add dollar sign if USD denominated
    last = "{:.10f}".format(last) if is_crypto else "$" + "{:.2f}".format(round(last, 2))
    open = "{:.10f}".format(open) if is_crypto else "$" + "{:.2f}".format(round(open, 2))
    high = "{:.10f}".format(high) if is_crypto else "$" + "{:.2f}".format(round(high, 2))
    low = "{:.10f}".format(low) if is_crypto else "$" + "{:.2f}".format(round(low, 2))

    return last, open, high, low


def get_chat_response_msg(query):
    try:
        custom_msg = {"role": "system", "content": config['custom_prompt']}
        system_msg = {"role": "system", "content": f"You must respond in less than {config['max_chat_response_words']} words"}
        user_msg = {"role": "user", "content": query}
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", max_tokens=int(config['max_chat_response_words']*1.25), messages=[custom_msg, system_msg, user_msg])
        return response.choices[0].message.content
    except Exception as e:
        traceback.print_exc()
        return "idk"


def get_latest_news_msg(symbol, n):
    try:
        yfticker = yfinance.Ticker(symbol)
        name = yfticker.info['shortName']
        articles = yfticker.news[0:n]
        embeds = list(map(lambda a: get_news_embed(a), articles))
        if not any(embeds):
            raise
        return {"content": "Latest news for " + name, "embeds": embeds}
    except Exception as e:
        traceback.print_exc()
        return {"content": 'Sorry, I ran into an issue pulling news articles for symbol: ' + symbol}


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


def get_competitive_analysis_msg(symbol, market):
    chain = CompetitiveAnalysisChain(ticker_symbol=symbol, product_market=market)
    msg = chain.run()['competitive_analysis']
    return msg



def start(c):
    global config
    config = c
    print('Starting discord listener')
    openai.api_key = c["openai_api_key"]
    client.run(c['discord_token'])