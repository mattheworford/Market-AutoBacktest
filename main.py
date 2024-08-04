import os
from dotenv import load_dotenv
from utils.config import API_KEY, BASE_URL, SYMBOL
from client.alpha_vantage import AlphaVantageApiClient
from services.alpha_vantage_services import DataService
from utils.api_constructor_utils import AlphaVantageApiConstructor
from models.alpha_vantage import AlphaVantageResponse

def main():
    try:
        client = AlphaVantageApiClient(key=API_KEY, base_url=BASE_URL)
        data_service = DataService(api_client=client)
        api_constructor = AlphaVantageApiConstructor(base_url=BASE_URL)

        endpoint_constructor = api_constructor.construct_time_series_daily_endpoint
        data = data_service.fetch_and_transform_data(endpoint_constructor, AlphaVantageResponse, symbol=SYMBOL, api_key=API_KEY)
        print(data_service.get_json_response(data))
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
