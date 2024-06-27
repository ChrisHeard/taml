from ..utils.RedisManager import RedisManager
from ..utils.CustomLogger import CustomLogger
from pydantic import BaseModel

class MarketDAO(BaseModel):

    redis: RedisManager
    logger: CustomLogger

    async def index(self, index: str):
        data = await self.redis.get_py_obj("indices", index)
        return data
    
    async def links(self, index: str):
        data = await self.redis.get_py_obj("links", index)
        return data
    
    async def components(self, index: str):
        data = await self.redis.get_py_obj("components", index)
        return data

    async def keys(self):
        data = await self.redis.keys("*")
        return data

    class Config:
        arbitrary_types_allowed = True