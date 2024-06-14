from Logger import CustomLogger
from pydantic import BaseModel
import utils
from typing import cast, List, Dict, Optional
from redis import Redis
from MarketsRef import MarketsRef as MR
from backend.MarketUpdater import MarketUpdater

class Market(BaseModel):
    
    id: str
    name: str
    api_ticker: str
    suffix: str
    index_hash: str
    components_hash: str
    link_hash: str
    link_ref: List[str]
    redis: Redis

    def __init__(self, id: str):

        self.id  = id

        id_dict: Dict = cast(Dict, MR.marketsDict.get(self.id))

        if not id_dict:
            raise ValueError(f"ID {self.id} not found in MarketsRef")
        
        self.redis = utils.load_redis()
        self.updater = MarketUpdater(market=self, url=id_dict['url'], parser=id_dict['parser'])
        self.logger = CustomLogger()
        self.name = id_dict['name']
        self.api_ticker = id_dict['api_ticker']
        self.suffix = id_dict['suffix']
        self.index_hash = f'index:{self.id}'
        self.components_hash = f'components:{self.id}'
        self.link_hash = f'links:{self.id}'
        self.adjustments = id_dict['adjustments']
        self.link_ref = self.__get_link_ref()

    def __get_link_ref(self) -> Optional[List[str]]:

        links_dict: dict = self.redis.hgetall(self.link_hash)

        if not links_dict:
            self.logger.info(f'{self.link_hash} returned an empty dict and requires initializing. Use MarketUpdater to initialize.')
            return None
        
        max_key = max(links_dict.keys(), key=int)

        latest_list = utils.bytes_to_py(links_dict.get(max_key))

        return latest_list
    

    # Pydantic configuration class
    class Config:

        arbitrary_types_allowed = True