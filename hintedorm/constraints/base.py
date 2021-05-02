from abc import (
    ABC,
    abstractmethod
)

from db_type.base import DBType
from field.entity_field import EntityField


class Constraint(ABC):
    def __init__(self, *fields: EntityField) -> None:
        self.fields = [field for field in fields if self.valid(field)]

    @abstractmethod
    def __call__(self, *, db_type: DBType):
        ...
    
    @abstractmethod
    def valid(self, field: EntityField) -> bool: ...
