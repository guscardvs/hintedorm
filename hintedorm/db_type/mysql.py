from typing import Any

from db_type.base_sql import SQLType


class MySQLType(SQLType):
    db_service_name = "mysql"

    def enclosed(self, v: Any) -> str:
        return f"`{v}`"

    def str_enclosed(self, v: Any) -> str:
        return f'"{v}"'
