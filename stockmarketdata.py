import json
import pandas as pd
import requests
import os
from dotenv import load_dotenv

class StockMarketData:
    def __init__(self, api_key) -> None:
        self.api_key = api_key

    def TIME_SERIES_INTRADAY(self, interval, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)

    def TIME_SERIES_DAILY(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()['Time Series (Daily)']
        return json.dumps(data, indent=4)
    
    def TIME_SERIES_WEEKLY(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)
    
    def TIME_SERIES_WEEKLY_ADJUSTED(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)

    def TIME_SERIES_MONTHLY(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)

    def TIME_SERIES_MONTHLY_ADJUSTED(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)

    def QUOTE_ENDPOINT(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)
    
    def TICKER_SEARCH(self, company_name):
        endpoint = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)

    def GLOBAL_MARKET_STATUS(self):
        endpoint = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)
        
    # def NEWS_AND_SENTIMENTS
    def TOP_GAINERS_AND_LOSERS(self):
        endpoint = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)
    
    def COMPANY_OVERVIEW(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)
    
    def INCOME_STATEMENT(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)
    
    def BALANCE_SHEET(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)
    
    def CASH_FLOW(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)
    
    def EARNINGS(self, symbol: str):
        endpoint = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={self.api_key}'
        data = requests.get(endpoint).json()
        return json.dumps(data, indent=4)
    
    # def LISTING_DELISTING_STATUS(self):
    #     endpoint = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={self.api_key}'
    #     data = requests.get(endpoint).json()
    #     return data
    
    # def EARNINGS_CALENDAR(self):
    #     endpoint = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={self.api_key}'
    #     data = requests.get(endpoint).json()
    #     return data
    
    # def IPO_CALENDAR(self):
    #     endpoint = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={self.api_key}'
    #     data = requests.get(endpoint).json()
    #     return data
# load_dotenv()

api_key = StockMarketData(os.getenv('API_KEY'))
smd = StockMarketData(api_key);
# print(data.TIME_SERIES_MONTHLY('AAPL'))