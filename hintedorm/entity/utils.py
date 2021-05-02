import inspect
import sys


def create_init(cls):
    ls = {}
    globals = sys.modules[cls.__module__].__dict__
    exec("def __init__(self, name: str):\n self.name = name\n", globals, ls)
    setattr(cls, "__init__", ls["__init__"])
    cls.__doc__ = cls.__name__ + str(inspect.signature(cls)).replace(" -> None", "")
    return cls
