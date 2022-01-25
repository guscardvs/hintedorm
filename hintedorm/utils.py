from datetime import (
    date,
    datetime
)
from enum import Enum
from typing import (
    NewType,
    Optional,
    TypeVar,
    get_args,
    get_origin
)

T = TypeVar("T")

Text = NewType("Text", str)


ALLOWED_TYPES = [str, Text, int, float, bool, datetime, date]
DEFAULT_MAX_STR_LEN = 100


class DBService(str, Enum):
    mysql = "mysql"
    postgres = "postgres"


class SQLOptions(str, Enum):
    nullable = "nullable"
    unique = "unique"
    primary_key = "primary_key"


def is_optional(type_: type) -> bool:
    origin, args = get_origin(type_), get_args(type_)
    if origin is not None:
        try:
            tp, optional = args
        except ValueError:
            return False
        else:
            return optional is type(None)
    return False


def type_from_optional(type_: type[Optional[T]]) -> type[T]:
    tp, *_ = get_args(type_)
    return tp

def get_mysql():
    try:
        import aiomysql
        return aiomysql
    except ImportError:
        return

def get_postgres():
    try:
        import asyncpg
        return asyncpg
    except ImportError:
        return

def is_mysql() -> bool:
    return bool(get_mysql())


def is_postgres() -> bool:
    return bool(get_postgres())

def get_driver(db_service: DBService):
    check = globals().get("is_{}".format(db_service.value), lambda: False)
    if not check():
        raise Exception("Make sure to install db driver!")
    return globals.get("get_{}".format(db_service.value))

