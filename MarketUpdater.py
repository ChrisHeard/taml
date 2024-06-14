from Market import Market
from typing import Callable, Optional
from GLOBALS import GLOBALS as GB

class MarketUpdater():

    reference_url: str
    parser: Optional[Callable[[str], str]]

    def __init__(self, market: Market, url, parser) -> None:
        
        self.market = market
        self.url = url
        self.parser = self.__get_parser(market, parser)

    def __get_parser(self, market, parser) -> Optional[Callable[[str], str]]:

        if self.parser:
            parser = GB.PARSER_REGISTRY.get(f"{market.id}_parser")
            if parser:
                return parser
            else:
                raise ValueError(f"Parser for {market.id} could not be found in PARSER_REGISTRY. Ensure that the parser string reference is named \"{market.id}_parser\" or set the parser bool to False.")
        else:
            return None