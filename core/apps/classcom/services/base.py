class BaseService:
    def list_index_default(self, array, index, default=None):
        try:
            return array[index]
        except (IndexError, Exception):
            return default

    def serializer_name_replace(self, data, replaces=[]):
        response = {}
        for key, val in data.items():
            if key in replaces:
                response[key.replace("_", "")] = val
            else:
                response[key] = val
        return response
