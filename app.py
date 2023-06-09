import listener
from flask import Flask, render_template, request
import threading
import json
import os

config = None
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    pass_attempt = request.args.get('password')
    pass_actual = config['ui_password']

    if pass_attempt == pass_actual:
        if request.method == 'POST':
            config['max_bot_query_length'] = int(request.form['max_bot_query_length']) or config['max_bot_query_length']
            config['max_chat_response_words'] = int(request.form['max_chat_response_words']) or config['max_chat_response_words']
            config['num_news_articles'] = int(request.form['num_news_articles']) or config['num_news_articles']
            config['custom_prompt'] = str(request.form['custom_prompt'])
            print('Settings updated')
        return render_template('settings.html', **config)
    else:
        return render_template('index.html')


def load_config():
    config = json.load(open('config.json'))
    os.environ["OPENAI_API_KEY"] = config['openai_api_key']

    return {
        'discord_token': config['discord_token'],
        'openai_api_key': config['openai_api_key'],
        'max_bot_query_length': config['max_bot_query_length'],
        'max_chat_response_words': config['max_chat_response_words'],
        'num_news_articles': config['num_news_articles'],
        'custom_prompt': config['custom_prompt'],
        'ui_password': config['ui_password']
    }


@app.before_first_request
def setup_listener():
    global config
    print("Loading config")
    config = load_config()
    listener_thread = threading.Thread(target=lambda: listener.start(config))
    listener_thread.daemon = False
    listener_thread.start()