import main
from flask import Flask, render_template, request
import threading
import json

config = None
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        config['max_bot_query_length'] = int(request.form['max_bot_query_length']) or config['max_bot_query_length']
        config['max_chat_response_words'] = int(request.form['max_chat_response_words']) or config['max_chat_response_words']
        config['num_news_articles'] = int(request.form['num_news_articles']) or config['num_news_articles']
        config['custom_prompt'] = str(request.form['custom_prompt'])
    return render_template('index.html', **config)

def load_config():
    config = json.load(open('config.json'))

    return {
        'discord_token': config['discord_token'],                       #the discord app token used to join a server
        'openai_api_key': config['openai_api_key'],                     #custom instructions to be included in each chat gpt query
        'max_bot_query_length': config['max_bot_query_length'],         #character limit that defines how long of a message the bot will respond to
        'max_chat_response_words': config['max_chat_response_words'],   #max number of words for a generated chat response to contain
        'num_news_articles': config['num_news_articles'],               #number of recent news articles to return with $news command
        'custom_prompt': config['custom_prompt']                        #custom instructions to be included in each chat gpt query
    }

@app.before_first_request
def setup_background_task():
    global config
    config = load_config()
    background_thread = threading.Thread(target=lambda: main.start(config))
    background_thread.daemon = False
    background_thread.start()