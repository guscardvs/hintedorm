import dataclasses
from typing import (
    Any,
    Callable,
    Generic,
    TypeVar,
    Union
)

from db_type import DBType
from utils import (
    SQLOptions,
    is_optional
)

from field._field import _Field

T = TypeVar("T")
DB_T = TypeVar("DB_T", bound=DBType)
NOT_SET = object()


class EntityField(Generic[T, DB_T]):
    db_type: DB_T

    def __init__(
        self,
        default_or_field: Union[_Field[T], T],
        type_: type[T],
        name: str,
        *,
        db_type: type[DB_T],
        nullable=False,
        primary_key=False,
        unique=False,
        unique_together=False,
    ) -> None:
        self.required = True
        self.type_ = type_
        self.name = name
        self.col_name = name
        if isinstance(default_or_field, _Field):
            self.set_from_field_cls(default_or_field)
        else:
            self.set_default(default_or_field)
            self.set_options(nullable, primary_key, unique, unique_together)
        self.set_db_type(db_type)
        if is_optional(self.type_):
            self.required = False
            self.options[SQLOptions.nullable] = True

    def set_db_type(self, db_type: type[DB_T]):
        self.db_type = db_type(self.col_name, self.options, self.type_, self.default)

    def set_from_field_cls(self, field: _Field):
        if field.column_name:
            self.col_name = field.column_name
        self.set_default(field.default)
        self.set_options(
            field.nullable, field.primary_key, field.unique, field.unique_together
        )

    def set_default(self, default):
        self.default = None
        if default is not Ellipsis:
            self.required = False
            self.default = default

    def set_options(
        self, nullable: bool, primary_key: bool, unique: bool, unique_together: bool
    ):
        self.primary_key = primary_key
        self.unique_together = unique_together
        self.options = {SQLOptions.nullable: nullable, SQLOptions.unique: unique}

    def get_value(self, parser: Callable[[Any], T] = None) -> T:
        val = self.default
        if hasattr(self, "alive_value"):
            val = self.alive_value
        if parser is not None:
            val = parser(val)
        return val  # type: ignore

    def value_decoder(self, raw_value: Any):
        return raw_value

    def type_declaration(self):
        return self.db_type.build_create()

    def __repr__(self) -> str:
        return f"EntityField(name={self.name}, type={self.type_}, default={getattr(self, 'default', None)})"

    def get_field(self):
        return dataclasses.field(default=self.default)

    def set_value(self, v):
        self.alive_value = v
        return self

    def is_unique(self):
        return self.options[SQLOptions.unique]
    
    def is_nullable(self):
        return self.options[SQLOptions.nullable]


def get_entity_field(
    default: T,
    type_: type[T],
    name: str,
    *,
    nullable=False,
    primary_key=False,
    unique=False,
    db_service=NOT_SET,
) -> type[EntityField[T, DBType]]:
    return EntityField(
        default,
        type_,
        name,
        db_service=db_service,
        nullable=nullable,
        primary_key=primary_key,
        unique=unique,
    )  # type: ignore
