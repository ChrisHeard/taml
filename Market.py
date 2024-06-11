from GLOBALS import GLOBALS as GB
from pydantic import BaseModel
from typing import List, Optional, Callable
from redis import Redis
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from MarketsRef import MarketsRef as MR
import utils
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Market(BaseModel, ABC):
    id: str
    name: Optional[str] = None
    api_ticker: Optional[str] = None
    reference_url: Optional[str] = None
    suffix: Optional[str] = None
    index_hash: Optional[bytes] = None
    components_hash: Optional[bytes] = None
    link_hash: Optional[bytes] = None
    link_ref: Optional[List[str]] = None
    adjustments: Optional[List[str]] = None
    parser: Optional[bool] = None
    parser_fn: Optional[Callable[[str], str]] = None
    client: Optional[Redis] = None

    def __init__(self, id: str):
        super().__init__(id=id)
        self.client = utils.load_redis()
        self.__populate_ref_attrs()

    def __populate_ref_attrs(self):
        ref_dict: dict = MR.marketsDict
        id_dict: dict = ref_dict.get(self.id)

        if not id_dict:
            raise ValueError(f"ID {self.id} not found in MarketsRef")

        self.name = id_dict['name']
        self.api_ticker = id_dict['api_ticker']
        self.reference_url = id_dict['url']
        self.suffix = id_dict['suffix']
        self.index_hash = f'index:{self.id}'.encode('utf-8')
        self.components_hash = f'components:{self.id}'.encode('utf-8')
        self.link_hash = f'links:{self.id}'.encode('utf-8')
        self.adjustments = id_dict['adjustments']
        self.link_ref = self.__get_link_ref()
        self.parser = self.__get_parser()

    def __get_parser(self) -> Optional[Callable[[str], str]]:
        if self.parser:
            parser = GB.PARSER_REGISTRY.get(f"{self.id}_parser")
            if parser:
                return parser
            else:
                raise ValueError(f"Parser for {self.id} could not be found in PARSER_REGISTRY. Ensure that the parser string reference is named \"{self.id}_parser\" or set the parser bool to False.")
        else:
            return None
        
    def __get_link_ref(self) -> Optional[List[str]]:

        links_dict: dict = self.client.hgetall(self.link_hash)

        if not links_dict:
            logger.info(f'{self.link_hash} returned an empty dict and requires initializing. Use MarketUpdater to initialize.')
            return None
        
        max_key = max(links_dict.keys(), key=int)

        latest_list = utils.bytes_to_py(links_dict.get(max_key))

        return latest_list

    class Config:

        arbitrary_types_allowed = True