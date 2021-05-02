from datetime import (
    date,
    datetime
)
from typing import (
    Any,
    Optional
)

from utils import DEFAULT_MAX_STR_LEN

from sql_type.base import SQLType


class MySQLType(SQLType):
    db_service_name = "mysql"

    def get_str(self, arg: Optional[str]):
        if arg is None:
            return f"VARCHAR({str(DEFAULT_MAX_STR_LEN)})"
        ct = self.validate_constraint(
            arg, lambda v: (True, int(v)), "varchar maxsize must be int"
        )
        self.validate_constraint(
            ct, lambda v: (ct > 255, ct), "VARCHAR maxsize must be lower than 255"
        )
        return f"VARCHAR({arg})"

    def get_int(self, arg: Optional[str]):
        return "INTEGER"

    def get_float(self, arg: Optional[str]):
        return "FLOAT"

    def get_bool(self, arg: Optional[str]):
        return "BOOL"

    def get_datetime(self, arg: Optional[str]):
        return "DATETIME"
    
    def get_date(self, arg: Optional[str]):
        return "DATE"

    def enclosed(self, v: Any) -> str:
        return f"`{v}`"

    def str_enclosed(self, v: Any) -> str:
        return f'"{v}"'

    def nullable(self, active: bool):
        if active:
            return "NULL"
        return "NOT NULL"

    def unique(self, active: bool):
        if active:
            return "UNIQUE"

    def primary_key(self, active: bool):
        if active:
            return "PRIMARY KEY"

    def get_default(self) -> Optional[str]:
        if self.default is Ellipsis or self.default is None:
            return None
        if isinstance(self.default, str):
            self.default = self.str_enclosed(self.default)

        if isinstance(self.default, datetime):
            self.default = self.str_enclosed(self.default.isoformat(sep=" "))
        if isinstance(self.default, date):
            self.default = self.str_enclosed(self.default.isoformat())
        return f"DEFAULT {self.default}"

    def build(self) -> str:
        default = self.get_default()
        base_str = f"{self.enclosed(self.field)} {self.get_sql_type()} {self.get_sql_options()}"
        if default is None:
            return base_str
        return f"{base_str} {default}"
