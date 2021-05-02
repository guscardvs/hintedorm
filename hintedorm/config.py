from encoders import EntityJsonEncoder

DEFAULT = object()

class Config:
    abstract = False
    table_name = DEFAULT
    default_json_encoder = EntityJsonEncoder
