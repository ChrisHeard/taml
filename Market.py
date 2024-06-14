from pydantic import BaseModel
from typing import List, Dict
from redis import Redis

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
    adjustments: Dict

    class Config:
        arbitrary_types_allowed = True
