from constraints.primary_key import PrimaryKey
from db_type.mysql import MySQLType
from entity import Entity
from field import field
from utils import Text


class Test(Entity):
    id: str = field("", primary_key=True)
    name: str = field(nullable=True, primary_key=True)
    description: Text = field(unique_together=True)


test = Test(name="username", description="description")

print(Test.create_table)
