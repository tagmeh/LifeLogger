import factory  # Factoryboy
from faker import Faker
from django.contrib.auth import get_user_model


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = fake.unique.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.ascii_email()













