from diskcache import Cache


class LocalStorage:
    cache: Cache

    def __init__(self):
        self.cache = Cache(directory="workspace/tmp")

    def set_value(self, key: str, value: any):
        self.cache.set(key, value)

    def get_value(self, key: str) -> any:
        return self.cache.get(key)
