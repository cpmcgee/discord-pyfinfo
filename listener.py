import discord
import message_generator


# Runtime config (passed from main thread)
config = None

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

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
        info = message_generator.get_price_info_msg(str(symbol).upper().strip())
        await message.channel.send(info)
    elif message.content.startswith('$chat '):
        query = message.content.split('$chat ', 1)[1]
        response = message_generator.get_chat_response_msg(query)
        await message.channel.send(response)
    elif message.content.startswith('$news '):
        symbol = message.content.split('$news ', 1)[1]
        response = message_generator.get_latest_news_msg(str(symbol).upper().strip(), config['num_news_articles'])
        await message.channel.send(**response)
    elif message.content.startswith('$ca '):
        params = message.content.split(' ', 2)
        symbol = str(params[1]).upper().strip()
        market = params[2]
        response = message_generator.get_competitive_analysis_msg(symbol, market)
        await message.channel.send(response)
    elif message.content.startswith('$val '):
        symbol = message.content.split('$val ', 1)[1]
        response = message_generator.get_valuation_metrics_msg(symbol)
        await message.channel.send(response)

def start(c):

    global config
    config = c
    message_generator.config = c
    
    print('Starting discord listener')
    global client
    client.run(config['discord_token'])