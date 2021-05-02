from db_type.base import DBType
from field.entity_field import EntityField

from constraints.base import Constraint


class PrimaryKey(Constraint):
    def __call__(self, *, db_type: DBType):
        self.db_type = db_type
        return self.get_db_str()

    def get_db_str(self):
        if not self.fields:
            return None
        kwd = self.db_type.primary_key(True)
        return f"{kwd} ({', '.join(self.db_type.enclosed(field.name) for field in self.fields)})"

    def valid(self, field: EntityField) -> bool:
        return field.primary_key
