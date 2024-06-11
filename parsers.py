def bel20_parser(ticker_table_list, suffix):
        updated_tickers = [ticker.split(":\xa0")[1] + suffix for ticker in ticker_table_list]
        return updated_tickers

def eurostoxx50_parser(ticker_table_list, suffix):
        return ticker_table_list

def ftse100_parser(ticker_table_list, suffix):
    ticker_list = [ticker.split(".")[0] + suffix for ticker in ticker_table_list]
    return ticker_list
