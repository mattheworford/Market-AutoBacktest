from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PolygonNewsData:
    article_id: str
    publisher_name: str
    publisher_homepage: str
    publisher_logo: str
    publisher_favicon: str
    title: str
    author: str
    published_date: str
    article_url: str
    related_tickers: List[str]
    image_url: str
    description: str
    keywords: List[str]
    insights: List[Dict[str, str]]
