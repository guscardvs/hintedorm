# from typing import Optional

# from constraints.primary_key import PrimaryKey
# from db_type.mysql import MySQLType
# from entity import Entity
# from field import field
# from utils import Text


# class Test(Entity):
#     id: str = field("", primary_key=True)
#     name: str = field("", primary_key=True)
#     description: Optional[Text]


# test = Test(name="username")

# print(Test.create_table)
# print(test.serialize())
from pathlib import Path

from database.model_finder import ModelFinder

DIR = Path(__file__).resolve().parent

model_finder = ModelFinder(DIR / "models")

model_finder.find()
[print(val.create_table) for val in model_finder.models.values()]
