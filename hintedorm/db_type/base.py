from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, TypeVar

from utils import ALLOWED_TYPES, SQLOptions

T = TypeVar("T")
RT = TypeVar("RT")


class DBType(ABC):
    db_service_name = ""

    def __init__(
        self,
        field: str = "",
        options: dict[SQLOptions, bool] = {},
        type_: type = type,
        default: Any = ...,
        type_arg: Optional[str] = None,
    ) -> None:
        self.field = field
        self.options = options
        self.type_ = type_
        self.type_arg = type_arg
        self.default = default

    def get_sql_type(self) -> str:
        return {k: getattr(self, f"get_{k.__name__.lower()}") for k in ALLOWED_TYPES}[
            self.type_
        ](self.type_arg)

    def validate_constraint(
        self, v: T, validator: Callable[[T], tuple[bool, RT]], err_msg: str
    ) -> RT:
        try:
            success, result = validator(v)
            if not success:
                raise ValueError
            return result
        except ValueError as err:
            raise ValueError(err_msg)

    def get_constraint_options(self) -> str:
        return " ".join(
            r
            for name, active in self.options.items()
            if (r := getattr(self, name.value)(active)) is not None
        )

    @abstractmethod
    def enclosed(self, v: Any) -> str:
        ...

    @abstractmethod
    def str_enclosed(self, v: Any) -> str:
        ...

    @abstractmethod
    def get_default(self) -> Optional[str]:
        ...

    @abstractmethod
    def build(self) -> str:
        ...

    @abstractmethod
    def nullable(self, active: bool):
        ...

    @abstractmethod
    def unique(self, active: bool):
        ...

    @abstractmethod
    def primary_key(self, active: bool):
        ...
