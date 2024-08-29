from dataclasses import dataclass
from typing import Optional


@dataclass
class TiingoData:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: Optional[float] = None
    adjusted_high: Optional[float] = None
    adjusted_low: Optional[float] = None
    adjusted_open: Optional[float] = None
    adjusted_volume: Optional[int] = None
    ex_dividend: Optional[float] = None
    split_ratio: Optional[float] = None
