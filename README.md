# PyFInfo  
This is a simple discord bot powered by Yahoo Finance and OpenAI.  

## Getting Started  
- Install python3 https://www.python.org/downloads/
- Install dependencies
	- `pip install -r requirements.txt`
- Add bot to your discord server: https://discordpy.readthedocs.io/en/stable/discord.html
	- Make sure to save the token generated during this process
- Generate an OpenAI API Key https://platform.openai.com/account/api-keys
- Create and populate config.json
	- See Config section below
- Run the application
	- `flask run`
- Visit the flask server URL once to start the bot

## Config
Configuration is handled by a `config.json` file at the root level of the repo. This will need to be created.

- discord_token - the token used to log the bot into discord
- openai_api_key - api key for accessing chat gpt
- max_bot_query_length - character limit that defines how long of a message the bot will respond to
- max_chat_response_words - max number of words for a generated chat response to contain
- num_news_articles - number of recent news articles to return with $news command
- custom_prompt - custom instructions to be included in each chat gpt query
- ui_password - password used to access the settings UI

#### Example config.json
```
{
  "discord_token": "asdf1234",
  "openai_api_key": "1234asdf",
  "max_bot_query_length": 200,
  "max_chat_response_words": 50,
  "num_news_articles": 5,
  "custom_prompt": "Keep responses less than 100 words",
  "ui_password": "4321"
}
```

## Example Usage  
Get price info of a traditional asset:
>$price {ticker}  
>$price SPY

Get price info for a crypto asset (USD or crypto denominated):  
>$price {base-quote}  
>$price BTC-USD  
>$price ETH-BTC

Get latest news articles (this is somewhat buggy due to pyfinance limitations)
>$news {ticker}  
>$news MSFT

General GPT query:  
>$chat {query}  
>$chat What is bitcoin?  
>$chat How is Earnings Per Share calculated?

Simple valuation metrics:  
>$val {ticker}  
>$val MSFT

Simple competitive analysis (needs tuning. traditional assets only):
>$ca {ticker} {market}  
>$ca msft cloud computing

## Settings UI
The settings UI can be accessed by visiting the url of the flask server and providing a `password` query parameter.

Example:
`http://localhost:5000?password=secret`

![Alt text](/static/settings_ui.jpg?raw=true)