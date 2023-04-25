from typing import List
import yfinance as yf
from models.valuation_metrics import ValuationMetrics
from models.price_info import PriceInfo
from models.news_article import NewsArticle
import traceback
import field_utils

def get_valuation_metrics(symbols: List[str]) -> List[ValuationMetrics]:
    try:
        yftickers = yf.Tickers(" ".join(symbols))
        return list(map(lambda t: ValuationMetrics(
            asset_name=t.info['shortName'],
            symbol=t.info['symbol'],
            ttm_pe_ratio=t.info.get('trailingPE') or 0,
            market_cap=t.info['marketCap'],
            price_to_book=t.info['priceToBook'],
            ttm_peg_ratio=t.info['trailingPegRatio']
        ), yftickers.tickers.values()))
    except:
        print("Error getting FinancialMetrics for: " + str(symbols))
        traceback.print_exc()
        return None
    

def get_price_infos(symbols: List[str]) -> List[PriceInfo]:
    try:
        yftickers = yf.Tickers(" ".join(symbols))
        return list(map(lambda t: PriceInfo(
            asset_name=t.info['shortName'],
            symbol=t.info['symbol'],
            day_last_price=t.fast_info['lastPrice'],
            day_open_price=t.fast_info['open'],
            day_low_price=t.fast_info['dayLow'],
            day_high_price=t.fast_info['dayHigh']
        ), yftickers.tickers.values()))
    except:
        print("Error getting PriceInfos for: " + str(symbols))
        traceback.print_exc()
        return None


def get_latest_news(symbol: str, n: int = 5) -> List[NewsArticle]:
    def parse_thumbnail(article):
        thumbnails = article.get('thumbnail', {}).get('resolutions', {})
        if thumbnails is not None:
            thumbnails = [t for t in thumbnails if t['tag'] == "140x140"]
            if any(thumbnails):
                thumbnail = thumbnails[0]['url']
                return thumbnail
        return None

    try:
        yfticker = yf.Ticker(symbol)
        name = yfticker.info['shortName']
        symbol = yfticker.info['symbol']
        articles = []
        for article in yfticker.news[0:n]:
            articles.append(NewsArticle(
                 asset_name=name,
                 symbol=symbol,
                 date=field_utils.get_datetime_from_unix_timestamp(article.get('providerPublishTime')),
                 title=article['title'],
                 link=article['link'],
                 thumbnail=parse_thumbnail(article)
            ))
        return articles
    except:
        print("Error getting NewsArticles for: " + symbol)
        traceback.print_exc()
        return None