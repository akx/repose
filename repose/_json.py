try:
    from orjson import dumps, loads
except ModuleNotFoundError:
    from json import dumps, loads  # noqa: F401
