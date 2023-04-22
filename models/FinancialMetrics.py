from dataclasses import dataclass
from datetime import date


@dataclass
class FinancialMetrics:
    asset_name: str
    symbol: str
    ttm_pe_ratio: float
    market_cap: float
    price_to_book: float
    ttm_div_yield: float
    ttm_peg_ratio: float