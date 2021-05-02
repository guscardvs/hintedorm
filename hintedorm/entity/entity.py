from typing import Any

from field.entity_field import EntityField

from entity.meta import MetaEntity


class Entity(metaclass=MetaEntity):
    _fields: list[EntityField]

    def __init__(self, **kwargs) -> None:
        self.set_fields_from_kwds(kwargs)

    def set_fields_from_kwds(self, kwds):
        fields = self.__class__.fields()
        for field in fields.values():
            if field.required and field.name not in kwds:
                raise AttributeError(
                    f"Field {field.name} is required"
                )
        for k, v in kwds.items():
            if k not in fields:
                raise AttributeError(
                    f"Entity({self.__class__.__name__}) does not have field{k}"
                )
            field = fields[k]
            setattr(self, k, field.set_value(v))

    @classmethod
    def get_fields(cls) -> list[EntityField]:
        return cls._fields  # type: ignore

    @classmethod
    def fields(cls) -> dict[str, EntityField]:
        return {field.name: field for field in cls.get_fields()}

    def serialize(self, option: str = "dict"):
        __options = {"dict": self.__serialize_dict, "json": self.__serialize_json}
        return __options[option]()

    def __serialize_dict(self):
        return {k: getattr(self, k) for k, _ in self._fields}  # type: ignore

    def __serialize_json(self):
        return self.Config.default_json_encoder().encode(self.__serialize_dict())

    def __getattribute__(self, name: str):
        attr = super().__getattribute__(name)
        if isinstance(attr, EntityField):
            return attr.value_decoder(attr.get_value())
        return attr

    def __setattr__(self, name: str, value: Any) -> None:
        attr = getattr(self, name)
        if isinstance(attr, EntityField):
            return super().__setattr__(name, attr.set_value(value))
        return super().__setattr__(name, value)


    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({', '.join(f'{field.name}={field.type_.__name__}' for field in self.get_fields())})"
