from typing import Any, Optional, TypeVar

T = TypeVar("T")


class _Field:
    def __init__(
        self,
        default: Any,
        *,
        column_name: Optional[str],
        nullable: bool,
        primary_key: bool,
        unique: bool,
    ) -> None:
        self.default = default
        self.column_name = column_name
        self.nullable = nullable
        self.primary_key = primary_key
        self.unique = unique


def field(
    default: T = ...,
    *,
    column_name: Optional[str] = None,
    nullable: bool = False,
    primary_key: bool = False,
    unique: bool = False,
) -> T:
    return _Field(
        default,
        column_name=column_name,
        nullable=nullable,
        primary_key=primary_key,
        unique=unique,
    )  # type: ignore
