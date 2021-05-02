from entity import Entity
from entity.utils import create_init
from field import field


@create_init
class Test(Entity):
    name: str = field(nullable=True)

    @classmethod
    def test(cls):
        print(cls.__doc__)


test = Test(name="username")

print(test.name)
print(test)
print(test._fields)
