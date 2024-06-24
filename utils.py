from GLOBALS import GLOBALS as GB
from collections import OrderedDict
import json
from typing import List, Dict, Any
from redis.asyncio import Redis


def normalize_dicts(dicts: List[Dict]) -> List[Dict]:

    '''
    Iterates over a list of dictionaries, aggregates a set of all unique keys found.

    Returns a list of dictionaries, each dict contains the full set of unique keys. 
    Values are empty strings if the original dict did not contain the corresponding key.
    '''

    unique_keys_dict: OrderedDict = OrderedDict()
    for sub_dict in dicts:
        for key in sub_dict.keys():
            if key not in unique_keys_dict:
                unique_keys_dict[key] = None
    
    unique_keys = list(unique_keys_dict.keys())

    normalized_list = []
    for sub_dict in dicts:
        normalized_sub_dict = {key: sub_dict.get(key, "") for key in unique_keys}
        normalized_list.append(normalized_sub_dict)

    return normalized_list

def load_redis() -> Redis:

    redis_client = Redis(host=GB.REDIS_HOST, port=GB.REDIS_PORT, db=GB.REDIS_DB)

    return redis_client

def bytes_to_py(bytes_obj: bytes) -> Any:

    serial_obj = bytes_obj.decode('utf-8')

    py_obj = json.loads(serial_obj)

    return py_obj

def py_to_bytes(py_obj: List | Dict) -> bytes:

    serial_obj = json.dumps(py_obj)

    bytes_obj = serial_obj.encode('utf-8')

    return bytes_obj