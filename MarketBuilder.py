from Market import Market
from Logger import CustomLogger
import utils
from typing import Dict, List
from MarketsRef import MarketsRef as MR
from backend.MarketUpdater import MarketUpdater

class MarketBuilder:
    def __init__(self, id: str):
        self.id = id
        self.id_dict: Dict = MR.marketsDict.get(id)
        if not self.id_dict:
            raise ValueError(f"ID {id} not found in MarketsRef")
        self.redis = utils.load_redis()
        self.logger = CustomLogger()

    def build(self) -> Market:
        name = self.id_dict['name']
        api_ticker = self.id_dict['api_ticker']
        suffix = self.id_dict['suffix']
        index_hash = f'index:{self.id}'
        components_hash = f'components:{self.id}'
        link_hash = f'links:{self.id}'
        adjustments = self.id_dict['adjustments']
        link_ref = self._get_link_ref(link_hash)

        updater = MarketUpdater(market=None, url=self.id_dict['url'], parser=self.id_dict['parser'])
        
        market = Market(
            id=self.id,
            name=name,
            api_ticker=api_ticker,
            suffix=suffix,
            index_hash=index_hash,
            components_hash=components_hash,
            link_hash=link_hash,
            link_ref=link_ref,
            redis=self.redis,
            adjustments=adjustments
        )
        
        market.updater = updater
        market.logger = self.logger

        return market

    def _get_link_ref(self, link_hash: str) -> List[str]:
        links_dict: dict = self.redis.hgetall(link_hash)
        if not links_dict:
            self.logger.info(f'{link_hash} returned an empty dict and requires initializing. Use MarketUpdater to initialize.')
            return []

        max_key = max(links_dict.keys(), key=int)
        latest_list = utils.bytes_to_py(links_dict.get(max_key))
        return latest_list
