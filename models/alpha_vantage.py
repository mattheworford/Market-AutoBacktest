from typing import Dict
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config


@dataclass
class MetaData(DataClassJsonMixin):
    information: str = field(metadata=config(field_name="1. Information"))
    symbol: str = field(metadata=config(field_name="2. Symbol"))
    last_refreshed: str = field(metadata=config(field_name="3. Last Refreshed"))
    output_size: str = field(metadata=config(field_name="4. Output Size"))
    time_zone: str = field(metadata=config(field_name="5. Time Zone"))


@dataclass
class TimeSeriesDaily(DataClassJsonMixin):
    open: str = field(metadata=config(field_name="1. open"))
    high: str = field(metadata=config(field_name="2. high"))
    low: str = field(metadata=config(field_name="3. low"))
    close: str = field(metadata=config(field_name="4. close"))
    volume: str = field(metadata=config(field_name="5. volume"))


@dataclass
class AlphaVantageResponse(DataClassJsonMixin):
    meta_data: MetaData = field(metadata=config(field_name="Meta Data"))
    time_series_daily: Dict[str, TimeSeriesDaily] = field(
        default_factory=dict, metadata=config(field_name="Time Series (Daily)")
    )
