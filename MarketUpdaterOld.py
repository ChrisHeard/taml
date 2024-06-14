from typing import List, Dict, Any
from datetime import datetime, timedelta
from GLOBALS import GLOBALS as GB
from MarketsRef import MarketsRef as MR
from io import StringIO
import pandas as pd
import re
import yfinance as yf 
import utils
import logging
from Market import Market

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketUpdater(Market):

    def __init__(self, id: str):
        super().__init__(id)

    def check_update_req(self, table):

        hash_key = f'{table}:{self.id}'

        try:
            if self.client.exists(hash_key):
                timestamp_log = [field.decode('utf-8') for field in self.client.hkeys(hash_key)]
                timestamp_log_datetimes = [datetime.strptime(ts, GB.REDIS_TIMESTAMP_FORMAT) for ts in timestamp_log]
                most_recent_datetime = max(timestamp_log_datetimes)
                time_difference = self.dt_now - most_recent_datetime

                if time_difference > timedelta(days=GB.REDIS_DATA_EXPIRATION_TIMER):
                    print(f'{hash_key} data has expired and will be updated.')
                    return True
                else:
                    print(f'{hash_key} data has not yet expired and will not update.')
                    return False
            else:
                print(f"The key '{hash_key}' does not exist and will be initialized.")
                return True
        except TypeError as e:
            print(f"TypeError: {e}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def update_all(self) -> None:
        
        self.dt_now = datetime.now()

        if self.check_update_req('index'):
            self.update_index()

        if self.check_update_req('components'):
            self.update_components()
        
        if self.check_update_req('links'):
            self.update_links()

    def update_index(self) -> None:
        new_index_data = self.__get_index_dict()
        utils.redis_store_py_obj(self.client, self.index_hash, new_index_data, self.dt_now)

    def update_components(self) -> None:
        new_components_data = self.__get_components_data()
        utils.redis_store_py_obj(self.client, self.components_hash, new_components_data, self.dt_now)

    def update_links(self) -> None:
        new_linked_components = self.__get_linked_components()
        utils.redis_store_py_obj(self.client, self.link_hash, new_linked_components, self.dt_now)

    def __get_components_data(self) -> List[Dict[str, Any]]:

        def __component_data_api_call(component):
            try:
                info = yf.Ticker(component).info
                company_info = {key: info.get(key, "") for key in MR.componentInfoKeys}
                return company_info
            except Exception as e:
                print(e)
                raise ValueError(f'API call for {component} during the components data update process failed. Please check the components ticker symbol for validity within the {self.id} key. Manually adjusting the ticker symbol in the market\'s \'adjustments\' field may be required')

        components_data = [__component_data_api_call(component) for component in self.link_ref]
        return components_data

    def __get_index_dict(self) -> Dict[str, Any]:
        yf_dict = yf.Ticker(self.api_ticker).info
        norm_dict = {key: yf_dict.get(key, "") for key in MR.indexInfoKeys}
        index_dict = {"id": self.id, **norm_dict}
        return index_dict
    
    def __get_linked_components(self) -> List[str]:

        def __read_html_table_str(table, custom_parser, suffix) -> List[str]:

            df = pd.read_html(StringIO(str(table)))[0]
            df.columns = [str(col) for col in df.columns]
            ticker_col = next((col for col in df.columns if re.search(r'Ticker|Symbol', col, re.IGNORECASE)), None)
            if ticker_col:
                ticker_table_list = df[ticker_col].astype(str).tolist()
                if custom_parser:
                    ticker_list = custom_parser(ticker_table_list, suffix)
                else:
                    ticker_split_list = [ticker.split(".")[0] for ticker in ticker_table_list]
                    ticker_hyphen_list = [ticker.replace(" ","-") for ticker in ticker_split_list]
                    ticker_list = [ticker + suffix for ticker in ticker_hyphen_list]

            return ticker_list
            
           
          

        def __get_components_list_from_html():
            tables = utils.get_html_tables(self.reference_url)
            parser = self.parser if self.parser else None

            for table in tables:
                components_list = __read_html_table_str(table, parser, self.suffix)
                if components_list:
                    return components_list
                

        def __adjust_components_list(components_list: List[str]):
            adjustments_dict = dict(self.adjustments)
            adjusted_components_list = [adjustments_dict.get(component, component) for component in components_list]
            return adjusted_components_list

        components_list = __get_components_list_from_html()

        adjusted_components_list = __adjust_components_list(components_list)

        return adjusted_components_list