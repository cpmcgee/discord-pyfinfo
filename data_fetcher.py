
from typing import List
import yfinance as yf
from models.FinancialMetrics import FinancialMetrics
from models.PriceInfo import PriceInfo
import traceback

def get_financial_metrics(symbols: List[str]) -> List[FinancialMetrics]:
    try:
        yftickers = yf.Tickers(" ".join(symbols))
        return list(map(lambda t: FinancialMetrics(
            asset_name=t.info['shortName'],
            symbol=t.info['symbol'],
            ttm_pe_ratio=t.info['trailingPE'],
            market_cap=t.info['marketCap'],
            price_to_book=t.info['priceToBook'],
            ttm_div_yield=t.info['trailingAnnualDividendYield'],
            ttm_peg_ratio=t.info['trailingPegRatio']
        )), yftickers.tickers.values())
    except:
        print("Error getting FinancialMetrics for: " + symbols)
        traceback.print_exc()
        return None
    

def get_price_infos(symbols: List[str]) -> List[PriceInfo]:
    try:
        yftickers = yf.Tickers(" ".join(symbols))
        return list(map(lambda t: PriceInfo(
            asset_name=t.info['shortName'],
            symbol=t.info['symbol'],
            day_last_price=t.info['lastPrice'],
            day_open_price=t.info['open'],
            day_low_price=t.info['dayLow'],
            day_high_price=t.info['dayHigh'],
        )), yftickers.tickers.values())
    except:
        print("Error getting PriceInfos for: " + symbols)
        traceback.print_exc()
        return None