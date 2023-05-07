import random

import factory
from faker import Faker

from habits.models import Habit, UserHabits
from django.contrib.auth import get_user_model

from habits.tests import providers

fake = Faker()

# Add providers
fake.add_provider(providers.HabitProvider())


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = fake.unique.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.ascii_email()


class HabitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Habit

    name = random.choice([fake.positive_habit(), fake.negative_habit()])
    is_good_habit = fake.boolean()


class UserHabitsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserHabits

    user = UserFactory
    date = fake.date_this_year
    habits = HabitFactory


class UserHabitsWithHabitsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserHabits

    user = factory.SubFactory(UserFactory)
    date = factory.LazyFunction(fake.date_this_year)
    habits = factory.RelatedFactoryList(HabitFactory, size=2)
