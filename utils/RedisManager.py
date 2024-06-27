from backend.static.GLOBALS import GLOBALS as GB
from redis.asyncio import ConnectionPool, Redis
from typing import Optional, Any, List
from contextlib import asynccontextmanager
import json

class RedisManager:
    _instance: Optional['RedisManager'] = None
    _pool: Optional[ConnectionPool] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RedisManager, cls).__new__(cls)
            cls._instance.__init_pool()
        return cls._instance

    @asynccontextmanager
    async def __redis_connection(self):
        client = Redis.from_pool(connection_pool=self._pool)
        try:
            yield client
        finally:
            await client.aclose()

    def __init_pool(self) -> None:
        self._pool = ConnectionPool(
            host=GB.REDIS_HOST,
            port=GB.REDIS_PORT,
            db=GB.REDIS_DB,
            max_connections=GB.REDIS_MAX_CONNECTIONS
        )

    async def store_py_obj(self, hash_key: str, field_key: str, payload: Any) -> None:
        async with self.__redis_connection() as client:
            key_type = await client.type(hash_key)
            
            if key_type != b'none' and key_type != b'hash':
                await client.delete(hash_key)
            
            serialized_payload: str = json.dumps(payload)
            bytes_payload: bytes = serialized_payload.encode('utf-8')
            await client.hset(hash_key, mapping={field_key: bytes_payload})

    async def get_py_obj(self, hash_key: str, field_key: str) -> Optional[Any]:
        async with self.__redis_connection() as client:
            bytes_payload = await client.hget(hash_key, field_key)
            if bytes_payload is not None:
                serialized_payload = bytes_payload.decode('utf-8')
                return json.loads(serialized_payload)
            return None

    async def set_value(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        async with self.__redis_connection() as client:
            await client.set(key, value, ex=expire)

    async def get_value(self, key: str) -> Optional[str]:
        async with self.__redis_connection() as client:
            value = await client.get(key)
            return value.decode('utf-8') if value else None
    
    async def get_type(self, key: str) -> str:
        async with self.__redis_connection() as client:
            key_type = await client.type(key)
            return key_type.decode('utf-8')

    async def delete_key(self, key: str) -> None:
        async with self.__redis_connection() as client:
            await client.delete(key)

    async def key_exists(self, key: str) -> bool:
        async with self.__redis_connection() as client:
            return await client.exists(key) > 0

    async def push_to_list(self, list_name: str, *values: Any) -> None:
        async with self.__redis_connection() as client:
            await client.rpush(list_name, *values)

    async def pop_from_list(self, list_name: str) -> Optional[str]:
        async with self.__redis_connection() as client:
            value = await client.lpop(list_name)
            return value.decode('utf-8') if value else None

    async def get_list(self, list_name: str) -> List[str]:
        async with self.__redis_connection() as client:
            values = await client.lrange(list_name, 0, -1)
            return [value.decode('utf-8') for value in values]
        
    async def keys(self, keys_filter: str) -> List[str]:
        async with self.__redis_connection() as client:
            values = await client.keys(keys_filter)
            return [value.decode('utf-8') for value in values]

    async def set_key_expiration(self, key: str, seconds: int) -> None:
        async with self.__redis_connection() as client:
            await client.expire(key, seconds)

    class Config:
        arbitrary_types_allowed = True
