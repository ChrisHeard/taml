from typing import Dict, Callable
import parsers

class GLOBALS: 
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_TIMESTAMP_FORMAT = '%Y%m%d'
    REDIS_DATA_EXPIRATION_TIMER = 1 # days

    PARSER_REGISTRY: Dict[str, Callable[[str], str]] = {
        "bel20_parser": parsers.bel20_parser,
        "eurostoxx50_parser": parsers.eurostoxx50_parser,
        "ftse100_parser": parsers.ftse100_parser
    }