from typing import List, Optional
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class Result(DataClassJsonMixin):
    c: float
    h: float
    l: float
    n: int
    o: float
    t: int
    v: int
    vw: float


@dataclass
class PolygonAggregatesResponse(DataClassJsonMixin):
    adjusted: bool
    queryCount: int
    request_id: str
    results: List[Result]
    resultsCount: int
    status: str
    ticker: str
    next_url: Optional[str] = None
