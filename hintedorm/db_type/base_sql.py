from datetime import (
    date,
    datetime
)
from typing import (
    Any,
    Optional
)

from utils import DEFAULT_MAX_STR_LEN

from db_type.base import DBType


class SQLType(DBType):
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

    def parse_default(self):
        if self.default is Ellipsis or self.default is None:
            return False
        if isinstance(self.default, str):
            self.default = self.str_enclosed(self.default)
        if isinstance(self.default, datetime):
            self.default = self.str_enclosed(self.default.isoformat(sep=" "))
        if isinstance(self.default, date):
            self.default = self.str_enclosed(self.default.isoformat())
        return True

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

    def get_text(self, arg: Optional[str]):
        return "TEXT"

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
        default = self.parse_default()
        if not default:
            return None
        return f"DEFAULT {self.default}"

    def build(self) -> str:
        default = self.get_default()
        base_str = f"{self.enclosed(self.field)} {self.get_sql_type()} {self.get_constraint_options()}"
        if default is None:
            return base_str
        return f"{base_str} {default}"
