import pytest
from habits.models import Habit


@pytest.mark.django_db
def test_create_habit():
    habit = Habit.objects.create(name='Drink Water', is_good_habit=True)
    assert habit.name == 'Drink Water'
    assert habit.is_good_habit is True


@pytest.mark.django_db
def test_habit_str():
    habit = Habit.objects.create(name='Drink Water', is_good_habit=True)
    assert str(habit) == 'Drink Water Type: Good'