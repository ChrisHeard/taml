from pydantic import BaseModel
from MarketsRef import MarketsRef

class Market(BaseModel):
    id: str