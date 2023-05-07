from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.tests.factories import HabitFactory

import pytest
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    def create_user(username="test@example.com", email="test@example.com"):
        return User.objects.create_user(username=username, email=email, password='testpass')

    return create_user


@pytest.fixture
def habit():
    return HabitFactory()


@pytest.fixture
def good_habit(db):
    return Habit.objects.create(name='good habit', is_good_habit=True)


@pytest.fixture
def bad_habit(db):
    return Habit.objects.create(name='bad habit', is_good_habit=False)


@pytest.fixture
def habit_data():
    return {'name': 'Drink enough water', 'is_good_habit': True}


@pytest.fixture
def habits_data(good_habit, bad_habit):
    return [{'name': good_habit.name}, {'name': bad_habit.name}]


@pytest.fixture
def habit_serializer(habit_data):
    return HabitSerializer(data=habit_data)
