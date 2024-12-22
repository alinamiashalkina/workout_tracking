import factory.fuzzy
from django.contrib.auth import get_user_model
from faker import Faker
from .models import TrainerUser, ClientUser, Admin

faker = Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username", )

    username = factory.LazyAttribute(lambda _: faker.user_name())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.LazyAttribute(lambda _: faker.email())
    # пароль будет задан тестовый для всех созданных пользователей
    # в базу данных будет сохранен в хэшированном виде
    password = factory.PostGenerationMethodCall("set_password",
                                                "testpassword"
                                                )
    role = factory.fuzzy.FuzzyChoice(User.Role)


class TrainerUserFactory(UserFactory):
    class Meta:
        model = TrainerUser

    role = User.Role.TRAINER


class ClientUserFactory(UserFactory):
    class Meta:
        model = ClientUser

    role = User.Role.CLIENT


class AdminFactory(UserFactory):
    class Meta:
        model = Admin

    role = User.Role.ADMIN
