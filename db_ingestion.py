import os
from services.db_services import DBService
from data_ingestion import (
    fetch_polygon_ticker_news_data,
    fetch_quandl_data,
    fetch_tiingo_data,
)
from dotenv import load_dotenv

load_dotenv()

# Initialize the data service
data_service = DBService()

# Fetch and upload Polygon news data
polygon_data = fetch_polygon_ticker_news_data()
if polygon_data is not None:
    data_service.upload_polygon_news(polygon_data)
else:
    print("No data to upload")
