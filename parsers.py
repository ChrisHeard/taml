from typing import List

def bel20_parser(ticker_table_list: List[str], suffix: str) -> List[str]:
    updated_tickers = [ticker.split(":\xa0")[1] + suffix for ticker in ticker_table_list]
    return updated_tickers

def eurostoxx50_parser(ticker_table_list: List[str], suffix: str) -> List[str]:
    return ticker_table_list

def ftse100_parser(ticker_table_list: List[str], suffix: str) -> List[str]:
    ticker_list = [ticker.split(".")[0] + suffix for ticker in ticker_table_list]
    return ticker_list
