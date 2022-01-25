from datetime import datetime
from json import JSONEncoder
from typing import Any

from field.entity_field import EntityField


class DateTimeMixin(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat(sep="T")
        return super().default(o)

class EntityJsonEncoder(DateTimeMixin):
    def default(self, o: Any) -> Any:
        return o.get_value() if isinstance(o, EntityField) else super().default(o)
