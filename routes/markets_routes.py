from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from ..DAO.MarketDAO import MarketDAO
from ..utils.CustomLogger import CustomLogger
from ..utils.RedisManager import RedisManager


markets_router = APIRouter()
redis = RedisManager()
logger = CustomLogger()
market = MarketDAO(redis=redis, logger=logger)


@markets_router.get("/get_index")
async def get_index(market: str = Query(..., description="Specify the market to retrieve")):
    market_object = await redis.get_py_obj("indices", market)
    response = process_response(market_object)
    return response

@markets_router.get("/get_components")
async def get_components(market: str = Query(..., description="Specify the market to retrieve")):
    market_object = await redis.get_py_obj("components", market)
    response = process_response(market_object)
    return response

def process_response(object: object) -> JSONResponse:
    if object is None:
        raise HTTPException(status_code=404, detail="Market not found")
    response = JSONResponse(content=object)
    response.headers['Cache-Control'] = 'public, max-age=18000'
    return response