from dataclasses import dataclass
from datetime import date


@dataclass
class NewsArticle:
    asset_name: str
    symbol: str
    date: date
    title: str
    link: str
    thumbnail: str