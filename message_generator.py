import traceback
from typing import List
import discord
from chains.competitive_analysis_chain import CompetitiveAnalysisChain
import field_utils
from data_sources import data_fetcher
from models.news_article import NewsArticle
from models.price_info import PriceInfo
from models.valuation_metrics import ValuationMetrics
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage
)


# Shared config object which contains ui-modifyable runtime settings
# Will be populated on startup by listener
config = None

def get_price_info_msg(symbol: str):
    try:
        info: PriceInfo = data_fetcher.get_price_infos([symbol])[0]

        last, open, high, low = format_price_info(
            symbol, 
            info.day_last_price, 
            info.day_open_price, 
            info.day_high_price, 
            info.day_low_price
        )

        res = f"""\
        \n{info.asset_name}
        Last:  **{last}**
        Open: {open}
        High:  {high}
        Low:   {low}
        """

        return res
    except Exception as e:
        traceback.print_exc()
        return f"I ran into a problem getting price info for {symbol.upper()}"


def format_price_info(symbol: str, last: float, open: float, high: float, low: float):
    is_crypto = ('-' in symbol.lower() and 'usd' not in symbol.lower())

    if is_crypto:
        last = field_utils.format_crypto_price(last)
        open = field_utils.format_crypto_price(open)
        high = field_utils.format_crypto_price(high)
        low = field_utils.format_crypto_price(low)
        
        return last, open, high, low
    else:
        last = field_utils.format_dollar_price(last)
        open = field_utils.format_dollar_price(open)
        high = field_utils.format_dollar_price(high)
        low = field_utils.format_dollar_price(low)
        
        return last, open, high, low


def get_chat_response_msg(query: str):
    try:
        llm = ChatOpenAI(max_tokens=int(config['max_chat_response_words']*1.5))

        messages = [
            SystemMessage(content=config['custom_prompt']),
            SystemMessage(content=f"You must respond in less than {config['max_chat_response_words']} words"),
            HumanMessage(content=query)
        ]
        response = llm(messages).content
        return response
    except:
        traceback.print_exc()
        return "I ran into a problem processing your request."


def get_latest_news_msg(symbol: str, n: int):
    try:
        articles: List[NewsArticle] = data_fetcher.get_latest_news(symbol, n)
        
        embeds = list(map(lambda a: discord.Embed(
            title=a.title, 
            url=a.link), 
        articles))

        if not any(embeds):
            raise
        
        return {"content": "Latest news for " + articles[0].asset_name, "embeds": embeds}
    except:
        traceback.print_exc()
        return {"content": f"I ran into a problem pulling news articles for symbol {symbol.upper()}"}


def get_competitive_analysis_msg(symbol, market):
    try:
        chain = CompetitiveAnalysisChain(ticker_symbol=symbol, product_market=market)
        msg = chain.run({"ticker_symbol": symbol, "product_market": market})
        return msg
    except:
        traceback.print_exc()
        return f"I ran into a problem getting competitive analysis for {symbol} in {market}"


def get_valuation_metrics_msg(symbol):
    try:
        info: ValuationMetrics = data_fetcher.get_valuation_metrics([symbol])[0]

        res = f"""\
        \n{info.asset_name}
        Market Cap: {field_utils.format_dollar_price(info.market_cap)}
        Price/Book: {field_utils.format_two_decimals(info.price_to_book)}
        P/E Ratio (TTM):  {field_utils.format_two_decimals(info.ttm_pe_ratio)}
        PEG Ratio (TTM): {field_utils.format_two_decimals(info.ttm_peg_ratio)}
        """

        return res
    except:
        traceback.print_exc()
        return f"I ran into a problem getting price info for {symbol.upper()}"