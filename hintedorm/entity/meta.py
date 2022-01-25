from inspect import isclass
from typing import (
    get_args,
    get_origin
)

from config import (
    DEFAULT,
    Config
)
from constraints.base import Constraint
from constraints.primary_key import PrimaryKey
from constraints.unique import Unique
from db_type.postgres import PostgresType
from field.entity_field import EntityField

from utils import (
    ALLOWED_TYPES,
    is_optional,
    type_from_optional
)

SENTINEL = object()


class MetaEntity(type):
    def __new__(cls, name, bases, namespace, **kwds):
        cls.setattr_from_namespace(namespace)
        cls.set_config(namespace)
        cls.db_type = PostgresType
        cls.set_table_name(name, namespace)
        cls.add_annotations_to_child(namespace)
        cls.create_table_str(namespace)
        return super().__new__(cls, name, bases, namespace, **kwds)

    @classmethod
    def setattr_from_namespace(cls, namespace: dict):
        namespace["_fields"] = []
        for name, type_ in cls.get_annotations(namespace).items():
            if name == "_fields":
                continue
            if not cls.has_valid_type(type_):
                raise NotImplementedError(f"field with type={type_} not implemented")
            if cls.is_annotation_only(namespace, name):
                cls.add_to_namespace(namespace, name, type_)
            cls.create_field(namespace, name, type_)
            namespace["_fields"].append(namespace[name])

    @classmethod
    def get_annotations(cls, namespace) -> dict[str, type]:
        return namespace.get("__annotations__", {})

    @classmethod
    def is_annotation_only(cls, namespace, field) -> bool:
        v = namespace.get(field, SENTINEL)
        return v == SENTINEL

    @classmethod
    def has_valid_type(cls, type_: type):
        if is_optional(type_):
            return type_from_optional(type_) in ALLOWED_TYPES
        return type_ in ALLOWED_TYPES

    @classmethod
    def add_to_namespace(cls, namespace: dict, field: str, type_: type):
        namespace[field] = ...

    @classmethod
    def create_field(cls, namespace: dict, field: str, type_: type):
        entity_field = EntityField(
            namespace[field], type_, field, db_type=cls.db_type
        )
        namespace[field] = entity_field

    @classmethod
    def create_table_str(cls, namespace):
        fields = namespace["_fields"]
        if not fields:
            namespace["create_table"] = None
        create_table = "CREATE TABLE(\n {}".format(
            ",\n ".join(field.type_declaration() for field in fields)
        )
        for constraint in cls.get_constraints(fields):
            if cst := constraint(db_type=cls.db_type()):
                create_table += ",\n {}".format(cst)
        namespace["create_table"] = create_table + "\n);"

    @classmethod
    def get_unique(cls, fields: list[EntityField]):
        return Unique(*fields)

    @classmethod
    def get_primary_key(cls, fields: list[EntityField]):
        return PrimaryKey(*fields)

    @classmethod
    def get_constraints(cls, fields) -> list[Constraint]:
        return [cls.get_unique(fields), cls.get_primary_key(fields)]

    @classmethod
    def set_config(cls, namespace: dict):
        bases: list = [Config]
        cfg_cls = namespace.get("Config")
        if isclass(cfg_cls):
            bases.append(cfg_cls)  # type: ignore
        namespace["Config"] = type("Config", tuple(bases), {})

    @classmethod
    def set_table_name(cls, name: str, namespace: dict):
        cfg_cls: type[Config] = namespace["Config"]
        if cfg_cls.table_name == DEFAULT:
            cfg_cls.table_name = name.lower()
        if not isinstance(cfg_cls.table_name, str):
            raise TypeError("table name must be str")

    @classmethod
    def add_annotations_to_child(cls, namespace):
        if "__annotations__" not in namespace:
            namespace["__annotations__"] = {}
        namespace["__annotations__"].update({"_fields": tuple[str, type]})
