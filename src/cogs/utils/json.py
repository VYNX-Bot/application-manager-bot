import orjson


def loads(string: str):
    return orjson.loads(string)


def dumps(obj: object):
    return orjson.dumps(obj).decode("utf-8")


def load(fp):
    return orjson.loads(fp.read())


def dump(obj, fp):
    fp.write(orjson.dumps(obj).decode("utf-8"))
