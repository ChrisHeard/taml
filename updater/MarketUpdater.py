from backend.static.MarketsRef import MarketsRef
from backend.utils.RedisManager import RedisManager
from backend.utils.CustomLogger import CustomLogger
from bs4 import BeautifulSoup as bs, ResultSet
import pandas as pd 
import re
import requests
import yfinance as yf
from io import StringIO
from typing import List, Any, Optional, Dict, Callable



class MarketUpdater:

    redis: RedisManager
    cache: MarketsRef
    logger: CustomLogger

    active_dict: Optional[Dict[str,Any]]

    
    
    def __init__(self) -> None:

        self.redis = RedisManager()
        self.cache = MarketsRef()
        self.logger = CustomLogger()

        self.active_dict = None

        self.PARSER_REGISTRY: Dict[str, Callable[[List[str], str], List[str]]] = {
            "bel20_parser": self.bel20_parser,
            "eurostoxx50_parser": self.eurostoxx50_parser,
            "ftse100_parser": self.ftse100_parser
        }


    async def update_links(self, a_dict) -> None:
        self.logger.info(f"Attempting to update 'links' for {a_dict['symbol']}.")
        new_linked_components = await self.__get_linked_components(a_dict)
        await self.redis.store_py_obj("links", a_dict['symbol'], new_linked_components)
        self.logger.info(f"Successfully updated 'links' for {a_dict['symbol']}.")

    async def update_components(self, a_dict) -> None:
        self.logger.info(f"Attempting to update 'components' for {a_dict['symbol']}.")
        new_components_data = await self.__get_components_data(a_dict)
        await self.redis.store_py_obj('components',a_dict['symbol'], new_components_data)
        self.logger.info(f"Successfully updated 'components' for {a_dict['symbol']}.")

    async def update_index(self, a_dict) -> None:
        self.logger.info(f"Attempting to update 'index' for {a_dict['symbol']}.")
        new_index_data = await self.__get_index_dict(a_dict)
        await self.redis.store_py_obj('indices', a_dict['symbol'], new_index_data)
        self.logger.info(f"Successfully updated 'index' for {a_dict['symbol']}.")

    async def update_all(self, id=None, a_dict=None) -> None:

        if id:
            a_dict = self.cache.marketsDict[id]
        if a_dict:
            await self.update_links(a_dict)
            await self.update_index(a_dict)
            await self.update_components(a_dict)
        else:
            ValueError("MarketUpdater update_all() was called but no market id or dictionary was provided.")

    async def __get_linked_components(self, a_dict) -> List[str]:

        '''
        Returns a list of all the components stock tickers for an input market ETF

        e.g. input "FTSE100" -> output ["ticker1", "ticker2"...]
        '''

        def __read_html_table_str(table,a_dict) -> List[str]:
            df = pd.read_html(StringIO(str(table)))[0]
            df.columns = pd.Index([str(col) for col in df.columns])
            ticker_col = next((col for col in df.columns if re.search(r'Ticker|Symbol', col, re.IGNORECASE)), None)
            if ticker_col:
                ticker_table_list = df[ticker_col].astype(str).tolist()
                parser = __get_parser(a_dict)
                if parser:
                    return parser(ticker_table_list, a_dict['suffix'])
                else:
                    ticker_split_list = [ticker.split(".")[0] for ticker in ticker_table_list]
                    ticker_hyphen_list = [ticker.replace(" ", "-") for ticker in ticker_split_list]
                    return [ticker + a_dict['suffix'] for ticker in ticker_hyphen_list]
            return []
        
        def __get_html_tables(url: str) -> ResultSet[Any]:

            response = requests.get(url)
            html_content = response.content
            soup = bs(html_content, 'html.parser')
            tables = soup.find_all('table')
            return tables
        
        def __get_components_list_from_html(a_dict):
            tables = __get_html_tables(a_dict['url'])
            for table in tables:
                components_list = __read_html_table_str(table, a_dict)
                if components_list:
                    return components_list

        def __adjust_components_list(components_list: List[str]) -> List[str]:

            if self.active_dict:
                adjustments_dict = dict(self.active_dict['adjustments'])
            else:
                print("An operation was attempted with a dict that doesnt exist in __adjust_components_list")

            return [adjustments_dict.get(component, component) for component in components_list]

        def __get_parser(a_dict: dict) -> Optional[Callable[[List[str], str], List[str]]]:
            
            parser_name = a_dict['parser']

            if parser_name:
                parser_func = self.PARSER_REGISTRY.get(parser_name)
                if parser_func:
                    return parser_func
                else:
                    raise ValueError(f"Parser for {self.cache.marketsDict['id']} could not be found in PARSER_REGISTRY. Ensure that the parser string reference is named \"{self.cache.marketsDict['id']}_parser\" or set the parser bool to False.")
            return None

       
        _components_list = __get_components_list_from_html(a_dict)

        _adjusted_list = __adjust_components_list(_components_list)

        return _adjusted_list

    async def __get_index_dict(self, a_dict) -> Dict[str, Any]:
        yf_dict = yf.Ticker(a_dict['api_ticker']).info
        return {"id": a_dict['symbol'], **{key: yf_dict.get(key, "") for key in self.cache.indexInfoKeys}}
    
    async def __get_components_data(self, a_dict) -> Optional[List[Dict[str, Any]]]:

        def __component_data_api_call(component: str) -> Dict[str, Any]:
            try:
                info = yf.Ticker(component).info
                return {key: info.get(key, "") for key in self.cache.componentInfoKeys}
            except Exception as e:
                print(e)
                raise ValueError(f'API call for {component} during the components data update process failed. Please check the components ticker symbol for validity within the {a_dict['symbol']} key. Manually adjusting the ticker symbol in the market\'s \'adjustments\' field may be required')


        linked_components = await self.redis.get_py_obj('links', a_dict['symbol'])

        if linked_components:
            return [__component_data_api_call(component) for component in linked_components]
        else:
            return None
        
    def bel20_parser(self, ticker_table_list: List[str], suffix: str) -> List[str]:
        updated_tickers = [ticker.split(":\xa0")[1] + suffix for ticker in ticker_table_list]
        return updated_tickers

    def eurostoxx50_parser(self, ticker_table_list: List[str], suffix: str) -> List[str]:
        return ticker_table_list

    def ftse100_parser(self, ticker_table_list: List[str], suffix: str) -> List[str]:
        ticker_list = [ticker.split(".")[0] + suffix for ticker in ticker_table_list]
        return ticker_list