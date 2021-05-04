from utils import (
    DBService,
    is_mysql,
    is_postgres
)

from db_type.mysql import MySQLType
from db_type.postgres import PostgresType


def get_db_type_cls():
    if is_mysql():
        return MySQLType
    if is_postgres():
        return PostgresType
    raise NotImplementedError


def get_db_type_from_service(db_service: DBService):
    __options = {DBService.mysql: MySQLType, DBService.postgres: PostgresType}
    return __options[db_service]

