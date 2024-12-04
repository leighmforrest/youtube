import factory
from faker import Faker

# Be sure to use items from Faker, not factory.Faker
fake = Faker()


class ThumbnailFactory(factory.DictFactory):
    url = factory.LazyAttribute(lambda _: fake.image_url())
    width = factory.LazyFunction(lambda: fake.random_int(min=50, max=200))
    height = factory.LazyFunction(lambda: fake.random_int(min=50, max=200))
