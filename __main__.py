from MarketBuilder import MarketBuilder
from MarketsRef import MarketsRef as MR

mr_dict = MR.marketsDict

market_array = [MarketBuilder(id=key).build() for key in mr_dict]


for market in market_array:
    market.updater.update_all()