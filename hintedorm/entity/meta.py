from inspect import isclass

from config import (
    DEFAULT,
    Config
)
from field.entity_field import EntityField

from utils import ALLOWED_TYPES

SENTINEL = object()


class MetaEntity(type):
    def __new__(cls, name, bases, namespace, **kwds):
        cls.setattr_from_namespace(namespace)
        cls.set_config(namespace)
        cls.set_table_name(name, namespace)
        cls.add_annotations_to_child(namespace)
        print(cls.create_table_str(*namespace["_fields"]))
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
        return type_ in ALLOWED_TYPES

    @classmethod
    def add_to_namespace(cls, namespace: dict, field: str, type_: type):
        namespace[field] = ...

    @classmethod
    def create_field(cls, namespace: dict, field: str, type_: type):
        namespace[field] = EntityField(
            namespace[field], type_, field, db_service="mysql"
        )

    @classmethod
    def create_table_str(cls, *fields: EntityField):
        if not fields:
            return None
        return (
            f"CREATE TABLE({', '.join(field.type_declaration() for field in fields)})"
        )

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
