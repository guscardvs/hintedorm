from typing import Any

from utils import DEFAULT_MAX_STR_LEN

from db_type.base_sql import SQLType


class PostgresType(SQLType):
    db_service_name = "postgres"

    def enclosed(self, v: Any):
        return f'"{v}"'
    
    def str_enclosed(self, v: Any):
        return f"'{v}'"



