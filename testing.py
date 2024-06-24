import asyncio
from RedisManager import RedisManager


async def main():
    
    
    redman = RedisManager()
    
    list = await redman.keys('*')

    print(list)

if __name__ == '__main__':
    asyncio.run(main())