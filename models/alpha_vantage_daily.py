from typing import Dict
from dataclasses import dataclass


@dataclass
class AlphaVantageData:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
