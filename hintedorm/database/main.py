from dataclasses import dataclass
from pathlib import Path

from hintedorm.utils import DBService


@dataclass
class Database:
    host: str
    port: int
    user: str
    password: str
    db_name: str
    model_root: Path

    def __call__(self, db_service: DBService):
        self.db_service = db_service
