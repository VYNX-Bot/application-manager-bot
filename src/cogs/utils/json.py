import orjson

def loads(string:str):
    return orjson.loads(string)

def dumps(obj:object):
    return orjson.dumps(obj)