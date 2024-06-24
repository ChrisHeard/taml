import asyncio
from MarketUpdater import MarketUpdater

async def main():

    updater = MarketUpdater()
    updater.active_dict = updater.cache.marketsDict['AEX']
    await updater.update_all(updater.active_dict)


if __name__ == '__main__':

    asyncio.run(main())


