# client/alpha_vantage.py
import requests
from typing import Dict, Type, TypeVar, Callable
from dataclasses_json import DataClassJsonMixin

T = TypeVar('T', bound=DataClassJsonMixin)

class AlphaVantageApiClient:
    def __init__(self, key: str, base_url: str) -> None:
        self.base_url = base_url
        self.key = key

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Authorization": f'Bearer {self.key}' if self.key else ''
        }
        return headers

    def get_data(self, endpoint_constructor: Callable[..., str], model: Type[T], **params) -> T:
        endpoint = endpoint_constructor(**params)
        response = requests.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return model.from_json(response.text)