class MarketsRef:
       
    marketsDict = {

        "AEX": {

            "url": 'https://en.wikipedia.org/wiki/AEX_index',
            "symbol": 'AEX',
            "name": 'AEX',
            "api_ticker": '^AEX',
            "hash_key": 'AEX',
            "suffix": '.AS',
            "adjustments": [],
            "parser": None
        },
        
        "BEL20": {
            "url": 'https://en.wikipedia.org/wiki/BEL_20',
            "symbol": 'BEL20',
            "name": 'BEL20',
            "ticker_symbol": '^BFX',
            "suffix": '.BR',
            "adjustments": [("APAM.BR","APAM.AS")],
            "parser": "bel20_parser"
        },

        "CAC40": {
            "url": 'https://en.wikipedia.org/wiki/CAC_40',
            "symbol": 'CAC40',
            "name": 'CAC40',
            "ticker_symbol": '^FCHI',
            "suffix": '.PA',
            "adjustments": [],
            "parser": None
        },

        "DAX": {
            "url": 'https://en.wikipedia.org/wiki/DAX',
            "symbol": 'DAX',
            "name": 'DAX',
            "ticker_symbol": '^GDAXI',
            "suffix": '.DE',
            "adjustments": [],
            "parser": None
        },

        "DOWJONES": {
            "url": 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average',
            "symbol": 'DOWJONES',
            "name": 'Dow Jones',
            "ticker_symbol": '^DJI',
            "suffix": '',
            "adjustments": [],
            "parser": None
        },

        "EUROSTOXX50": {
            "url": 'https://en.wikipedia.org/wiki/EURO_STOXX_50',
            "symbol": 'EUROSTOXX50',
            "name": 'Euro Stoxx 50',
            "ticker_symbol": '^STOXX50E',
            "suffix": '',
            "adjustments": [],
            "parser": "eurostoxx50_parser"
        },

        "FTSE100": {
            "url": 'https://en.wikipedia.org/wiki/FTSE_100_Index',
            "symbol": 'FTSE100',
            "name": 'FTSE 100',
            "ticker_symbol": '^FTSE',
            "suffix": '.L',
            "adjustments": [('BT.L', 'BT-A.L')],
            "parser": "ftse100_parser"
        },

        "OMXH25": {
            "url": 'https://en.wikipedia.org/wiki/OMX_Helsinki_25',
            "symbol": 'OMXH25',
            "name": 'OMX Helsinki 25',
            "ticker_symbol": '^OMXH25',
            "suffix": '.HE',
            "adjustments": [],
            "parser": None
        },

        "OMXS30": {
            "url": 'https://en.wikipedia.org/wiki/OMX_Stockholm_30',
            "symbol": 'OMXS30',
            "name": "OMX Stockholm 30",
            "ticker_symbol": '^OMX',
            "suffix": '.ST',
            "adjustments": [],
            "parser": None
        },
    
        "IBEX35": {
            "url": 'https://en.wikipedia.org/wiki/IBEX_35',
            "symbol": 'IBEX35',
            "name": "IBEX 35",
            "ticker_symbol": '^IBEX',
            "suffix": '.MC',
            "adjustments": [],
            "parser": None
        },
        
        "MDAX": {
            "url": 'https://en.wikipedia.org/wiki/MDAX',
            "symbol": 'MDAX',
            "name": "MDAX",
            "ticker_symbol": '^MDAXI',
            "suffix": '.DE',
            "adjustments": [],
            "parser": None
        },

        "NASDAQ100": {
            "url": 'https://en.wikipedia.org/wiki/NASDAQ-100',
            "symbol": 'NASDAQ100',
            "name": "NASDAQ 100",
            "ticker_symbol": '^NDX',
            "suffix": '',
            "adjustments": [],
            "parser": None
        },

        "SP100": {
            "url": 'https://en.wikipedia.org/wiki/S%26P_100',
            "symbol": 'SP100',
            "name": 'SP 100',
            "ticker_symbol": '^OEX',
            "suffix": '',
            "adjustments": [],
            "parser": None
        },

        "SP500": {
            "url": 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
            "symbol": 'SP500',
            "name": 'SP 500',
            "ticker_symbol": '^GSPC',
            "suffix": '',
            "adjustments": [],
            "parser": None
        },

        "SW20": {
            "url": 'https://en.wikipedia.org/wiki/Swiss_Market_Index',
            "symbol": 'SW20',
            "name": 'Switzerland 20',
            "ticker_symbol": '^SSMI',
            "suffix": '.SW',
            "adjustments": [],
            "parser": None
        }

    }

    componentInfoKeys = [
        'symbol',
        'shortName', 
        'longName',  
        'trailingPegRatio',
        'askSize', 
        'marketCap', 
        #'fiftyTwoWeekLow', 
        #'fiftyTwoWeekHigh', 
        'priceToSalesTrailing12Months', 
        #'fiftyDayAverage', 
        #'twoHundredDayAverage', 
        #'trailingAnnualDividendRate', 
        'trailingAnnualDividendYield', 
        #'currency', 
        #'enterpriseValue', 
        'profitMargins', 
        'floatShares', 
        'sharesOutstanding', 
        #'heldPercentInstitutions', 
        #'impliedSharesOutstanding', 
        #'bookValue', 
        #'priceToBook', 
        #'lastFiscalYearEnd', 
        #'nextFiscalYearEnd', 
        #'mostRecentQuarter', 
        #'earningsQuarterlyGrowth', 
        'netIncomeToCommon', 
        'trailingEps', 
        'forwardEps', 
        'pegRatio', 
        #'lastSplitFactor', 
        #'lastSplitDate', 
        #'enterpriseToRevenue', 
        #'enterpriseToEbitda', 
        #'52WeekChange', 
        #'SandP52WeekChange', 
        'lastDividendValue', 
        #'lastDividendDate', 
        #'exchange', 
        #'quoteType', 
        #'underlyingSymbol', 
        #'firstTradeDateEpochUtc', 
        #'timeZoneFullName', 
        #'timeZoneShortName', 
        #'uuid', 
        #'messageBoardId', 
        #'gmtOffSetMilliseconds', 
        #'currentPrice', 
        #'targetHighPrice', 
        #'targetLowPrice', 
        #'targetMeanPrice', 
        #'targetMedianPrice', 
        #'recommendationMean', 
        #'recommendationKey', 
        #'numberOfAnalystOpinions', 
        #'totalCash', 
        #'totalCashPerShare', 
        #'ebitda', 
        #'totalDebt', 
        'quickRatio', 
        'currentRatio', 
        #'totalRevenue', 
        'debtToEquity', 
        #'revenuePerShare', 
        #'returnOnAssets', 
        #'returnOnEquity', 
        #'freeCashflow', 
        #'operatingCashflow', 
        'earningsGrowth', 
        #'revenueGrowth', 
        #'grossMargins', 
        #'ebitdaMargins', 
        #'operatingMargins', 
        #'financialCurrency'
        ]
    
    indexInfoKeys = [
        'maxAge', 
        'priceHint', 
        'previousClose', 
        'open', 
        #'dayLow', 
        #'dayHigh', 
        'regularMarketPreviousClose', 
        'regularMarketOpen', 
        'regularMarketDayLow', 
        'regularMarketDayHigh', 
        'averageVolume', 
        'averageVolume10days', 
        'averageDailyVolume10Day', 
        'fiftyTwoWeekLow', 
        'fiftyTwoWeekHigh', 
        'fiftyDayAverage', 
        'twoHundredDayAverage', 
        'currency', 
        #'exchange', 
        #'quoteType', 
        #'symbol', 
        #'underlyingSymbol', 
        #'shortName', 
        #'longName', 
        #'firstTradeDateEpochUtc', 
        #'timeZoneFullName', 
        #'timeZoneShortName', 
        #'uuid', 
        #'messageBoardId', 
        #'gmtOffSetMilliseconds', 
        'trailingPegRatio'
    ]