import pytest

from habits.models import Habit


@pytest.fixture
def good_habit(db):
    return Habit.objects.create(name='good habit', is_good_habit=True)


def test_habit_str(good_habit):
    assert str(good_habit) == f"{good_habit.name} Type: Good"
