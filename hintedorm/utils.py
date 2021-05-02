from datetime import (
    date,
    datetime
)
from enum import Enum

ALLOWED_TYPES = [str, int, float, bool, datetime, date]
DEFAULT_MAX_STR_LEN = 100


class DBService(str, Enum):
    mysql = "mysql"
    postgres = "postgres"
    sqlite = "sqlite"

class SQLOptions(str, Enum):
    nullable = "nullable"
    unique = "unique"
    primary_key = "primary_key"
