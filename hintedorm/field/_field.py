from typing import (
    Any,
    Generic,
    Optional,
    TypeVar
)

T = TypeVar("T")


class _Field(Generic[T]):
    def __init__(
        self,
        default: T,
        *,
        column_name: Optional[str],
        nullable: bool,
        primary_key: bool,
        unique: bool,
        unique_together: bool
    ):
        self.default = default
        self.column_name = column_name
        self.nullable = nullable
        self.primary_key = primary_key
        self.unique = unique
        self.unique_together = unique_together


def field(
    default: T = ...,
    *,
    column_name: Optional[str] = None,
    nullable: bool = False,
    primary_key: bool = False,
    unique: bool = False,
    unique_together: bool = False
) -> T:
    return _Field(
        default,
        column_name=column_name,
        nullable=nullable,
        primary_key=primary_key,
        unique=unique,
        unique_together=unique_together,
    )  # type: ignore
