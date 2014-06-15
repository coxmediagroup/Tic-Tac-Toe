import json
from _abcoll import __all__


__all__ = ("get_exception_registry", "get_error_serializer", "JSONWriter")

_exc_registry = None
def get_exception_registry():
    global _exc_registry
    if _exc_registry is None:
        _exc_registry = ExceptionMappingRegistry()
    return _exc_registry


def get_error_serializer(exc_inst, response, writer=None, debug=False):
    if writer is None:
        writer = JSONWriter(resp=response)
    else:
        writer.set_response(response)
    reg = get_exception_registry()
    return ErrorSerializer(exc_inst, writer, reg, debug)


class JSONWriter(object):
    
    def __init__(self, resp=None, json_encoder=None):
        if json_encoder is None:
            self._encoder = json.JSONEncoder(indent=1)
        else:
            self._encoder = json_encoder
        self._resp = resp
    
    def set_response(self, resp):
        self._resp = resp
    
    def write(self, dict_):
        self._resp.set_status(dict_["status"])
        self._resp.write(self._encoder.encode(dict_))


class ExceptionMappingRegistry(object):
    def __init__(self):
        self._data = dict()

    def register(self, exc_type, errcode, extract_attrs=()):
        if exc_type not in self._data:
            self._data[exc_type] = (errcode, extract_attrs)
    
    def __getitem__(self, k):
        return self._data[k]
    
    def get(self, k, default=None):
        return self._data.get(k, default)


class ErrorSerializer(object):
    
    def __init__(self, exc_inst, writer, exc_registry=None, debug=False):
        self._exc_inst = exc_inst
        self._writer = writer
        self._debug_flag = debug
        if exc_registry is None:
            self._registry = get_exception_registry()
        else:
            self._registry = exc_registry
    
    def write(self):
        try:
            err_code, extract_attrs = self._registry[self._exc_inst.__class__]
        except KeyError:
            err_code = 500
            extract_attrs = ("message",)
        data = {"status": err_code}
        exc = self._exc_inst
        data.update((attr, getattr(exc, attr, None)) for attr in extract_attrs)
        self._writer.write(data)
