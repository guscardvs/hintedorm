from field.entity_field import EntityField

from entity.meta import MetaEntity


class Entity(metaclass=MetaEntity):
    _fields: list[EntityField]
    def __init__(self, **kwargs) -> None:
        field_names = [field.name for field in self.get_fields()]
        for k, v in kwargs.items():
            if k in field_names:
                setattr(self, k, v)
            else:
                raise AttributeError(
                    f"Entity({self.__class__.__name__}) does not have field{k}"
                )

    @classmethod
    def get_fields(cls) -> list[EntityField]:
        return cls._fields  # type: ignore

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
            return attr.get_value()
        return attr

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{field.name}={field.type_.__name__}' for field in self.get_fields())})"
