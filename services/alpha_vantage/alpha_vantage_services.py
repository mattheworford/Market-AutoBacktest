# services/data_service.py
from typing import Callable, Type
from dataclasses_json import DataClassJsonMixin
from client.alpha_vantage import AlphaVantageApiClient

<<<<<<< Updated upstream:services/alpha_vantage/alpha_vantage_services.py
class DataService:
    def __init__(self, api_client: AlphaVantageApiClient):
        self.api_client = api_client

    def fetch_and_transform_data(self, endpoint_constructor: Callable[..., str], model: Type[DataClassJsonMixin], **params) -> DataClassJsonMixin:
=======

class AlphaVantanageDataService:
    def __init__(self, api_client: AlphaVantageApiClient):
        self.api_client = api_client

    def fetch_data_with_endpoint(
        self,
        endpoint_constructor: Callable[..., str],
        model: Type[DataClassJsonMixin],
        **params,
    ) -> DataClassJsonMixin:
>>>>>>> Stashed changes:services/alpha_vantage_services.py
        return self.api_client.get_data(endpoint_constructor, model, **params)

    def get_json_response(self, data: DataClassJsonMixin) -> str:
        return data.to_json(indent=4)
