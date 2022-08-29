try:
    from orjson import loads, dumps
except ModuleNotFoundError:
    from json import loads, dumps
