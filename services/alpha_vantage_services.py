from typing import Callable, Type
from dataclasses_json import DataClassJsonMixin
from client.alpha_vantage import AlphaVantageApiClient


class DataService:
    def __init__(self, api_client: AlphaVantageApiClient):
        self.api_client = api_client

    def fetch_and_transform_data(
        self,
        endpoint_constructor: Callable[..., str],
        model: Type[DataClassJsonMixin],
        **params,
    ) -> DataClassJsonMixin:
        return self.api_client.get_data(endpoint_constructor, model, **params)

    def get_json_response(self, data: DataClassJsonMixin) -> str:
        return data.to_json(indent=4)
