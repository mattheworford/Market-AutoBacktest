from typing import List
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class PreviousCloseResult(DataClassJsonMixin):
    T: str
    c: float
    h: float
    l: float
    o: float
    t: int
    v: int
    vw: float


@dataclass
class PolygonDailyApiResponse(DataClassJsonMixin):
    adjusted: bool
    queryCount: int
    request_id: str
    results: List[PreviousCloseResult]
    resultsCount: int
    status: str
    ticker: str
