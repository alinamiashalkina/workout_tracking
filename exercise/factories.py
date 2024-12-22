import factory.fuzzy
from faker import Faker

from .models import Category, Exercise

faker = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _: faker.word())


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise

    name = factory.LazyAttribute(lambda _: faker.sentence()[:50])
    description = factory.Faker("text", max_nb_chars=200)
    category = factory.SubFactory(CategoryFactory)
