# PyFInfo  
This is a simple discord bot powered by Yahoo Finance and ChatGPT.  
  
Currently, this provides simple ticker info and a chat interface. Future plans consist of ChatGPT generated responses which provide insight to requested market data.  

## Getting Started  
- Install python3 https://www.python.org/downloads/
- Install dependencies
	- `pip install discord.py`
	- `pip install yfinance`
	- `pip install openai`
- Add bot to your server: https://discordpy.readthedocs.io/en/stable/discord.html
	- Make sure to save the token generated during this process
- Generate an OpenAI API Key https://platform.openai.com/account/api-keys
- Populate config.json with these values
- Run the bot
	- `python main.py`

## Example Usage  
Get stock market info:  
>$ticker SPY

Get crypto info (USD or crypto denominated):  
>$ticker BTC-USD  
>$ticker ETH-BTC  
  
ChatGPT query:  
>$chat What is bitcoin?  
>$chat How is Earnings Per Share calculated?