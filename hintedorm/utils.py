from datetime import (
    date,
    datetime
)
from enum import Enum


class Text(str):
    ...


ALLOWED_TYPES = [str, Text, int, float, bool, datetime, date]
DEFAULT_MAX_STR_LEN = 100


class DBService(str, Enum):
    mysql = "mysql"
    postgres = "postgres"


class SQLOptions(str, Enum):
    nullable = "nullable"
    unique = "unique"
    primary_key = "primary_key"
