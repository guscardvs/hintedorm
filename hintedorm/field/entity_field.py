import dataclasses
from typing import (
    Callable,
    Generic,
    TypeVar
)

from sql_type import get_sql_type_cls
from sql_type.base import SQLType
from sql_type.main import get_sql_type_from_service
from utils import (
    DBService,
    SQLOptions
)

from field._field import _Field

T = TypeVar("T")
SQL_T = TypeVar("SQL_T", bound=SQLType)
NOT_SET = object()


class EntityField(Generic[T, SQL_T]):
    sql_type: SQL_T

    def __init__(
        self,
        default_or_field: T,
        type_: type[T],
        name: str,
        *,
        db_service: str = "sqlite",
        nullable=False,
        primary_key=False,
        unique=False,
    ) -> None:
        self.required = True
        self.type_ = type_
        self.name = name
        self.col_name = name
        self.set_db_service(db_service)
        if isinstance(default_or_field, _Field):
            self.set_from_field_cls(default_or_field)
        else:
            self.set_default(default_or_field)
            self.set_options(nullable, primary_key, unique)
        self.set_sql_type()

    def set_db_service(self, db_service: str):
        if db_service == NOT_SET:
            db_service = get_sql_type_cls().db_service_name
        try:
            self.db_service = DBService(db_service)
        except ValueError as err:
            raise ValueError("db_service val is not a valid db_service") from err

    def set_from_field_cls(self, field: _Field):
        if field.column_name:
            self.col_name = field.column_name
        self.set_default(field.default)
        self.set_options(field.nullable, field.primary_key, field.unique)

    def set_default(self, default):
        self.default = default
        if default is Ellipsis:
            self.required = False
            self.default = None

    def set_options(self, nullable: bool, primary_key: bool, unique: bool):
        self.options = {
            SQLOptions.nullable: nullable,
            SQLOptions.primary_key: primary_key,
            SQLOptions.unique: unique,
        }

    def get_value(self, parser: Callable[[], T] = None) -> T:
        if parser is not None:
            return parser()
        return self.default or (lambda: self.type_())()  # type: ignore

    def set_sql_type(self):
        self.sql_type = get_sql_type_from_service(self.db_service)(
            self.col_name, self.options, self.type_, self.default
        )

    def type_declaration(self):
        return self.sql_type.build()

    def __repr__(self) -> str:
        return f"Field(name={self.name}, type={self.type_}, default={getattr(self, 'default', None)})"

    def get_field(self):
        return dataclasses.field(default=self.default)


def get_entity_field(
    default: T,
    type_: type[T],
    name: str,
    *,
    nullable=False,
    primary_key=False,
    unique=False,
    db_service=NOT_SET,
) -> type[EntityField[T, SQLType]]:
    return EntityField(
        default,
        type_,
        name,
        db_service=db_service,
        nullable=nullable,
        primary_key=primary_key,
        unique=unique,
    )  # type: ignore
