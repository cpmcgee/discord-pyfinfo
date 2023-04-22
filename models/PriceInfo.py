from dataclasses import dataclass
from datetime import date


@dataclass
class PriceInfo:
    asset_name: str
    symbol: str
    day_last_price: float
    day_open_price: float
    day_high_price: float
    day_low_price: float