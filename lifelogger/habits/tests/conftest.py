import random

from faker import Faker

from habits.models import Habit

import pytest
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from habits.tests.providers import HabitProvider

User = get_user_model()
fake = Faker()

# Add providers
fake.add_provider(HabitProvider())


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    def create_user(email="test@example.com"):
        username = email
        return User.objects.create_user(
            username=username,
            email=email,
            password='testpass',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

    return create_user


@pytest.fixture
def good_habit(db):
    """Habit Instance of the Good variety"""
    return Habit.objects.create(name='good habit', is_good_habit=True)


@pytest.fixture
def bad_habit(db):
    """Habit Instance of the Bad variety"""
    return Habit.objects.create(name='bad habit', is_good_habit=False)


@pytest.fixture
def habit(good_habit, bad_habit):
    """Random good or bad Habit Instance."""
    return random.choice([good_habit, bad_habit])


@pytest.fixture
def habits(good_habit, bad_habit):
    """Random good or bad Habit Instance."""
    return [random.choice([good_habit, bad_habit]) for i in range(3)]


@pytest.fixture
def habit_object():
    """Habit dict object, not a Habit instance."""
    return {'name': fake.positive_habit(), 'is_good_habit': True}


@pytest.fixture
def habits_object():
    """A list of habit dict objects."""
    return [
        {'name': fake.positive_habit(), 'is_good_habit': True},
        {'name': fake.positive_habit(), 'is_good_habit': True},
        {'name': fake.positive_habit(), 'is_good_habit': True},
        {'name': fake.negative_habit(), 'is_good_habit': False},
        {'name': fake.negative_habit(), 'is_good_habit': False},
        {'name': fake.negative_habit(), 'is_good_habit': False},
    ]
